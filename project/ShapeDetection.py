import cv2 as cv
import numpy as np
import math


class ShapeDetection:

    def __init__(self, grayImage, showWindows=False):
        self.ImageIsGray(grayImage)
        self.showWindows = showWindows
        self.grayImage = grayImage

        if self.showWindows:
            self.resultImage = cv.cvtColor(grayImage, cv.COLOR_GRAY2BGR)
            self.drawingColor = (255, 0, 255)
            self.drawingThicknessLine = 1
            self.drawingThicknessCircle = 2

        self.SetContours()

    def ImageIsGray(self, img):
        """Check if image is gray scale or not. 

        Args:
            img : image to check

        Raises:
            TypeError: If image is not gray scale raise a TypeError.

        Returns:
            bool: If image is gray scale return True.
        """
        if len(img.shape) < 3:
            return True

        if img.shape[2] == 1:
            return True

        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]

        if (b == g).all() and (b == r).all():
            return True

        raise TypeError("grayImage must be gray scale!")
    
    def SetContours(self):
        """
        Find contours in given image and show them if showWindows is true
        """
        self.contours, _ = cv.findContours(
            self.grayImage, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        if self.showWindows:
            cv.imshow("Gray Image", self.grayImage)
            cv.drawContours(self.resultImage, self.contours, -
                            1, self.drawingColor, thickness=self.drawingThicknessLine)
            cv.imshow("Contours", self.resultImage)

    def DetectCircles(self, validRadiusError=10):
        """Find circles in the given image and show steps if showWindows is true

        Args:
            validRadiusError (int, optional): Valid error rate between the max and min radius. Can detect non-circular shapes if the error is too large. Defaults to 10.

        Returns:
            List: A list contains all the circles in the image.
        """
        circleList = []

        for contour in self.contours:
            area = cv.contourArea(contour)
            if(area > 50):
                M = cv.moments(contour)

                if(M["m00"] == 0):
                    continue

                m10 = int(M["m10"])
                m01 = int(M["m01"])
                m00 = int(M["m00"])

                centerX = int(m10 / m00)
                centerY = int(m01 / m00)
                centerPoint = Point(centerX, centerY)

                if self.showWindows:
                    cv.circle(self.resultImage, centerPoint.GetAsTuple(),
                              self.drawingThicknessCircle, self.drawingColor, -1, cv.LINE_8)

                firstPoint = contour[0]
                otherPoint = Point(firstPoint[0][0], firstPoint[0][1])
                distance = centerPoint.GetDistance(otherPoint)
                nearestPoint = otherPoint
                furthestPoint = otherPoint
                minDistance = distance
                maxDistance = distance

                for point in contour:
                    otherPoint = Point(point[0][0], point[0][1])
                    distance = centerPoint.GetDistance(otherPoint)

                    if(distance < minDistance):
                        minDistance = distance
                        nearestPoint = otherPoint

                    if(distance > maxDistance):
                        maxDistance = distance
                        furthestPoint = otherPoint

                if(maxDistance == 0 or minDistance == 0):
                    continue

                if(Formulas.PercentageErrorEquation(maxDistance, minDistance) <= validRadiusError):
                    newCircle = Circle(centerPoint, area,
                                       minDistance, maxDistance)
                    circleList.append(newCircle)

                    if self.showWindows:
                        cv.line(self.resultImage, centerPoint.GetAsTuple(), nearestPoint.GetAsTuple(
                        ), (255, 0, 0), self.drawingThicknessLine, cv.LINE_AA)
                        cv.line(self.resultImage, centerPoint.GetAsTuple(), furthestPoint.GetAsTuple(
                        ), (0, 0, 255), self.drawingThicknessLine, cv.LINE_AA)
               
        if self.showWindows:
            cv.imshow("Result", self.resultImage)
        return circleList

    def DetectEllipses(self, validPoint=90, validEquationError=15):
        """Find ellipses in the given image and show steps if showWindows is true

        Args:
            validPoint (int, optional): Percentage of all pixels count of the contour to valid pixels count. Defaults to 90.
            validEquationError (int, optional): Percentage error of the value that should be to pixels equation result. Defaults to 15.

        Returns:
            [type]: [description]
        """
        ellipseList = []

        for contour in self.contours:
            area = cv.contourArea(contour)
            if(area > 50):
                M = cv.moments(contour)

                if(M["m00"] == 0):
                    continue

                m10 = int(M["m10"])
                m01 = int(M["m01"])
                m00 = int(M["m00"])

                centerX = int(m10 / m00)
                centerY = int(m01 / m00)
                centerPoint = Point(centerX, centerY)

                if self.showWindows:
                    cv.circle(self.resultImage, centerPoint.GetAsTuple(),
                              self.drawingThicknessCircle, self.drawingColor, -1, cv.LINE_8)

                firstPoint = contour[0]
                otherPoint = Point(firstPoint[0][0], firstPoint[0][1])
                distance = centerPoint.GetDistance(otherPoint)
                nearestPoint = otherPoint
                furthestPoint = otherPoint
                minDistance = distance
                maxDistance = distance

                for point in contour:
                    otherPoint = Point(point[0][0], point[0][1])
                    distance = centerPoint.GetDistance(otherPoint)

                    if(distance < minDistance):
                        minDistance = distance
                        nearestPoint = otherPoint

                    if(distance > maxDistance):
                        maxDistance = distance
                        furthestPoint = otherPoint

                if(maxDistance == 0 or minDistance == 0):
                    continue

                if self.showWindows:
                    cv.line(self.resultImage, centerPoint.GetAsTuple(), nearestPoint.GetAsTuple(
                    ), (255, 0, 0), self.drawingThicknessLine, cv.LINE_AA)
                    cv.line(self.resultImage, centerPoint.GetAsTuple(), furthestPoint.GetAsTuple(
                    ), (0, 0, 255), self.drawingThicknessLine, cv.LINE_AA)

                if(np.abs(centerPoint.x-nearestPoint.x) < np.abs(centerPoint.x-furthestPoint.x)):
                    b = minDistance
                    bPoint = nearestPoint
                    a = maxDistance
                    aPoint = furthestPoint
                else:
                    b = maxDistance
                    bPoint = furthestPoint
                    a = minDistance
                    aPoint = nearestPoint

                angle = centerPoint.GetAngle(aPoint)

                allPointsNumber = len(contour)

                validPointsCount = 0
                validPointsNumber = (
                    allPointsNumber*validPoint)/100

                NoneValidPointsCount = 0
                NoneValidPointsCountLimit = allPointsNumber-validPointsNumber

                for point in contour:
                    otherPoint = Point(point[0][0], point[0][1])

                    result = Formulas.RotatedEllipseEquation(
                        a, b, centerPoint, otherPoint, angle)

                    error = Formulas.PercentageErrorEquation(
                        Formulas.EllipseEqtuationResult, result)

                    if(error < validEquationError):
                        if self.showWindows:
                            cv.circle(self.resultImage, otherPoint.GetAsTuple(), self.drawingThicknessCircle,
                                      self.drawingColor, -1, cv.LINE_8)

                        validPointsCount += 1
                    else:
                        if self.showWindows:
                            cv.circle(self.resultImage, otherPoint.GetAsTuple(), self.drawingThicknessCircle,
                                      (0, 0, 0), -1, cv.LINE_8)
                        NoneValidPointsCount += 1

                    if(validPointsNumber <= validPointsCount):
                        newEllipse = Ellipse(
                            centerPoint, area, maxDistance, minDistance, angle)
                        ellipseList.append(newEllipse)
                        break

                    if(NoneValidPointsCountLimit <= NoneValidPointsCount):
                        break
        if self.showWindows:
            cv.imshow("Result", self.resultImage)
        return ellipseList

    def DetectSquares(self, validError = 10):

        squareList = []

        for contour in self.contours:
            area = cv.contourArea(contour)
            if(area > 50):
                M = cv.moments(contour)

                if(M["m00"] == 0):
                    continue

                m10 = int(M["m10"])
                m01 = int(M["m01"])
                m00 = int(M["m00"])

                centerX = int(m10 / m00)
                centerY = int(m01 / m00)
                centerPoint = Point(centerX, centerY)

                approx = cv.approxPolyDP(contour, 0.01* cv.arcLength(contour, True), True)

                pointFirstCorner = Point(approx[0][0][0],approx[0][0][1])
                pointSecondCorner = Point(approx[1][0][0],approx[1][0][1])
                pointThirdCorner = Point(approx[2][0][0],approx[2][0][1])
                pointFourthCorner = Point(approx[3][0][0],approx[3][0][1])
                sideCenterPoint = pointFirstCorner.GetCenter(pointSecondCorner)

                sideLenght1 = Point.GetDistance(pointFirstCorner,pointSecondCorner)
                sideLenght2 = Point.GetDistance(pointSecondCorner,pointThirdCorner)
                sideLenght3 = Point.GetDistance(pointThirdCorner,pointFourthCorner)
                sideLenght4 = Point.GetDistance(pointFourthCorner,pointFirstCorner)
                sideLenghts = [sideLenght1, sideLenght2, sideLenght3, sideLenght4]

                shortestSideLenght = Helper.FindMinElement(sideLenghts)
                longestSideLenght = Helper.FindMaxElement(sideLenghts)

                if (Formulas.PercentageErrorEquation(1, (sideLenghts[0]/sideLenghts[1])) <= validError 
                    and Formulas.PercentageErrorEquation(1, (sideLenghts[1]/sideLenghts[2])) <= validError 
                    and Formulas.PercentageErrorEquation(1, (sideLenghts[2]/sideLenghts[3])) <= validError 
                    and Formulas.PercentageErrorEquation(1, (sideLenghts[3]/sideLenghts[1])) <= validError ):
                
                    rotationAngle = Formulas.AngleEquation(centerPoint, sideCenterPoint)
                    
                    if self.showWindows:
                        cv.circle(self.resultImage, centerPoint.GetAsTuple(),
                                self.drawingThicknessCircle, self.drawingColor, -1, cv.LINE_8)
                        cv.circle(self.resultImage, sideCenterPoint.GetAsTuple(),
                                self.drawingThicknessCircle, self.drawingColor, -1, cv.LINE_8)

                    newSqaure = Square(centerPoint,area,shortestSideLenght,longestSideLenght,rotationAngle)
                    squareList.append(newSqaure)

                    if self.showWindows:
                        cv.line(self.resultImage, centerPoint.GetAsTuple(), pointFirstCorner.GetAsTuple(), (255, 0, 0), self.drawingThicknessLine, cv.LINE_AA)
                        cv.line(self.resultImage, centerPoint.GetAsTuple(), sideCenterPoint.GetAsTuple(), (0, 0, 255), self.drawingThicknessLine, cv.LINE_AA)
        if self.showWindows:
            cv.imshow("Result", self.resultImage)
        return squareList

# this module contains useful equations and objets to calculate the places of the shapes in analytical plane

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

class Helper:
    @staticmethod
    def FindMaxElement(Array):
        maxElement = Array[0]
        for element in Array:
            if maxElement < element:
                maxElement = element

        return maxElement

    @staticmethod
    def FindMinElement(Array):
        minElement = Array[0]
        for element in Array:
            if minElement > element:
                minElement = element

        return minElement

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

    def GetAngle(self, other):
        """Gets the angle between given points

        Parameters
        ----------
        other : Point
            The point which is in 2D plane
        Returns
        -------
        float
            angle value between given point and self
        """
        return Formulas.AngleEquation(self, other)

    def GetCenter(self, other):
        """Gets the center point between given points

        Parameters
        ----------
        other : Point
            The point which is in 2D plane
        Returns
        -------
        Point
            center point in given points
        """
        return Point(int(Formulas.CenterPointEquation(self.x, other.x)),
                    int(Formulas.CenterPointEquation(self.y, other.y)))

class Circle:
    def __init__(self, CenterPoint=Point(0, 0), Area=0, ShortRadius=0, LongRadius=0):
        self.CenterPoint = CenterPoint
        self.Area = Area
        self.LongRadius = LongRadius
        self.ShortRadius = ShortRadius
        self.Radius = (self.ShortRadius+self.LongRadius)/2

    def __str__(self):
        result = "-------------------------------------"
        result += "\n            Circle               "
        result += "\nCenterPoint = "+str(self.CenterPoint)
        result += "\nArea = "+str(self.Area)
        result += "\nRadius = "+str(self.Radius)
        result += "\n-------------------------------------"
        return result

class Ellipse:
    def __init__(self, CenterPoint=Point(0, 0), Area=0, LongRadius=0, ShortRadius=0, RotationAngle=0):
        self.CenterPoint = CenterPoint
        self.Area = Area
        self.RotationAngle = RotationAngle
        self.LongRadius = LongRadius
        self.ShortRadius = ShortRadius

    def __str__(self):
        result = "-------------------------------------"
        result += "\n            Ellipse               "
        result += "\nCenterPoint = "+str(self.CenterPoint)
        result += "\nArea = "+str(self.Area)
        result += "\nLongRadius = "+str(self.LongRadius)
        result += "\nShortRadius = "+str(self.ShortRadius)
        result += "\nRotationAngle = "+str(self.RotationAngle)
        result += "\n-------------------------------------"
        return result

class Square:
    def __init__(self, CenterPoint=None, Area=0, ShortestSideLenght=0, LongestSideLenght=0, RotationAngle=0):
        self.CenterPoint = CenterPoint
        self.Area = Area
        self.ShortestSideLenght = ShortestSideLenght
        self.LongestSideLenght = LongestSideLenght
        self.RotationAngle = RotationAngle

    def __str__(self):
        result = "-------------------------------------"
        result += "\n            Square               "
        result += "\nCenterPoint = "+str(self.CenterPoint)
        result += "\nArea = "+str(self.Area)
        result += "\nLongestSide = "+str(self.LongestSideLenght)
        result += "\nShortestSide = "+str(self.ShortestSideLenght)
        result += "\nRotationAngle = "+str(self.RotationAngle)
        result += "\n-------------------------------------"
        return result