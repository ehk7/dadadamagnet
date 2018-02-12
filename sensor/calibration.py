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

        self.locked_distance=0
        self.closed_distance=0
        self.open_distance=0

        self.logger=DataLogger()

    def calibrate_locked(self):
        self.logger.measure(10, 100)
        self.logger.std_dev()
        self.locked=[self.logger.mean_x, self.logger.mean_y, self.logger.mean_z]
        self.locked_distance = 10*(math.sqrt(self.logger.std_x * self.logger.std_x
                                            + self.logger.std_y * self.logger.std_y
                                            + self.logger.std_z * self.logger.std_z))

    def calibrate_closed(self):
        self.logger.measure(10, 100)
        self.logger.std_dev()
        self.closed=[self.logger.mean_x, self.logger.mean_y, self.logger.mean_z]
        self.closed_distance = 10*(math.sqrt(self.logger.std_x * self.logger.std_x
                                            + self.logger.std_y * self.logger.std_y
                                            + self.logger.std_z * self.logger.std_z))

    def calibrate_open(self):
        self.logger.measure(10, 100)
        self.logger.std_dev()
        self.open=[self.logger.mean_x, self.logger.mean_y, self.logger.mean_z]
        self.open_distance = 10*math.sqrt(self.logger.std_x**2
                                            + self.logger.std_y**2
                                            + self.logger.std_z**2)

    def is_locked(self):
        self.logger.measure(10, 10)
        (x,y,z) = self.logger.mean()
        distance = (self.locked[0]-x)**2 + (self.locked[1]-y)**2+(self.locked[2]-z)**2
        if distance<self.locked_distance:
            return True
        else:
            return False

    def is_closed(self):
        self.logger.measure(10, 10)
        (x,y,z) = self.logger.mean()
        distance = (self.closed[0]-x)**2 + (self.closed[1]-y)**2+(self.closed[2]-z)**2
        if distance<self.closed_distance:
            return True
        else:
            return False

    def is_open(self):
        self.logger.measure(10, 10)
        (x,y,z) = self.logger.mean()
        distance = (self.open[0]-x)**2 + (self.open[1]-y)**2+(self.open[2]-z)**2
        if distance<self.open_distance:
            return True
        else:
            return False

    def get_status(self):
        if self.is_locked():
            return 1
        elif self.is_closed():
            return 2
        else:
            return 3




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

        self.std_x = math.sqrt(sum(map(lambda x: (x - self.mean_z) * (x - self.mean_z), self.x)) / len(self.x))

        return (self.std_x,self.std_y,self.std_z)




