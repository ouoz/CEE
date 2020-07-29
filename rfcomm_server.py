import serial
s = serial.Serial("/dev/rfcomm0", 9600, timeout=10)
print(s.readline())