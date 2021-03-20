from dbray import sphere
from dbray import plane
from dbray import triangle
from dbray import material
import numpy as np
import random


class Scene:

    def __init__(self):

        self.objects = []
        self.materials = []

    def addObject(self, object, pmaterial):

        print (f'adding object {object.toVector()} with material {pmaterial.toVector()}')
        self.objects.append(object)
        self.materials.append(pmaterial)

    def getNumObjects(self):
        return len(self.objects)

    def getMatrix(self):
        matrix = []
        for object, material in zip(self.objects, self.materials):
            localValue = object.toVector()
            localValue.extend(material.toVector())
            matrix.append(localValue)
        matrix = np.array(matrix, dtype=np.float32)
        return matrix

    def createSampleScene(self):

        # Add some objects to the scene
        random.seed(42)
        #for i in range(200):
        #   self.addObject(sphere.Sphere([random.random() * 10.0 - 5.0, random.random() * 10.0 + 15.0, random.random() * 100.0 - 105.0],
        #                               random.random() * 1.0 + 0.1), material.Material(random.random(), random.random(), random.random()))


        self.addObject(plane.Plane([0.0, -5.0, 0.0], [0.0, 1.0, 0.0]), material.Material(1.0, 1.0, 1.0))

        for i in range(100):
            x = random.random() * 10.0
            y = random.random() * 10.0 + 3.0
            z = random.random() * 100.0 - 100.0
            self.addObject(triangle.Triangle([x,y,z], [x+5,y,z], [x+2,y+1,z+5]), material.Material(random.random(), random.random(), random.random()))
