from Formulas import Formulas

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

