# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:03:10 2015

@author: mmedia
"""

import serial
import time
import socket

ser = serial.Serial('/dev/ttyS0', 38400)

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class sosSignal():
    
    PORT = 12000
    
    DOT = 0.1
    DASH = 3*DOT
    
    PART = DOT
    LETTER = 3*DOT
    WORD = 7*DOT
    
    def __init__(self, copernicus, *args, **kwargs):
        self.copernicus = copernicus
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
    def sos(self):
        print "calliing sos"
        self.led_sos()
        self.send_sos()

    def led_sos(self):
        for j in range(3):
            for i in range(3):
                self.led_signal(self.DASH if j%2 else self.DOT)
                if i == 2:
                    self.space(self.LETTER if j < 2 else self.WORD)
                else:
                    self.space(self.PART)

    def led_signal(self, length):
        self.copernicus.setLed(True)
        self.space(length)
        self.copernicus.setLed(False)

    def space(self, length):
        time.sleep(length)

    def send_sos(self):
        for j in range(3):
            for i in range(3):
                self.signal(self.DASH if j%2 else self.DOT)
                if i == 2:
                    self.space(self.LETTER if j < 2 else self.WORD)
                else:
                    self.space(self.PART)

    def signal(self, length):
        self.send_signal('0')
        self.space(length)
        self.send_signal('1')

    def send_signal(self, signal):
        self.sock.send(signal, ('<broadcast>', self.PORT))
        