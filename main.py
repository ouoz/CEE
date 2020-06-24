import pyaudio
import numpy as np
import time
from scipy.signal import argrelmax

# interphone setting
CHUNK = 1024
RATE = 8000    # sampling rate
dt = 1.0/RATE
freq = np.linspace(0,1.0/dt,CHUNK)
fn = 1.0/dt/2    # nyquist freq
FREQ_HIGH_BASE = 863.0  # high tone frequency
FREQ_LOW_BASE = 691.0   # low tone frequency
FREQ_ERR = 0.02         # allowable freq error
#variable
detect_high = False
detect_low = False

def getMaxFreqFFT(sound, chunk, freq):
    f = np.fft.fft(sound)/(chunk/2)
    f_abs = np.abs(f)
    peak_args = argrelmax(f_abs[:(int)(chunk/2)])
    f_peak = f_abs[peak_args]
    f_peak_argsort = f_peak.argsort()[::-1]
    peak_args_sort = peak_args[0][f_peak_argsort]
    return freq[peak_args_sort[0]]

def detectDualToneInOctave(freq_in, freq_high_base, freq_low_base, freq_err):
    det_h = det_l = False
    octave_h = freq_in / freq_high_base
    octave_l = freq_in / freq_low_base
    near_oct_h = round(octave_h)
    near_oct_l = round(octave_l)
    if near_oct_h == 0 or near_oct_l == 0:
        return False, False
    err_h = np.abs((octave_h-near_oct_h) / near_oct_h)
    err_l = np.abs((octave_l-near_oct_l) / near_oct_l)

    if err_h < freq_err:
        det_h = True
    elif err_l < freq_err:
        det_l = True

    return det_h, det_l

if __name__=='__main__':
    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
    start = time.time()
    cnt = 0

    while stream.is_active():
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            abs_array = np.abs(ndarray)/32768
        
            if abs_array.max() > 0.001:
                freq_max = getMaxFreqFFT(ndarray, CHUNK, freq)
                print("Max Frequency:", freq_max, "Hz")
                h,l = detectDualToneInOctave(freq_max, FREQ_HIGH_BASE, FREQ_LOW_BASE, FREQ_ERR)
                cur  = time.time() 
                if h:
                    if cur - start > 1.0:
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