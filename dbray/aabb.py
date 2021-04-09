class AABB():

    def __init__(self, vmin, vmax):
        self.vmin = vmin
        self.vmax = vmax
        self.geometryType = 4
        self.parent = 0

    def toVector(self):
        return [[self.geometryType, self.parent, 0.0], self.vmin, self.vmax,
                [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

    def getNumObjects(self):
        return 1