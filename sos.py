# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:03:10 2015

@author: mmedia
"""

import serial
import time
import socket

ser = serial.Serial('/dev/ttyS0', 38400)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind(('', 0))
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


query = {
    'LED1_ON': chr(32 + 1),
    'LED1_OFF': chr(32),
    'AUT_UP_B1': chr(128 + 16),
    'AUT_UP_B2': chr(128 + 8),
}

resp = {
    'B1_PR': chr(128 + 64 + 2 + 1),
    'B2_PR': chr(128 + 64 + 4 + 1),
}

IP = "192.168.17.83"
PORT = 5005

DOT = 0.1
DASH = 3*DOT

PART = DOT
LETTER = 3*DOT
WORD = 7*DOT


def led_sos():
    for j in range(3):
        for i in range(3):
            signal(DASH if j%2 else DOT)
            if i == 2:
                space(LETTER if j < 2 else WORD)
            else:
                space(PART)

def signal(length):
    ser.write(query['LED1_ON'])
    time.sleep(length)
    ser.write(query['LED1_OFF'])

def space(length):
    time.sleep(length)



def send_sos():
    for j in range(3):
        for i in range(3):
            send_signal(DASH if j%2 else DOT)
            if i == 2:
                space(LETTER if j < 2 else WORD)
            else:
                space(PART)

def send_signal(length):
    sock.sendto('0' if length == DOT else '1', (IP, PORT))



ser.write(query['AUT_UP_B2'])

sock.sendto('0', (IP, PORT))

while True:
    c = ser.read(1)

    if len(c) > 0:
        if c == resp['B2_PR']:
            send_sos()