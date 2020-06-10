# coding: utf-8

import pyaudio
import numpy as np

CHUNK = 1024
RATE = 44100 # サンプリング周波数

P = pyaudio.PyAudio()

stream = P.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)

while stream.is_active():
    try:
        input = stream.read(CHUNK, exception_on_overflow=False)
        # bufferからndarrayに変換
        ndarray = np.frombuffer(input, dtype='int16')

        ''' 高速フーリエ変換をして時間領域から周波数領域にする場合は下1行を追加する '''
        #f = np.fft.fft(ndarray)

        # ndarrayからリストに変換
        # Pythonネイティブのint型にして扱いやすくする
        a = [np.asscalar(i) for i in ndarray]

        # 試しに0番目に入っているものを表示してみる
        print(a[0])

        ''' 音声を出力する場合はstreamのoutputをTrueにして下2行を追加する '''
 #output = np.array(a, dtype='int16').tobytes()
        #stream.write(output)
    except KeyboardInterrupt:
        break

stream.stop_stream()
stream.close()
P.terminate()

print('Stop Streaming')