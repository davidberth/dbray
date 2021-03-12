import sphere
import material
import numpy as np
import random

class Scene:

    def __init__(self):

        self.objects = []
        self.materials = []

    def addObject(self, psphere, pmaterial):

        print (f'adding sphere {psphere.toVector()} with material {pmaterial.toVector()}')
        self.objects.append(psphere)
        self.materials.append(pmaterial)

    def getNumSpheres(self):
        return len(self.objects)

    def getMatrix(self):
        matrix = []
        for object, material in zip(self.objects, self.materials):
            localValue = object.toVector()
            localValue.extend(material.toVector())
            matrix.append(localValue)
        matrix = np.array(matrix, dtype=np.float32)
        return matrix

    def getObjectsMatrix(self):
        #TODO vectorize this!
        matrix = []
        for object in self.objects:
            matrix.append(object.toVector())
        matrix = np.array(matrix)
        return matrix

    def getMaterialsMatrix(self):
        #TODO vectorize this also!
        matrix = []
        for mat in self.materials:
            matrix.append(mat.toVector())
        matrix = np.array(matrix)
        return matrix

    def createSampleScene(self):

        # Add some objects to the scene.
        #self.addObject(sphere.Sphere([0.0, 3.7, -12.0], 1.5), material.Material(1.0, 0.0, 0.0))
        #self.addObject(sphere.Sphere([0.1, 0.5, -4.0], 0.2), material.Material(0.0, 1.0, 0.0))
        #self.addObject(sphere.Sphere([0.5, -0.5, -3.0], 0.3), material.Material(0.0, 0.0, 1.0))

        for i in range(500):
            self.addObject(sphere.Sphere([random.random() * 10.0 - 5.0, random.random() * 10.0 - 5.0, random.random() * 10.0 - 15.0],
                                         random.random() * 2.0 + 0.2), material.Material(random.random(), random.random(), random.random()))

