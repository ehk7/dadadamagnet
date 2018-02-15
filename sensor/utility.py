"""
Module containing Vector3D and Status utility classes
"""
import math

class Status:
    """
    Class used to convert between human readable statuses and numerical codes
    """
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
        """
        Create a new vector
        :param x: x value to use, defaults to 0
        :param y: y value to use, defaults to 0
        :param z: z value to use, defaults to 0
        """
        self.x=x
        self.y=y
        self.z=z


    def dot(self, vector):
        """
        Dot product self and vector
        :param vector: vector calculate the other dot product with
        :return: the dot product
        """
        return (self.x*vector.x+self.y*vector.y+self.z*vector.z)

    def __add__(self, vector):
        """
        Overloaded add operation operator, simply add the respective components
        :param vector: vector add
        :return: the sum
        """
        res = Vector3D()
        res.x=vector.x+self.x
        res.y=vector.y+self.y
        res.z=vector.z+self.z
        return res

    def mul(self,scalar):
        """
        Multiplication of vector by scalar
        :param scalar: scalar value to multiply by
        :return: the product
        """
        res = Vector3D()
        res.x = self.x*scalar
        res.y = self.y*scalar
        res.z = self.z*scalar
        return res

    def __sub__(self, other):
        """
        Subtraction operator overloaded to support vector subtraction
        :param other: subtracts the vector form self
        :return: the result
        """
        return (self+other.mul(-1))

    def __mul__(self, other):
        """
        Hadamard product of self and other
        :param other: the other vector to calulate the Hadamard product with
        :return: the result of the calculation
        """
        return Vector3D(self.x*other.x, self.y*other.y, self.z*other.z)

    def __str__(self):
        """
        Support for easy printing and conversion to string
        :return: a string representation of the vector
        """
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"

    def sqrt(self):
        """
        Takes the square root of each component of the vector (Hadamard square root)
        :return: the square root
        """
        res = Vector3D(self.x,self.y,self.z)
        res.x=math.sqrt(res.x)
        res.y=math.sqrt(res.y)
        res.z=math.sqrt(res.z)
        return res

    def distance(self, other):
        """
        Calculates the distance (magnitude of the difference) between two vectors
        :param other: the other vector to calculate the distance from
        :return: scalar result
        """
        res = self-other
        res= res.dot(res)
        return (math.sqrt(res))
