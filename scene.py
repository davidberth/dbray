import sphere
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
