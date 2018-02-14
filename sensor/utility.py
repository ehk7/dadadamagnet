import math
from enum import Enum

class Status(Enum):
    UNCALIBRATED = 1
    CALIBRATING = 2
    LOCKED = 3
    CLOSED = 4
    OPEN = 5


class Vector3D:
    """Class respresenting 3d vectors"""
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z


    def dot(self, vector):
        return (self.x*vector.x+self.y*vector.y+self.z*vector.z)

    def __add__(self, vector):
        res = Vector3D()
        res.x=vector.x+self.x
        res.y=vector.y+self.y
        res.z=vector.z+self.z
        return res

    def mul(self,scalar):
        res = Vector3D()
        res.x = self.x*scalar
        res.y = self.y*scalar
        res.z = self.z*scalar
        return res

    def __sub__(self, other):
        return (self+other.mul(-1))

    def __mul__(self, other):
        return Vector3D(self.x*other.x, self.y*other.y, self.z*other.z)

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"

    def sqrt(self):
        res = Vector3D(self.x,self.y,self.z)
        res.x=math.sqrt(res.x)
        res.y=math.sqrt(res.y)
        res.z=math.sqrt(res.z)
        return res

    def distance(self, other):
        res = self-other
        res= res.dot(res)
        return (math.sqrt(res))
