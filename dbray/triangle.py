class Triangle():

    def __init__(self, v0, v1, v2, normal0, normal1, normal2):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.geometryType = 3
        self.level = 0
        self.normal0 = normal0
        self.normal1 = normal1
        self.normal2 = normal2

    def setLevel(self, level):
        self.level = level

    def toVector(self):
        return [[self.geometryType, self.level, 0.0], self.v0, self.v1,
                self.v2, self.normal0, self.normal1, self.normal2]

    def getNumObjects(self):
        return 1