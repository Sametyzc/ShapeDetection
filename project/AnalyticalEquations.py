import numpy as np

# this module contains useful equations and objets to calculate the places of the shapes in analytical plane


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
        difference_x = np.power(self.x - other.x, 2)
        difference_y = np.power(self.y - other.y, 2)
        return np.sqrt(difference_x + difference_y)
    