from magnetometer import Magnetometer
from utime import sleep_ms
import ujson
import math

class DataLogger:
    """Logs data from the magenetomer for implementing the calibration levels"""
    def __init__(self, magnetometer=None):
        if magnetometer==None:
            self.magnetometer = Magnetometer()
        else:
            self.magnetometer = magnetometer
        self.x=[]
        self.y=[]
        self.z=[]

    def measure(self, num_readings, time_ms_per_reading=0):
        """time per reading must be more than 7 ms"""
        if(time_ms_per_reading>7):
            time_sleep = time_ms_per_reading-7
            for i in range(num_readings+2):
                self.magnetometer.take_measurement()
                if i>1:
                    self.x.append(self.magnetometer.x)
                    self.y.append(self.magnetometer.y)
                    self.z.append(self.magnetometer.z)
                    sleep_ms(time_sleep)

        else:
            for i in range(num_readings):
                self.magnetometer.take_measurement()
                if i>1:
                    self.x.append(self.magnetometer.x)
                    self.y.append(self.magnetometer.y)
                    self.z.append(self.magnetometer.z)

    def get_json(self):
        data["x"]=self.x
        data["y"]=self.y
        data["z"]=self.z

        return ujson.dumps(data)

    def std_dev(self):
        mean = sum(self.z)/len(self.z)
        z = math.sqrt(sum(map(lambda x: (x - mean) * (x - mean), self.z)) / len(self.z))

        mean = sum(self.y) / len(self.y)
        y = math.sqrt(sum(map(lambda x: (x - mean) * (x - mean), self.y)) / len(self.y))

        mean = sum(self.x) / len(self.x)
        x = math.sqrt(sum(map(lambda x: (x - mean) * (x - mean), self.x)) / len(self.x))
        return (x,y,z)




