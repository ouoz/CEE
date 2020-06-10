import pyaudio
import numpy as np
import time
from scipy.signal import argrelmax

# interphone setting
CHUNK = 1024
RATE = 8000    # sampling rate
dt = 1/RATE
freq = np.linspace(0,1.0/dt,CHUNK)
fn = 1/dt/2    # nyquist freq
FREQ_HIGH_BASE = 863.0  # high tone frequency
FREQ_LOW_BASE = 691.0   # low tone frequency
FREQ_ERR = 0.02         # allowable freq error
#variable
detect_high = False
detect_low = False

# FFTで振幅最大の周波数を取得する関数
def getMaxFreqFFT(sound, chunk, freq):
    # FFT
    f = np.fft.fft(sound)/(chunk/2)
    f_abs = np.abs(f)
    # ピーク検出
    peak_args = argrelmax(f_abs[:(int)(chunk/2)])
    f_peak = f_abs[peak_args]
    f_peak_argsort = f_peak.argsort()[::-1]
    peak_args_sort = peak_args[0][f_peak_argsort]
    # 最大ピークをreturn
    return freq[peak_args_sort[0]]

# 検知した周波数がインターホンの音の音か判定する関数
def detectDualToneInOctave(freq_in, freq_high_base, freq_low_base, freq_err):
    det_h = det_l = False
    # 検知した周波数が高音・低音のX倍音なのか調べる
    octave_h = freq_in / freq_high_base
    octave_l = freq_in / freq_low_base
    near_oct_h = round(octave_h)
    near_oct_l = round(octave_l)
    if near_oct_h == 0 or near_oct_l == 0:
        return False, False
    # X倍音のXが整数からどれだけ離れているか
    err_h = np.abs((octave_h-near_oct_h) / near_oct_h)
    err_l = np.abs((octave_l-near_oct_l) / near_oct_l)

    # 基音、２倍音、３倍音の付近であればインターホンの音とする
    if err_h < freq_err:
        det_h = True
    elif err_l < freq_err:
        det_l = True

    return det_h, det_l

if __name__=='__main__':
    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
    start = time.time() #高音が最後に記録された時間、デフォルトでは開始時間とする
    cnt = 0 #高音がどれだけ続いたかを示す、この値によって低音の判定に移るか決める

    while stream.is_active():
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            abs_array = np.abs(ndarray)/32768
        
            if abs_array.max() > 0.001:
                # FFTで最大振幅の周波数を取得
                freq_max = getMaxFreqFFT(ndarray, CHUNK, freq)
                print("Max Frequency:", freq_max, "Hz")
                h,l = detectDualToneInOctave(freq_max, FREQ_HIGH_BASE, FREQ_LOW_BASE, FREQ_ERR)
                cur  = time.time() 
                if h:
                    if cur - start > 1.0: #高音が記録された間隔が3秒以上以上開いていたら
                        start = cur
                        cnt = 0
                    cnt += 1
                    detect_high = True
                    print("First Part Detected")
                if l and cnt > 1:
                    detect_low = True
                    print("Second Part Detected")
    
                # dual tone detected
                if detect_high and detect_low:
                    print("Intercom has been detected !!!!!!!")
                    time.sleep(5)
                    print("flag reset")
                    cnt = 0
                    detect_high = detect_low = False
    
        except KeyboardInterrupt:
            break
        
    stream.stop_stream()
    stream.close()
    P.terminate()