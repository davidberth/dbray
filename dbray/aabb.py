class AABB():

    def __init__(self, vmin, vmax):
        self.vmin = vmin
        self.vmax = vmax
        self.geometryType = 4
        self.level = 0

    def toVector(self):
        return [[self.geometryType, self.level, 0.0], self.vmin, self.vmax,
                [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

    def setLevel(self, level):
        self.level = level

    def getNumObjects(self):
        return 1