import serial
from time import time
from threading import Thread, Timer
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

MIN_DOT_TIME = 0.1
MAX_DOT_TIME = 2.0

DOT_TIME = 0.5

letters = "abcdefghijklmnopqrstuvwxyz"

morse = ["01","1000","1010","100", "0", "0010", "110", "0000", "00", "0111", "101", "0100", "11", "10", "111", "0110", "1101", "010", "000", "1", "001", "0001", "011", "1001", "1011", "1100"]

class Receiver(object):

    def __init__(self, copernicus):
        self.copernicus = copernicus
        self.timer = 0
        self.signals_cache = ''
        self.last_signal = ''

        self.setup()

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

    def calculate_angle(self, code):
        try:
            return ord(letters[morse.index(code)]) - ord('a') + 1
        except:
            return -1

    def error(self):
        pass

    def calculate_dot_time(self, knob_position):
        return ((knob_position - 64.0) / 63.0) * (MAX_DOT_TIME - MIN_DOT_TIME) + MIN_DOT_TIME

    def run(self):
        self.timer = time()

        while True:
            signal, _ = self.sock.recvfrom(1024)

            if signal == '0' or signal == '1':
                self.handle_signal(signal)

            Timer(3 * DOT_TIME, self.consume_signals_cache).start()

    def handle_signal(self, signal):
        print "handling signal..."

        current_time = time()

        if len(self.signals_cache) > 0 and signal == self.signals_cache[-1]:
            print "error!"
        else:
            time_diff = current_time - self.timer

            print "time diff: ", time_diff

            if time_diff <= DOT_TIME:
                self.signals_cache += '0'
            else:
                self.signals_cache += '1'

            print "cache: ", self.signals_cache

    def consume_signals_cache(self):
        print "consuming signals cache..."

        time_diff = time() - self.timer

        if time_diff > 3 * DOT_TIME:
            angle = self.calculate_angle(self.signals_cache)

            print "angle: ", angle

            if angle > 0:
                self.copernicus.set_dashboard_angle(angle)
            else:
                print "error!"

            self.timer = time()
