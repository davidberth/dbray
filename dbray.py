import window
import buffer
import raytracer

screenx, screeny = 600, 600
screen = buffer.Buffer(screenx, screeny)
window = window.Window(screeny, screenx)
tracer = raytracer.RayTracer()

running = True
while running:
    tracer.render(screen)
    running = window.frame(screen)




