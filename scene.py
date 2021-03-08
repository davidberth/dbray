import sphere
import material
import numpy as np


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
        self.addObject(sphere.Sphere([0.0, 0.0, 2.0], 0.5), material.Material(1.0, 0.0, 0.0))
        self.addObject(sphere.Sphere([0.0, 0.5, 4.0], 0.6), material.Material(0.0, 1.0, 0.0))
        self.addObject(sphere.Sphere([0.5, -0.5, 3.0], 0.3), material.Material(0.0, 0.0, 1.0))