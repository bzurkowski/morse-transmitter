# -*- coding: utf-8 -*-
import socket
from sos import sosSignal

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

SIGNAL_BUTTON = chr(128 + 16)

class Sender:

    def __init__(self, copernicus):
        self.copernicus = copernicus
        self.sos = sosSignal(copernicus)

        self.setup()

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.copernicus.write(128 + 16 + 8)
        #self.copernicus.autoUpdate(button2 = True)

    def run(self):
        while True:
            # self.copernicus.flushInput()

            signal = self.copernicus.read()

            if (signal == 195):
                self.send_signal('1')
                print 1
            elif (signal == 194):
                self.send_signal('0')
                print 0
            elif (signal == 197):
                print "SOS"
                self.sos.sos()

    def send_signal(self, signal):
        self.sock.sendto(str(signal), (UDP_IP, UDP_PORT))
