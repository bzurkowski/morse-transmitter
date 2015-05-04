from serial import Serial

class Copernicus(Serial):
    
    response = {
        'B1_PR': 128 + 64 + 2 + 1,
        'B1_REL': 128 + 64 + 2,
        'B2_PR': 128 + 64 + 4 + 1,
        'B2_REL': 128 + 64 + 4,
        'KNOB_MIN': 64,
        'KNOB_MAX': 64 + 32 + 16 + 8 + 4 + 2 + 1,
    }
    
    def read(self):
        c = super(Copernicus, self).read(1)

        while len(c) <= 0:
            c = super(Copernicus, self).read(1)
        
        return ord(c)
        
    def write(self, value):
        return super(Copernicus, self).write(chr(value))
        
    def setDashboardAngle(self, val):
        self.write((val))
        
    def setLed(self, on):
        self.write((32 + on))
        
    def autoUpdate(self, button1 = False, button2 = False, knob = False):
        to_send = 128 + \
            (16 if button1 else 0) + \
            (8 if button2 else 0) + \
            (4 if knob else 0)
        self.write(to_send)
        