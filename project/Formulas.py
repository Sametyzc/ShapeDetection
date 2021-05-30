# this module contains useful equations and objets to calculate the places of the shapes in analytical plane
import numpy as np
import math
from Point import Point

class Formulas:

    CircleEqtuationResult = 1
    @staticmethod
    def CircleEquation(radius, centerPoint, otherPoint):
        valueX = np.power((otherPoint.x - centerPoint.x), 2)
        valueY = np.power((otherPoint.y - centerPoint.y), 2)
        return (valueX + valueY)/np.power(radius, 2)

    EllipseEqtuationResult = 1
    # Ellipse geometric place formula (((x-h)/a)^2)+(((y-k)/)^2) = 1
    @staticmethod
    def EllipseEquation(a, b, centerPoint, otherPoint):
        valueX = np.power((otherPoint.x - centerPoint.x), 2)/np.power(a, 2)
        valueY = np.power((otherPoint.y - centerPoint.y), 2)/np.power(b, 2)
        return valueX + valueY

    RotatedEllipseEqtuationResult = 1
    # Rotated ellipse geometric place formula
    @staticmethod
    def RotatedEllipseEquation(a, b, centerPoint, otherPoint, rotateAngle):
        radian = math.radians(rotateAngle)
        value1 = np.power((otherPoint.x-centerPoint.x)*math.cos(radian) +
                          (otherPoint.y-centerPoint.y)*math.sin(radian), 2)
        value2 = np.power((otherPoint.x-centerPoint.x)*math.sin(radian) -
                          (otherPoint.y-centerPoint.y)*math.cos(radian), 2)
        return (value1/np.power(a, 2)) + (value2/np.power(b, 2))

    @staticmethod
    def DistanceEquation(Point1, Point2):
        if isinstance(Point1, Point) and isinstance(Point2, Point):
            difference_x = np.power(Point1.x - Point2.x, 2)
            difference_y = np.power(Point1.y - Point2.y, 2)
            return np.sqrt(difference_x + difference_y)
        else:
            raise TypeError("Parameters must be type Point")

    @staticmethod
    def AngleEquation(Point1, Point2):
        if isinstance(Point1, Point) and isinstance(Point2, Point):
            if(Point1.y > Point2.y):
                upperPoint = Point1
                lowerPoint = Point2
            else:
                upperPoint = Point2
                lowerPoint = Point1

            value_x = np.abs(upperPoint.x - lowerPoint.x)
            value_y = np.abs(upperPoint.y - lowerPoint.y)

            if(value_x == 0):
                return 90

            result = math.degrees(math.atan(value_y/value_x))

            if(upperPoint.x > lowerPoint.x):
                return result
            else:
                return 180 - result
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

    @staticmethod
    def CenterPointEquation(x, y):
        return (x+y)/2
