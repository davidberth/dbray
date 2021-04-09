class Sphere():

    def __init__(self, center, radius):
        self.setCenter(center)
        self.setRadius(radius)
        self.geometryType = 2
        self.level = 0

    def setCenter(self, center):
        assert len(center) == 3
        self.center = center

    def setRadius(self, radius):
        self.radius = radius

    def setLevel(self, level):
        self.level = level

    def toVector(self):
        return [[self.geometryType, self.level, 0.0], [self.center[0], self.center[1], self.center[2]], [self.radius, 0.0, 0.0],
                [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

    def getNumObjects(self):
        return 1
