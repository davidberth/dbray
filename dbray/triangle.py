class Triangle():

    def __init__(self, v0, v1, v2):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.geometryType = 3
        self.parent = 0

    def setLevel(self, level):
        self.level = level

    def toVector(self):
        return [[self.geometryType, self.level, 0.0], self.v0, self.v1,
                self.v2, [0.0, 0.0, 0.0]]

    def getNumObjects(self):
        return 1