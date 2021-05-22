from ShapeDetection import ShapeDetection
import cv2 as cv
import math

image = cv.imread("../examples/images/kare6.png")

cv.imshow("image", image)

image = cv.GaussianBlur(image, (5, 5), 0)

hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
mask1 = cv.inRange(hsv, (0, 50, 50), (10, 255, 255))
mask2 = cv.inRange(hsv, (170, 50, 50), (180, 255, 255))
mask = cv.bitwise_or(mask1, mask2)

#mask = cv.Canny(image,100,300)

sd = ShapeDetection(mask,showWindows=True)
squareList = sd.DetectSquares(10)

for square in squareList:
    cv.circle(image, square.CenterPoint.GetAsTuple(), 3,
                                      (255,120,255), -1, cv.LINE_8)
    print("---------")
    print("Center Point :",square.CenterPoint)
    print("Area :",square.Area)
    print("Longest Side Lenght :",square.LongestSideLenght)
    print("Shortest Side Lenght :",square.ShortestSideLenght)
    print("Rotation Angle :",square.RotationAngle)
    print("---------")

print("Toplam: ", len(squareList))
cv.imshow("result image",image)

cv.waitKey(0)
cv.destroyAllWindows()