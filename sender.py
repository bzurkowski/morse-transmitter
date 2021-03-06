import socket
from sos import Sos
from time import sleep

UDP_IP = "192.168.17.83"
UDP_PORT = 5005

class Sender:

    def __init__(self, copernicus):
        self.copernicus = copernicus
        self.setup()

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sos  = Sos(self.copernicus)

        self.copernicus.write(152)

    def run(self):
        while True:            
            self.copernicus.flush()
            
            signal = self.copernicus.read()

            if (signal == 195):
                self.send_signal('1')
            elif (signal == 194):
                self.send_signal('0')
                sleep(0.05)
            elif (signal == 197):
                self.sos.sos()

    def send_signal(self, signal):
        self.sock.sendto(str(signal), (UDP_IP, UDP_PORT))
