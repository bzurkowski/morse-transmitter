# -*- coding: utf-8 -*-
import serial
import time
import socket

UDP_IP = "192.168.17.83"
UDP_PORT = 5005

SIGNAL_BUTTON = chr(128 + 16)
DOT_TIME      = 0.5
LINE_TIME     = 3 * DOT_TIME

timer = time.time()

class Timer:

    def __init__(self):
        self.time = time.time()

    def reset(self):
        self.time = time.time()

class Sender:

    def __init__(self):
        self.setup()

    def setup(self):
        print "UDP target IP:", UDP_IP
        print "UDP target port:", UDP_PORT

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ser = serial.Serial('/dev/ttyS0', 38400)

        self.ser.write(SIGNAL_BUTTON)

        self.timer = Timer()

    def input_signals(self):
        while True:
            self.ser.flushInput()
            signal = self.ser.read(1)


            if (ord(signal) == 195):  # 128 + 64 + 2 + 1
                current_time = time.time()

                if (current_time - self.timer.time) <= DOT_TIME:
                    print 0
                    self.send_signal(0)
                else:
                    print 1
                    self.send_signal(1)

                self.timer.reset()

    def send_signal(self, signal):
        self.sock.sendto(str(signal), (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    s = Sender()

    s.input_signals()


