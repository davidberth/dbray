from dbray import window
from dbray import scene
from dbray.material import Material
from dbray.sphere import Sphere
from dbray.plane import Plane
from dbray.extpolygon import ExtrudedPolygon
from dbray.terrain import Terrain
import math
import random
import numpy as np


win = window.Window('DBray: Simple Example - David Berthiaume', 800,800)
scene = scene.Scene()

# Add some objects to the scene
random.seed(42)

tsizex, tsizey = 257, 257
heightField  = 2.0 * np.random.random((tsizex, tsizey))
#heightField = np.zeros((tsizex, tsizey))

#for i in range(tsizex):
#    for j in range(tsizey):
#        heightField[i,j] = np.random.random((tsizex, tsizey))

#scene.addObject(Terrain(heightField), Material(2.0, 2.0, 2.0, 0.1, 0.4, 0.3, 60.0))

scene.addObject(Plane([0.0, -1.0, 0.0], [0.0, 1.0, 0.0]), Material(2.0, 2.0, 2.0, 0.1, 0.4, 0.3, 60.0))

for i in range(0, 600, 5):
    x = math.cos(i / 100.0) * 50.0
    z = math.sin(i / 100.0) * 50.0
    s = 5
    h = 20
    #scene.addObject(AABB([x, 0.0, z], [x+s, h, z+s]),
    #                Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

    scene.addObject(ExtrudedPolygon([[x, 0.0, z], [x + s, 0.0, z], [x + s, 0.0, z + s/4], [x, 0.0, z + s]], h),
                Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

#scene.addObject(AABB([0, 0.0, 0], [100, 100, 100]),
#                    Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

win.camera.setPosition((0.0, 40.0, 25.0))
win.camera.setLookAt((20.0, 0.0, 20.0))

win.setScene(scene)
win.run()
