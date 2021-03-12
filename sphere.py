import numpy as np
from numba import jit

@jit(nopython=True)
def intersect(O, D, sphere):
    r = sphere[3]
    CO = O - sphere[:3]

    a = np.dot(D, D)
    b = 2*np.dot(CO, D)
    c = np.dot(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return np.inf, np.inf

    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)
    return t1, t2

class Sphere:

    def __init__(self, center, radius):
        self.setCenter(center)
        self.setRadius(radius)

    def setCenter(self, center):
        assert len(center) == 3
        self.center = center

    def setRadius(self, radius):
        self.radius = radius

    def toVector(self):
        return [[self.center[0], self.center[1], self.center[2]], [self.radius, 0.0, 0.0]]
