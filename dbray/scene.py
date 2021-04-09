from dbray import sphere
from dbray import plane
from dbray import triangle
from dbray import aabb
from dbray import material
from dbray import extpolygon

import numpy as np
import random
import math

class Scene:

    def __init__(self):

        self.objects = []
        self.materials = []

    def addObject(self, object, pmaterial):
        print (f'adding object {object.toVector()} with material {pmaterial.toVector()}')
        self.objects.append(object)
        self.materials.append(pmaterial)

    def getNumObjects(self):
        numObjects = 0
        for obj in self.objects:
            numObjects+=obj.getNumObjects()
        return numObjects

    def getMatrix(self):
        matrix = []
        for object, material in zip(self.objects, self.materials):
            if object.geometryType < 5:
                localValue = object.toVector()
                localValue.extend(material.toVector())
                matrix.append(localValue)
            else:
                for subobj in object.objects:
                    localValue = subobj.toVector()
                    localValue.extend(material.toVector())
                    matrix.append(localValue)
        matrix = np.array(matrix, dtype=np.float32)
        return matrix




