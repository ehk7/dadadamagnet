import math

class Status:
    def getStatusCode(self, statusName):
        if statusName == "UNCALIBRATED":
            return 1
        elif statusName == "CALIBRATING":
            return 2
        elif statusName == "LOCKED":
            return 3
        elif statusName == "CLOSED":
            return 4
        elif statusName == "OPEN":
            return 5


class Vector3D:
    """Class respresenting 3d vectors,"""
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z


    def dot(self, vector):
        """dot product self and vector"""
        return (self.x*vector.x+self.y*vector.y+self.z*vector.z)

    def __add__(self, vector):
        """overloaded add operation operator, simply add the respective components"""
        res = Vector3D()
        res.x=vector.x+self.x
        res.y=vector.y+self.y
        res.z=vector.z+self.z
        return res

    def mul(self,scalar):
        """multiplication of vector by scalar"""
        res = Vector3D()
        res.x = self.x*scalar
        res.y = self.y*scalar
        res.z = self.z*scalar
        return res

    def __sub__(self, other):
        """subtraction operator overloaded to support vector subtraction"""
        return (self+other.mul(-1))

    def __mul__(self, other):
        """Hadamard product"""
        return Vector3D(self.x*other.x, self.y*other.y, self.z*other.z)

    def __str__(self):
        """Support for easy printing and conversion to string"""
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"

    def sqrt(self):
        """Takes the square root of each component of the vector"""
        res = Vector3D(self.x,self.y,self.z)
        res.x=math.sqrt(res.x)
        res.y=math.sqrt(res.y)
        res.z=math.sqrt(res.z)
        return res

    def distance(self, other):
        """Calculates the distance (magnitude of the difference) between two vectors"""
        res = self-other
        res= res.dot(res)
        return (math.sqrt(res))
