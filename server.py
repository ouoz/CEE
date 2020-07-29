# -*- coding: utf-8 -*-
# Main.py
from RN42 import RN42
from time import sleep
import RPi.GPIO as GPIO
import sys
import time

class Main:
    #""" Main Class """

    # Setting & Connect
    ras = RN42("ras", "9C:5C:F9:B2:1C:DE", 1)
    ras.connectBluetooth(ras.bdAddr,ras.port)

    print("Entering main loop now")

    while 1:
        try:
            ras.sock.send("Hello World")
            print("data send")
            time.sleep(1)
        except KeyboardInterrupt:
            ras.disconnect(ras.sock)
