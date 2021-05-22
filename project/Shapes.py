from Point import Point

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
