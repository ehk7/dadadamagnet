from magnetometer import Magnetometer
from utime import sleep_ms
from utility import Vector3D
import ujson
import math

class Lock:
    """Takes measurements of magnetometer levels to determine lock status"""
    def __init__(self):
        # self.locked=[0,0,0]
        # self.closed=[0,0,0]
        # self.open=[0,0,0]
        self.locked = Vector3D()
        self.closed = Vector3D()
        self.open = Vector3D()

        self.locked_distance = Vector3D()
        self.closed_distance = Vector3D()
        self.open_distance = Vector3D()

        self.logger=DataLogger()
        self.scale_factor = 20

    def set_scale_factor(self, scale_factor):
        self.scale_factor = scale_factor

    def calibrate_locked(self):
        self.logger.measure(100, 30)
        self.logger.std_dev()

        self.locked = self.logger.data_mean
        self.locked_distance = self.logger.data_std_dev.distance(Vector3D(0,0,0))

    def calibrate_closed(self):
        self.logger.measure(100, 30)
        self.logger.std_dev()
        self.closed=self.logger.data_mean
        self.closed_distance = self.logger.data_std_dev.distance(Vector3D(0, 0, 0))

    def calibrate_open(self):
        self.logger.measure(100, 30)
        self.logger.std_dev()
        self.open=self.logger.data_mean
        self.open_distance = self.logger.data_std_dev.distance(Vector3D(0, 0, 0))

    def is_locked(self):
        self.logger.measure(10, 10)
        meanpos = self.logger.mean()

        if meanpos.distance(self.locked)<self.locked_distance*self.scale_factor:
            return True
        else:
            return False

    def is_closed(self):
        self.logger.measure(10, 10)
        meanpos = self.logger.mean()

        if meanpos.distance(self.closed) < self.closed_distance*self.scale_factor:
            return True
        else:
            return False

    def is_open(self):
        self.logger.measure(10, 10)
        meanpos = self.logger.mean()
        if meanpos.distance(self.closed) < self.closed_distance*self.scale_factor:
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

        self.data=[]

    def measure(self, num_readings, time_ms_per_reading=0):
        self.data=[]
        """time per reading must be more than 7 ms"""
        if(time_ms_per_reading>7):
            time_sleep = time_ms_per_reading-7
            for i in range(num_readings+2):
                self.magnetometer.take_measurement()
                if i>1:
                    vector = Vector3D()
                    vector.x = self.magnetometer.x
                    vector.y = self.magnetometer.y
                    vector.z = self.magnetometer.z
                    self.data.append(vector)
                    sleep_ms(time_sleep)

        else:
            for i in range(num_readings):
                self.magnetometer.take_measurement()
                if i>1:
                    vector = Vector3D()
                    vector.x = self.magnetometer.x
                    vector.y = self.magnetometer.y
                    vector.z = self.magnetometer.z
                    self.data.append(vector)

        if num_readings>=10:
            self.data=self.data[5:]

    def get_json(self):

        return ujson.dumps(self.data)

    def mean(self):
        if self.data==[]:
            print("Take measurement first using measure()")
            return 0
        self.data_mean= Vector3D()
        for i in self.data:
            self.data_mean = self.data_mean + i
        self.data_mean = self.data_mean.mul(1/len(self.data))

        return self.data_mean

    def std_dev(self):
        self.mean()
        res = Vector3D()
        for i in range(len(self.data)):
            res=res+(self.data[i]-self.data_mean)*(self.data[i]-self.data_mean)

        res=res.mul(1/len(self.data))

        res = res.sqrt()

        self.data_std_dev = res
        return res




