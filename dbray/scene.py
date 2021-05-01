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
        #print (f'adding object {object.toVector()} with material {pmaterial.toVector()}')
        self.objects.append(object)
        self.materials.append(pmaterial)

    def getNumObjects(self):
        numObjects = 0
        for obj in self.objects:
            numObjects+=obj.getNumObjects()
        return numObjects

    def setMatrix(self, cy, cx, pad, matrix, localValue):
        matrix[cy, cx:cx+len(localValue),:] = np.array(localValue)
        cy+=1
        if cy > 2047:
            cy = 0
            cx+=pad
        return cy, cx

    def getMatrix(self):

        matrix = np.zeros((2048, 2048, 3), dtype=np.float32)
        cy = 0
        cx = 0
        pad = 10

        for object, material in zip(self.objects, self.materials):
            if object.geometryType < 5:
                localValue = object.toVector()
                localValue.extend(material.toVector())
                cy, cx = self.setMatrix(cy, cx, pad, matrix, localValue)

            else:

                if object.geometryType == 5:
                    # First we add an AABB to encompass the composite object.
                    aabb = object.getAABB()
                    # This defines how many objects to skip if the parent isn't collided with
                    aabb.setLevel(len(object.objects))
                    localValue = aabb.toVector()
                    # The material won't be used here.
                    localValue.extend(material.toVector())
                    cy, cx = setMatrix(cy, cx, pad, matrix, localValue)

                for subobj in object.objects:
                    localValue = subobj.toVector()
                    localValue.extend(material.toVector())
                    cy, cx = self.setMatrix(cy, cx, pad, matrix, localValue)

        return matrix




