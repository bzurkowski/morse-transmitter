from copernicus import Copernicus
from sender import Sender
from threading import Thread


if __name__ == "__main__":
  copernicus = Copernicus('/dev/ttyS0', 38400)
  
  sender = Sender(copernicus)
  
  Thread(target = sender.accept_signals).start()
  
