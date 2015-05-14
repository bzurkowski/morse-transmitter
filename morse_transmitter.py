import os
from threading import Thread

from copernicus import Copernicus
from sender     import Sender
from receiver   import Receiver

if __name__ == "__main__":
  copernicus = Copernicus('/dev/ttyS0', 38400)

  sender = Sender(copernicus)

  receiver = Receiver(copernicus)

  Thread(target=sender.run).start()

  print "Sender started..."

  Thread(target=receiver.run).start()

  print "Receiver started..."
