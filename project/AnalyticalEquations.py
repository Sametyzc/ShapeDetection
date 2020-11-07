import numpy as np

# this module contains useful equations and objets to calculate the places of the shapes in analytical plane


class Formulas:

    CircleEqtuationResult = 1
    @staticmethod
    def CircleEquation(radius, centerPoint, otherPoint):
        valueX = np.power((otherPoint.x - centerPoint.x), 2)
        valueY = np.power((otherPoint.y - centerPoint.y), 2)
        return (valueX + valueY)/np.power(radius, 2)

    @staticmethod
    def DistanceEquation(Point1, Point2):
        if isinstance(Point1, Point) and isinstance(Point2, Point):
            difference_x = np.power(Point1.x - Point2.x, 2)
            difference_y = np.power(Point1.y - Point2.y, 2)
            return np.sqrt(difference_x + difference_y)
        else:
            raise TypeError("Parameters must be type Point")

    @staticmethod
    def PercentageErrorEquation(ExactValue, ApproximateValue):
        if(ExactValue == ApproximateValue):
            return 0
        if(ExactValue == 0):
            raise ZeroDivisionError("ExactValue is zero!")
        value = np.abs(ExactValue - ApproximateValue)
        return (value/ExactValue)*100


class Point:    
    """
    A class used to represent a 2D Point
    ...

    Attributes
    ----------
    x : float
        x value of the point
    y : float
        y value of the point
    Methods
    -------
    GetAsTuple()
        returns the tuple which is representing the point
    """

    def __init__(self, x, y):
        """init function

        Args:
            x (float): x value of the point
            y ([float]): y value of the point
        """
        self.x = x
        self.y = y

    def __str__(self):
        return str.format("({0}, {1})", self.x, self.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def GetAsTuple(self):
        """Gets the distance between given points

        Returns
        -------
        Tuple
            Returns the tuple which is representing the point. First value is x.
        """
        return (self.x, self.y)

    def GetDistance(self, other):
        """Gets the distance between given points

        Parameters
        ----------
        other : Point
            The point which is in 2D plane
        Returns
        -------
        float
            Distance value between given point and self
        """
        return Formulas.DistanceEquation(self, other)
