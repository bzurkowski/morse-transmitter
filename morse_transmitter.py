import os

from copernicus.copernicus import Copernicus
from sender import Sender
from receiver import Receiver
from threading import Thread

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath("../" + __file__)))
SERIAL_PATH = os.path.join(BASE_DIR, 'dev', 'ttyS0')

if __name__ == "__main__":
  copernicus = Copernicus(SERIAL_PATH, 38400)

  sender = Sender(copernicus)

  receiver = Receiver(copernicus)

  Thread(target=sender.run).start()

  print "Sender started..."

  Thread(target=receiver.run).start()

  print "Receiver started..."
