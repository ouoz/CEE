import pyaudio
import numpy as np
import time
from scipy.signal import argrelmax


"""A error occurs now version... let's classify !"""
detect_exit = False

def set_exit():
    if not detect_exit:
        detect_exit = True
    else:
        detect_exit = False
def getMaxFreqFFT(sound, chunk, freq):
    f = np.fft.fft(sound)/(chunk/2)
    f_abs = np.abs(f)
    peak_args = argrelmax(f_abs[:(int)(chunk/2)])
    f_peak = f_abs[peak_args]
    f_peak_argsort = f_peak.argsort()[::-1]
    peak_args_sort = peak_args[0][f_peak_argsort]
    return [freq[peak_args_sort[0]], freq[peak_args_sort[1]], freq[peak_args_sort[2]], freq[peak_args_sort[3]], freq[peak_args_sort[4]]]

def getTop5(freq_in, freq_high_base, freq_err):
    for val in freq_in: 
        if abs(val - freq_high_base) < freq_err: 
            return True
    
    return False

def detect():
    # interphone setting
    CHUNK = 1024
    RATE = 48000    # sampling rate
    dt = 1.0/RATE
    freq = np.linspace(0,1.0/dt,CHUNK)
    fn = 1.0/dt/2    # nyquist freq
    FREQ_ERR = 0.02         # allowable freq error
    peeks = [float(val.strip()) for val in open("peeks.txt", 'r', encoding = "utf-8-sig").readlines()]
    #variable
    itr = 0
    det_cnt = 0
    
    
    
    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
    start = time.time()
    cnt = 0
    last_det = 0
    
    print(peeks)

    while stream.is_active() and not detect_exit:
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            abs_array = np.abs(ndarray)/32768
        
            if abs_array.max() > 0.01:
                freq_max = getMaxFreqFFT(ndarray, CHUNK, freq)
                #print("Max Frequency:", freq_max, "Hz")
                h = getTop5(freq_max, peeks[itr], FREQ_ERR)
                cur_t  = time.time() 
                
                if cur_t - last_det > 1.0: 
                    itr = 0
                    cnt = 0

                if cnt > 5 and itr == len(peeks) - 1: 
                    print("Intercom has been detected !!!!!!!")
                    det_cnt += 1
                    time.sleep(5)
                    print("flag reset")
                    itr = 0
                    cnt = 0
                elif cnt > 5 and itr != len(peeks) - 1 and getTop5(freq_max, peeks[itr + 1], FREQ_ERR): 
                    itr += 1
                    cnt = 0
                    last_det = cur_t
                    print("detected!!!")
                elif h:
                    cnt += 1
                    last_det = cur_t
    
        except KeyboardInterrupt:
            break
        
    stream.stop_stream()
    stream.close()
    P.terminate()