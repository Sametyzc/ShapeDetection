import cv2 as cv
from Shapes import Circle
from AnalyticalEquations import Point, Formulas
import numpy as np


class ShapeDetection:
    def __init__(self, grayImage, showWindows=False):
        self.ImageIsGray(grayImage)

        self.showWindows = showWindows
        self.grayImage = grayImage

        self.SetEdgesAndContours()

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

    def SetEdgesAndContours(self):
        self.edges = cv.Canny(self.grayImage, 100, 300)

        if self.showWindows:
            cv.imshow("edges", edges)
            cv.waitKey(0)

        self.contours, hierarchy = cv.findContours(
            self.edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    def DetectCircles(self, validError=90):
        edges = self.edges.copy()
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

                cv.circle(edges, centerPoint.GetAsTuple(), 3, (255, 255, 255), -1, cv.LINE_8)
                cv.imshow("center point", edges)
                cv.waitKey(0)

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

                value = Formulas.PercentageErrorEquation(
                    maxDistance, minDistance)

                if(Formulas.PercentageErrorEquation(maxDistance, minDistance) >= 10):
                    continue

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

                avarageRadiuse = (b+a)/2

                allPointsNumber = len(contour)

                validPointsCount = 0
                validPointsNumber = (
                    allPointsNumber*validError)/100

                NoneValidPointsCount = 0
                NoneValidPointsCountLimit = allPointsNumber-validPointsNumber

                for point in contour:
                    otherPoint = Point(point[0][0], point[0][1])

                    result = Formulas.CircleEquation(
                        avarageRadiuse, centerPoint, otherPoint)

                    error = Formulas.PercentageErrorEquation(
                        Formulas.CircleEqtuationResult, result)

                    if(error < 15):
                        """
                        cv.circle(edges, (x, y), 1,
                                  (255, 255, 0), -1, cv.LINE_8)
                        """
                        validPointsCount += 1
                    else:
                        """
                        cv.circle(edges, (x, y), 1, (0, 0, 0), -1, cv.LINE_8)
                        """
                        NoneValidPointsCount += 1

                    if(validPointsNumber <= validPointsCount):
                        newCircle = Circle(centerPoint, area, avarageRadiuse)
                        circleList.append(newCircle)
                        break
                    if(NoneValidPointsCountLimit <= NoneValidPointsCount):
                        break

        return circleList
