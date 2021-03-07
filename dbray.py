import win
import buffer
import raytracer
import scene
import sphere
import material

screenx, screeny = 600,600
screen = buffer.Buffer(screenx, screeny)
scene = scene.Scene()
window = win.Window(screeny, screenx)
tracer = raytracer.RayTracer()

# Add some objects to the scene
scene.addObject(sphere.Sphere([0.0, 0.0, 2.0], 0.5), material.Material(1.0, 0.0, 0.0))
scene.addObject(sphere.Sphere([0.0, 0.5, 4.0], 0.6), material.Material(0.0, 1.0, 0.0))
scene.addObject(sphere.Sphere([0.5, -0.5, 3.0], 0.3), material.Material(0.0, 0.0, 1.0))


running = True
while running:
    tracer.render(screen, scene)
    running = window.frame(screen)




