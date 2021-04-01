from dbray import window
from dbray import scene
from dbray.material import Material
from dbray.sphere import Sphere
from dbray.plane import Plane
from dbray.triangle import Triangle
from dbray.extpolygon import ExtrudedPolygon
import math
import random
import trimesh

win = window.Window('DBray: Simple Example - David Berthiaume', 800, 800)
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


scene.addObject(Plane([0.0, 0.0, 0.0], [0.0, 1.0, 0.0]), Material(1.0, 1.0, 1.0, 0.01, 0.4, 0.3, 10.0))
#scene.addObject(Plane([0.0, 0.0, -20.0], [0.0, 0.0, 1.0]), Material(1.0, 1.0, 1.0, 0.01, 0.4, 0.3, 30.0))

for i in range(10):
    x = random.random() * 100.0 - 50.0
    z = random.random() * 100.0 - 50.0
    s = random.random() * 10.0 + 5.0
    h = random.random() * 10.0 + 4.0
    scene.addObject(ExtrudedPolygon([[x, 0.0, z], [x + s, 0.0, z], [x + s, 0.0, z + s], [x, 0.0, z + s]], h),
                Material(random.random(), random.random(), random.random(), 0.01, 0.4, 0.5, 190.0))

win.camera.setPosition((0.0, 10.0, 15.0))
win.camera.setLookAt((0.0, 3.0, -3.0))

win.setScene(scene)
win.run()
