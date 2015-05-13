import socket
from threading import Thread, Timer
from time import time
from morse_codes import morse_codes, letters

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

MIN_DOT_TIME = 0.1
MAX_DOT_TIME = 2.0

DOT_TIME = 1.0

class Receiver(object):

    def __init__(self, copernicus):
        self.copernicus = copernicus
        self.setup()

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

        self.letter_timer = None
        self.word_timer  = None

        self.prev_signal = ''

        self.reset_timer()
        self.reset_cache()

    def run(self):
        while True:
            signal, _ = self.sock.recvfrom(1024)

            if self.valid_signal(signal):
                self.handle_signal(signal)
            else:
                self.error("invalid signal")

            self.prev_signal = signal

            self.reset_timer()

    def valid_signal(self, signal):
        if signal != self.prev_signal and signal in ['0', '1']:
            return True
        return False

    def handle_signal(self, signal):
        if signal == '1':
            self.copernicus.led_on()
        else:
            self.copernicus.led_off()
            return

        time_diff = time() - self.timer

        if time_diff <= DOT_TIME:
            self.signals_cache += '0'
        else:
            self.signals_cache += '1'

        print "cache: ", self.signals_cache

    def consume_signals_cache(self):
        print "consuming signals cache..."

        time_diff = time() - self.timer

        angle = self.calculate_angle(self.signals_cache)

        if angle > 0:
            self.copernicus.set_dashboard_angle(angle)
        else:
            self.error("invalid morse code")

        self.reset_cache()
        self.reset_timer()

    def separate_word(self):
        self.copernicus.reset_dashboard_angle()

    def calculate_angle(self, code):
        try:
            letter = letters[morse_codes.index(code)]
            print letter

            return ord(letter) - ord('a') + 1
        except:
            return -1

    def calculate_dot_time(self, knob_position):
        dot_time  = (knob_position - 64.0) / 63.0
        dot_time *= MAX_DOT_TIME - MIN_DOT_TIME
        dot_time += MIN_DOT_TIME

        return dot_time

    def reset_timer(self):
        self.timer = time()

        if self.letter_timer:
            self.letter_timer.cancel()

        if self.word_timer:
            self.word_timer.cancel()

        self.letter_timer = Timer(3 * DOT_TIME, self.consume_signals_cache)
        self.word_timer   = Timer(7 * DOT_TIME, self.separate_word)

        self.letter_timer.start()
        self.word_timer.start()

    def reset_cache(self):
        self.signals_cache = ''

    def error(self, msg=None):
        if msg:
            print msg
        else:
            print "error!"

        self.reset_cache()
        self.reset_timer()
