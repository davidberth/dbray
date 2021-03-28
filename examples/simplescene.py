from dbray import window
from dbray import scene
from dbray.material import Material
from dbray.sphere import Sphere
from dbray.plane import Plane
from dbray.triangle import Triangle
import math
import random
import trimesh

win = window.Window('DBray: Simple Example - David Berthiaume', 1000, 1000)
scene = scene.Scene()

# Add some objects to the scene
random.seed(42)
for i in range(10):
    x = i * 5.0 - 25.0
    mat = Material(random.random(), random.random(), random.random())
    scene.addObject(Sphere([x, 5.0, -8.0], i/5.0 + 0.5), mat)
    scene.addObject(Triangle([x, 5.0, -12.0], [x+2.0, 6.0, -17.0], [x+1.0, 14.0, -18.0]), mat)


scene.addObject(Plane([0.0, 0.0, 0.0], [0.0, 1.0, 0.0]), Material(1.0, 1.0, 1.0))
win.camera.setPosition((0.0, 10.0, 15.0))
win.camera.setLookAt((0.0, 3.0, -3.0))

win.setScene(scene)
win.run()
