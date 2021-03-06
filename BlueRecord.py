import pyaudio
import numpy as np
import time
from scipy.signal import argrelmax



out_fn = "peeks.txt"

record_exit = False


# sampling highest frequency until 5th

"""A error occurs now version... let's classify"""
def set_exit():
    if not record_exit:
        record_exit = True
    else:
        record_exit = False

def getMaxFreqFFT(sound, chunk, freq):
    f = np.fft.fft(sound)/(chunk/2)
    f_abs = np.abs(f)
    peak_args = argrelmax(f_abs[:(int)(chunk/2)])
    f_peak = f_abs[peak_args]
    f_peak_argsort = f_peak.argsort()[::-1]
    peak_args_sort = peak_args[0][f_peak_argsort]
    return [freq[peak_args_sort[0]], freq[peak_args_sort[1]], freq[peak_args_sort[2]]] 


def record():
    # interphone setting
    CHUNK = 1024
    RATE = 48000    # sampling rate
    dt = 1/RATE
    freq = np.linspace(0,1.0/dt,CHUNK)
    fn = 1/dt/2    # nyquist freq
    FREQ_HIGH_BASE = 863.0  # high tone frequency
    FREQ_LOW_BASE = 691.0   # low tone frequency
    FREQ_ERR = 0.02         # allowable freq error
    #variable
    detect_high = False
    detect_low = False
    streak = 10
    
    
    P = pyaudio.PyAudio()
    stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
    start = time.time()
    freq_max = -1000.0
    cnt = 0
    pos = 0
    peeks = []
    cur = 0
    last_t = 0

    while stream.is_active() and not record_exit:
        try:
            input = stream.read(CHUNK, exception_on_overflow=False)
            ndarray = np.frombuffer(input, dtype='int16')
            abs_array = np.abs(ndarray)/32768

            if abs_array.max() > 0.015:
                freq_max = getMaxFreqFFT(ndarray, CHUNK, freq)
                
                if cnt > streak: 
                    flag = False
                    for val in freq_max: 
                        if abs(val - cur) < 0.001: 
                            flag = True
                            break
                    if not flag: 
                        peeks.append(cur)
                        cur = freq_max[0]
                        cnt = 0
                        continue

                flag = False
                for val in freq_max:
                    if abs(cur - val) < 0.001 :
                        cnt += 1
                        flag = True
                        break
                    
                
                if flag and ((time.time() - last_t) < 0.2):
                    last_t = time.time()
                    continue
                else: 
                    cnt = 0
                    cur = freq_max[0]
                    last_t = time.time()
    
        except KeyboardInterrupt:
            break


    with open(out_fn, 'w', encoding = "utf-8-sig") as kaki: 
        for val in peeks: 
            kaki.write(str(val) + '\n')

    stream.stop_stream()
    stream.close()
    P.terminate()
    
    
    
    
    
    
    
    
    
    
    
class Recording:    

    def __init__(self):
        self.record_exit = False
    
    def set_exit(self):
        if not self.record_exit:
            self.record_exit = True
        else:
            self.record_exit = False

    def getMaxFreqFFT(self, sound, chunk, freq):
        f = np.fft.fft(sound)/(chunk/2)
        f_abs = np.abs(f)
        peak_args = argrelmax(f_abs[:(int)(chunk/2)])
        f_peak = f_abs[peak_args]
        f_peak_argsort = f_peak.argsort()[::-1]
        peak_args_sort = peak_args[0][f_peak_argsort]
        return [freq[peak_args_sort[0]], freq[peak_args_sort[1]], freq[peak_args_sort[2]], freq[peak_args_sort[3]], freq[peak_args_sort[4]]] 


    def record(self):
        # interphone setting
        CHUNK = 1024
        RATE = 48000    # sampling rate
        dt = 1/RATE
        freq = np.linspace(0,1.0/dt,CHUNK)
        fn = 1/dt/2    # nyquist freq
        FREQ_HIGH_BASE = 863.0  # high tone frequency
        FREQ_LOW_BASE = 691.0   # low tone frequency
        FREQ_ERR = 0.02         # allowable freq error
        #variable
        detect_high = False
        detect_low = False
        streak = 10
        
        
        P = pyaudio.PyAudio()
        stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
        start = time.time()
        freq_max = -1000.0
        cnt = 0
        pos = 0
        peeks = []
        cur = 0


        while stream.is_active() and not self.record_exit:
            try:
                input = stream.read(CHUNK, exception_on_overflow=False)
                ndarray = np.frombuffer(input, dtype='int16')
                abs_array = np.abs(ndarray)/32768

                if abs_array.max() > 0.025:
                    freq_max = getMaxFreqFFT(ndarray, CHUNK, freq)
                    print(freq_max)
                    
                    if cnt > streak: 
                        flag = False
                        for val in freq_max: 
                            if abs(val - cur) < 0.001: 
                                flag = True
                                break
                        if not flag: 
                            peeks.append(cur)
                            cur = freq_max[0]
                            cnt = 0
                            continue

                    flag = False
                    for val in freq_max:
                        if abs(cur - val) < 0.001 :
                            cnt += 1
                            flag = True
                            break
                        
                    
                    if flag and ((time.time() - last_t) < 0.2):
                        last_t = time.time()
                        continue
                    else: 
                        cnt = 0
                        cur = freq_max[0]
                        last_t = time.time()
        
            except KeyboardInterrupt:
                break


        with open(out_fn, 'w', encoding = "utf-8-sig") as kaki: 
            for val in peeks: 
                kaki.write(str(val) + '\n')

        stream.stop_stream()
        stream.close()
        P.terminate()
