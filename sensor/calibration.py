from magnetometer import Magnetometer
from utime import sleep_ms
import ujson
import math

class Lock:
    """Takes measurements of magnetometer levels to determine lock status"""
    def __init__(self):
        self.locked=[0,0,0]
        self.closed=[0,0,0]
        self.open=[0,0,0]
        self.locked_dist=0
        self.closed_dist=0
        self.open_dist=0

    def calibrate_locked(self):
        pass

    def calibrate_closed(self):
        pass

    def calibrate_open(self):
        pass

    def get_status(self):
        pass

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
        self.x=[]
        self.y=[]
        self.z=[]
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

    def mean(self):
        if self.x==[] or self.y==[] or self.z==[]:
            print("Take measurement first using measure()")
            return 0

        self.mean_x=sum(self.x)/len(self.x)
        self.mean_y=sum(self.y)/len(self.y)
        self.mean_z=sum(self.z)/len(self.z)

        return (self.mean_x, self.mean_y, self.mean_z)

    def std_dev(self):
        self.mean()

        self.std_z = math.sqrt(sum(map(lambda x: (x - self.mean_x) * (x - self.mean_x), self.z)) / len(self.z))

        self.std_y = math.sqrt(sum(map(lambda x: (x - self.mean_y) * (x - self.mean_y), self.y)) / len(self.y))

        self.std_x = math.sqrt(sum(map(lambda x: (x - self.mean__z) * (x - self.mean__z), self.x)) / len(self.x))

        return (self.std_x,self.std_y,self.std_z)




