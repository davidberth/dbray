class Plane():

    def __init__(self, origin, normal):
        self.setOrigin(origin)
        self.setNormal(normal)
        self.geometryType = 1

    def setOrigin(self, origin):
        assert len(origin) == 3
        self.origin = origin

    def setNormal(self, normal):
        assert len(normal) == 3
        self.normal = normal

    def toVector(self):
        return [[self.geometryType, 0.0, 0.0], [self.origin[0], self.origin[1], self.origin[2]],
                [self.normal[0], self.normal[1], self.normal[2]], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
