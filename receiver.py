def receiver():
    import serial
    import time
    import threading
    import socket

    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    text = "abcdefghijklmnopqrstuvwxyz"
    morse= ["01","1000","1010","100", "0", "0010", "110", "0000", "00", "0111", "101", "0100", "11", "10", "111", "0110", "1101", "010", "000", "1", "001", "0001", "011", "1001", "1011", "1100"]

    def error():
        print("error")
        ser.write(chr(32+1))
        def reset():
            ser.write(chr(32))
        later = threading.Timer(1.0, reset, ())
        later.start()
        global timer
        global char
        global last
        timer = time.time()
        char = ""
        last = ""


    def givemeangle(code):
      try:
        return ord(text[morse.index(code)])-ord('a')+1
      except:
        return -1

    #ser.write(chr(givemeangle(c)))

    dotTime = 0.1

    def knoobListener():
      global dotTime
      min = 0.1
      max = 2.0
      ser.write(chr(128+4))
      while True:
        cc = ser.read(1)
        if len(cc)>0:
          result = (((float(ord(cc)) - 64.0)/63.0)*(max-min))+min
          dotTime = result
          print("dotTime "+ str(dotTime))

    knoobListenerThread = threading.Thread(target=knoobListener)
    knoobListenerThread.start()

    timer = time.time()
    char = ""
    last = ""

    def input_signals(what):
      global timer
      global char
      global last

      current_time = time.time()

      def check(time_last):
          print("check")
          print(time.time() - time_last)
          print(3*dotTime)
          if (time.time() - time_last) >= 3*dotTime:
              global timer
              global char
              global last
              a = givemeangle(char)
              if(a==-1):
                error()
              else:
               ser.write(chr(a))
              timer = time.time()
              char = ""
              last = ""


      if what == "1":
        if (last == "1"):
            error()
        last = "1"
        timer = time.time()
        ser.write(chr(64+8))
      else:
        ser.write(chr(64+0))
        if (last == "0"):
            error()
        last = "0"
        if (current_time - timer) <= dotTime:
            char = char.join("0")
        elif (current_time - timer) <= 3*dotTime:
            char = char.join("1")
        check = threading.Timer(3*dotTime, check, (current_time,))
        check.start()

    UDP_IP = "192.168.17.85"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    error()
    while True:
      data, addr = sock.recvfrom(1024)
      print(data)
      if data in ["0","1"]:
        input_signals(data)

    knoobListenerThread.join()


#RUN
import threading
receiverThread = threading.Thread(target=receiver)
receiverThread.start()
receiverThread.join()