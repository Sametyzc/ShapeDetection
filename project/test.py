from ShapeDetection import *
import cv2 as cv
import math

image = cv.imread("./examples/images/ellipses.png")

cv.imshow("image", image)

image = cv.GaussianBlur(image, (5, 5), 0)

hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
mask1 = cv.inRange(hsv, (0, 50, 50), (10, 255, 255))
mask2 = cv.inRange(hsv, (170, 50, 50), (180, 255, 255))
mask = cv.bitwise_or(mask1, mask2)

#mask = cv.Canny(image,100,300)

sd = ShapeDetection(mask,showWindows=True)
ellipseList = sd.DetectCircle()

for ellipse in ellipseList:
    cv.circle(image, ellipse.CenterPoint.GetAsTuple(), 3,
                                      (255,120,255), -1, cv.LINE_8)
    print("---------")
    print("Center Point :",ellipse.CenterPoint)
    print("Area :",ellipse.Area)
    print("LongRadius :",ellipse.LongRadius)
    print("AverageRadius :",ellipse.ShortRadius)
    print("RotationAngle :",ellipse.RotationAngle)
    print("---------")

print("Toplam: ", len(ellipseList))
cv.imshow("result image",image)
cv.waitKey(0)
a = Point(10,10)
b = Point(0,0)
print("aci: ", b.GetAngle(a))