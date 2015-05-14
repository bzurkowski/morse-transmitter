import socket
from time import sleep

class Sos():

    UDP_IP = "192.168.17.83"
    PORT = 5005

    DOT = 0.4
    DASH = 3*DOT

    PART = DOT
    LETTER = 4*DOT

    def __init__(self, copernicus, *args, **kwargs):
        self.copernicus = copernicus
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def sos(self):
        print "calliing sos"
        self.send_sos()

    def space(self, length):
        sleep(length)

    def send_sos(self):
        for j in range(3):
            for i in range(3):
                self.signal(self.DASH if j%2 else self.DOT)
                if i == 2:
                    self.space(self.LETTER)
                else:
                    self.space(self.PART)

    def signal(self, length):
        self.send_signal('1')
        self.copernicus.led_on()
        self.space(length)
        self.send_signal('0')
        self.copernicus.led_off()

    def send_signal(self, signal):
        self.socket.sendto(signal, (self.UDP_IP, self.PORT))
