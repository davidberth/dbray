from dbray.triangle import Triangle
from dbray.aabb import AABB
import numpy as np
# This is a compound geometry type
class Terrain():

    def __init__(self, heightField):
        self.heightField = heightField
        self.geometryType = 6
        self.level = 0
        self.objects = []

        self.quadtree(0, heightField.shape[0]-1, 0, heightField.shape[1]-1, heightField, 0, self.objects)
        self.minvec = [0, np.min(heightField), 0]
        self.maxvec = [heightField.shape[0], np.max(heightField), heightField.shape[1]]

    def quadtree(self, xmin, xmax, ymin, ymax, heightField, level, objects):

        localLevel = level
        oldLevel = level
        hsubset = heightField[xmin:xmax+1, ymin:ymax+1]
        hmax = np.max(hsubset)
        hmin = np.min(hsubset)
        aabb = AABB([xmin, hmin, ymin], [xmax + 1.0, hmax + 0.001, ymax + 1.0])
        objects.append(aabb)
        currentIndex = len(objects) - 1

        halfx = (xmax - xmin)//2
        halfy = (ymax - ymin)//2

        if (xmax - xmin) * (ymax - ymin) < 5:
            # we are at a leaf so we generate terrain geometries

            for x in range(xmin, xmax):
                for y in range(ymin, ymax):
                    v1 = [x, heightField[x,y], y]
                    v2 = [x + 1, heightField[x+1,y], y]
                    v3 = [x, heightField[x,y+1], y + 1]

                    triangle = Triangle(v1, v2, v3)
                    objects.append(triangle)

                    v1 = [x + 1, heightField[x + 1, y], y]
                    v2 = [x + 1, heightField[x + 1, y + 1], y + 1]
                    v3 = [x, heightField[x, y + 1], y + 1]

                    triangle = Triangle(v1, v2, v3)
                    objects.append(triangle)
                    localLevel+=2

        else:
            # need to subdivide further and generate AABBs
            localLevel+= self.quadtree(xmin, xmin + halfx, ymin, ymin + halfy, heightField, level, objects) - oldLevel
            localLevel += self.quadtree(xmin + halfx, xmax, ymin, ymin + halfy, heightField, level, objects) - oldLevel
            localLevel += self.quadtree(xmin, xmin + halfx, ymin + halfy, ymax, heightField, level, objects) - oldLevel
            localLevel += self.quadtree(xmin + halfx, xmax, ymin + halfy, ymax, heightField, level, objects) - oldLevel

        objects[currentIndex].setLevel(localLevel - oldLevel)

        localLevel+=1

        return localLevel

    def getAABB(self):
        return AABB(self.minvec, self.maxvec)

    def setLevel(self, level):
        self.level = level

    def getNumObjects(self):
        return len(self.objects)

