from AnalyticalEquations import Point, Formulas
import Shapes
from ShapeDetection import ShapeDetection
import cv2 as cv




image = cv.imread("./examples/images/red-circles.png")

cv.imshow("image", image)
cv.waitKey(0)

image = cv.GaussianBlur(image, (5, 5), 0)

hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
mask1 = cv.inRange(hsv, (0, 100, 95), (5, 255, 255))
mask2 = cv.inRange(hsv, (170, 100, 95), (180, 255, 255))
mask = cv.bitwise_or(mask1, mask2)

mask = cv.medianBlur(mask, 9)

sd = ShapeDetection(mask)
circleList = sd.DetectCircles()  

for circle in circleList:
    print("---------")
    print("Center Point :",circle.CenterPonit)
    print("Area :",circle.Area)
    print("Radius :",circle.Radius)
    print("---------")