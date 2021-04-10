from dbray import window
from dbray import scene
from dbray.material import Material
from dbray.sphere import Sphere
from dbray.plane import Plane
from dbray.triangle import Triangle
from dbray.aabb import AABB
from dbray.extpolygon import ExtrudedPolygon
import math
import random
import trimesh

win = window.Window('DBray: Simple Example - David Berthiaume', 1000, 1000)
scene = scene.Scene()

# Add some objects to the scene
random.seed(42)
for i in range(10):



    x = i * 5.0 - 25.0
    ambient = 0.05
    if i==5:
        ambient = 0.25
    mat = Material(random.random(), random.random(), random.random(),
                   ambient, 0.3 + i * .05, 0.3 + i * .04, i * 18.0 + 10.0)
    scene.addObject(Sphere([x, i/5.0 + 0.5, -8.0], i/5.0 + 0.5), mat)
    #scene.addObject(Triangle([x, 5.0, -12.0], [x+2.0, 6.0, -17.0], [x+1.0, 14.0, -18.0]), mat)


scene.addObject(Plane([0.0, 0.0, 0.0], [0.0, 1.0, 0.0]), Material(2.0, 2.0, 2.0, 0.1, 0.4, 0.3, 60.0))
#scene.addObject(Plane([0.0, 0.0, -20.0], [0.0, 0.0, 1.0]), Material(1.0, 1.0, 1.0, 0.01, 0.4, 0.3, 30.0))

for i in range(0, 600, 6):
    x = math.cos(i / 100.0) * 300.0
    z = math.sin(i / 100.0) * 300.0
    s = 10
    h = 20
    #scene.addObject(AABB([x, 0.0, z], [x+s, h, z+s]),
    #                Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

    scene.addObject(ExtrudedPolygon([[x, 0.0, z], [x + s, 0.0, z], [x + s, 0.0, z + s/2], [x, 0.0, z + s]], h),
                Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

#scene.addObject(AABB([0, 0.0, 0], [100, 100, 100]),
#                    Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

win.camera.setPosition((0.0, 10.0, 15.0))
win.camera.setLookAt((0.0, 3.0, -3.0))

win.setScene(scene)
win.run()
