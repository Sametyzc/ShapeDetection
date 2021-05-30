import cv2 as cv
import numpy as np
from Formulas import Formulas
from Point import Point
from Shapes import Circle, Ellipse, Square

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

                sideLenght1 = pointFirstCorner.GetDistance(pointSecondCorner)
                sideLenght2 = pointSecondCorner.GetDistance(pointThirdCorner)
                sideLenght3 = pointThirdCorner.GetDistance(pointFourthCorner)
                sideLenght4 = pointFourthCorner.GetDistance(pointFirstCorner)
                sideLenghts = [sideLenght1, sideLenght2, sideLenght3, sideLenght4]

                shortestSideLenght = min(sideLenghts)
                longestSideLenght = max(sideLenghts)

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