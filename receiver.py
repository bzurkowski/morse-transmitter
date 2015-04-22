import serial
import time
import threading
import socket

ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
text = "abcdefghijklmnopqrstuvwxyz"
morse= ["01","1000","1010","100", "0", "0010", "110", "0000", "00", "0111", "101", "0100", "11", "10", "111", "0110", "1101", "010", "000", "1", "001", "0001", "011", "1001", "1011", "1100"]

def givemeangle(code):
  try:
    return ord(text[morse.index(code)])-ord('a')+1
  except:
    return -1

#ser.write(chr(givemeangle(c)))

dotTime = 0.1

def knoobListener():
  min = 0.1
  max = 2.0
  ser.write(chr(128+4))
  while True:
    cc = ser.read(1)
    if len(cc)>0:
      result = (((float(ord(cc)) - 64.0)/63.0)*(max-min))+min
      #dotTime = result

knoobListenerThread = threading.Thread(target=knoobListener)
knoobListenerThread.start()

timer = time.time()
char = ""

def input_signals(what):
  global timer
  global char

  current_time = time.time()
  if (current_time - timer) <= dotTime:
    if what == "0":
      print 0
      char.join("0")
      #ser.write(chr(32+1))
    else:
      print 1
      char.join("1")
  else:
    print(char)
    timer = time.time()

UDP_IP = "192.168.17.83"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
while True:
  data, addr = sock.recvfrom(1024)
  print(data)
  if data in ["0","1"]:
    input_signals(data)





knoobListenerThread.join()