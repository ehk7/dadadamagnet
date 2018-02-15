"""
Module containing alarm class, used to trigger the buzzer
"""
import machine
import time

class Alarm:
    def __init__(self):
        """
        Initialise pin output to piezoelectric buzzer
        """
        self.pin=machine.Pin(13, machine.Pin.OUT)

    def beep(self, freq = 1000, t = 5):
        """
        Activates alarm with frequency and duration specified
        :param freq: square wave frequency at which to run the buzzer
        :param t: amount of time to run the buzzer for
        :return: no return value
        """
        for i in range(t*freq):
            self.pin.on()
            time.sleep(1 / (2 * freq))
            self.pin.off()
            time.sleep(1 / (2 * freq))
