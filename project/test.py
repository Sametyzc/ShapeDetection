from ShapeDetection import *
import cv2 as cv

"""
image = cv.imread("./examples/images/image2.png")

cv.imshow("image", image)

image = cv.GaussianBlur(image, (5, 5), 0)

hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
mask1 = cv.inRange(hsv, (0, 100, 95), (5, 255, 255))
mask2 = cv.inRange(hsv, (170, 100, 95), (180, 255, 255))
mask = cv.bitwise_or(mask1, mask2)

mask = cv.medianBlur(mask, 9)


mask = cv.Canny(image,100,300)

sd = ShapeDetection(mask, showWindows=True)
circleList = sd.DetectCircles(15)

for circle in circleList:
    print("---------")
    print("Center Point :",circle.CenterPoint)
    print("Area :",circle.Area)
    print("ShortRadius :",circle.ShortRadius)
    print("LongRadius :",circle.LongRadius)
    print("AverageRadius :",circle.AverageRadius)
    print("---------")

cv.waitKey(0)
"""
p1 = Point(20, 20)
p2 = Point(23, 24)
print("Angle in degree:", p1.GetAngle(p2))