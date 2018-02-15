from magnetometer import Magnetometer
from utime import sleep_ms
from utility import Vector3D
import ujson
import math
from utility import Status

status = Status()

class Lock:
    """Takes measurements of magnetometer levels to determine lock status"""
    def __init__(self):
        """
        Contruct a new Lock object (akes no parameters)
        """
        self.locked = Vector3D()
        self.closed = Vector3D()
        self.open = Vector3D()

        self.locked_distance = Vector3D()
        self.closed_distance = Vector3D()
        self.open_distance = Vector3D()

        self.logger=DataLogger()
        self.scale_factor = 20


    def set_scale_factor(self, scale_factor):
        """
        Set the scale factor
        :param scale_factor: the factor by which the standard deviation is multiplied to get the scale factor
        :return: no return value
        """
        self.scale_factor = scale_factor

    def calibrate_locked(self):
        """
        Takes measurements that will used to determine whether the lock is in a locked state
        :return: no return value
        """
        self.logger.measure(20, 30)
        self.logger.std_dev()

        self.locked = self.logger.data_mean
        self.locked_distance = self.logger.data_std_dev.distance(Vector3D(0,0,0))

    def calibrate_closed(self):
        """
        Takes measurements that will used to determine whether the lock is in a closed and unlocked state
        :return: no return value
        """
        self.logger.measure(20, 30)
        self.logger.std_dev()
        self.closed=self.logger.data_mean
        self.closed_distance = self.logger.data_std_dev.distance(Vector3D(0, 0, 0))

    def calibrate_open(self):
        """
        Takes measurements that will used to determine whether the door is open state
        :return: no return value
        """
        self.logger.measure(20, 30)
        self.logger.std_dev()
        self.open=self.logger.data_mean
        self.open_distance = self.logger.data_std_dev.distance(Vector3D(0, 0, 0))

    def is_locked(self):
        """
        Tests whether the door is locked
        :return: True is locked, False is not
        """
        self.logger.measure(10, 10)
        meanpos = self.logger.mean()

        if meanpos.distance(self.locked)<self.locked_distance*self.scale_factor:
            return True
        else:
            return False

    def is_closed(self):
        """
        Tests whether the door is closed and unlocked
        :return: True if closed and unlocked, False otherwise
        """
        self.logger.measure(10, 10)
        meanpos = self.logger.mean()

        if meanpos.distance(self.closed) < self.closed_distance*self.scale_factor:
            return True
        else:
            return False

    def is_open(self):
        """
        Tests whether the door is open
        :return: True if open, Fale otherwise
        """
        self.logger.measure(10, 10)
        meanpos = self.logger.mean()
        if meanpos.distance(self.closed) < self.closed_distance*self.scale_factor:
            return True
        else:
            return False

    def get_status(self):
        """
        Get the status of the lock
        :return: integer status code, according to the Status class
        """
        if self.is_locked():
            return status.getStatusCode("LOCKED")
        elif self.is_closed():
            return status.getStatusCode("CLOSED")
        else:
            return status.getStatusCode("OPEN")




class DataLogger:
    """
    Logs data from the magenetometer
    """
    def __init__(self, magnetometer=None):
        """
        Creates a DataLogger instance, optionally uses a Magnetometer instance if given, otherwises creates a new
        instance
        :param magnetometer: the optional magnetometer instance it will use to record data
        """
        if magnetometer==None:
            self.magnetometer = Magnetometer()
        else:
            self.magnetometer = magnetometer

        self.data=[]

    def measure(self, num_readings, time_ms_per_reading=0):
        """
        Takes reading from the magnetometer and scales to the correct units
        :param num_readings: number of readings to take
        :param time_ms_per_reading: time to spend taking each reading
        :return: no return value
        """
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
        """
        Converts recorded magnetometer data to JSON
        :return: JSON object containing magnetometer readings
        """
        return ujson.dumps(self.data)

    def mean(self):
        """
        Calculates the mean of the recorded data
        :return: Vector3D instance of the mean value recorded in each axis
        """
        if self.data==[]:
            print("Take measurement first using measure()")
            return 0
        self.data_mean= Vector3D()
        for i in self.data:
            self.data_mean = self.data_mean + i
        self.data_mean = self.data_mean.mul(1/len(self.data))

        return self.data_mean

    def std_dev(self):
        """
        Calculate the standard deviation of the recorded data
        :return: Vector3D instance of the std deviation value recorded in each axis
        """
        self.mean()
        res = Vector3D()
        for i in range(len(self.data)):
            res=res+(self.data[i]-self.data_mean)*(self.data[i]-self.data_mean)

        res=res.mul(1/len(self.data))

        res = res.sqrt()

        self.data_std_dev = res
        return res




