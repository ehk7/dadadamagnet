import machine
import time

class Alarm:
    def __init__(self):
        self.pin=machine.Pin(13, machine.Pin.OUT)

    def beep(self, freq = 1000, t = 5):
        """Activates alarm with frequency specified"""
        for i in range(t*freq):
            self.pin.on()
            time.sleep(1 / (2 * freq))
            self.pin.off()
            time.sleep(1 / (2 * freq))
