from request_codes import autoupdate_codes, query_codes
from serial import Serial


class Copernicus(object):

  def __init__(self, port=None, baudrate=9600):
    self.serial = Serial(port, baudrate)

  def read():
    return ord(self.serial.read(1))

  def write(value):
    return self.serial.write(chr(value))

  def set_autoupdates(self, peripheral):
    self.write(autoupdate_codes[peripheral])

  def query(self, peripheral):
    self.write(query_codes[peripheral])

  def set_dashboard_angle(self, angle):
    if 0 <= angle <= 31:
      self.write(angle)
    else:
      ValueError("Dashboard angle out of range (0-31)")

  def reset_dashboard_angle(self):
    self.set_dashboard_angle(0)

  def led_on(self):
    self.write(33)

  def led_off(self):
    self.write(32)
