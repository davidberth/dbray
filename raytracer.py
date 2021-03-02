import numpy as np
from numba import jit
import buffer
import sphere

@jit(nopython=True)
def renderScene(sy, sx, buffer, camera, objects, materials):
    numObjects, _ = objects.shape
    t_min = 1.0
    for x in range(0, sx):
        for y in range(0, sy):
            D = np.array([x/sx - 0.5, y/sy - 0.5, 1.0])

            closest_t = 9999999999.0
            closest_sphere = -1
            for k in range(numObjects):

                t1, t2 = sphere.intersect(camera, D, objects[k])
                if t1 > t_min and t1 < closest_t:
                    closest_t = t1
                    closest_sphere = k
                if t2 > t_min and t2 < closest_t:
                    closest_t = t2
                    closest_sphere = k

            if closest_sphere > -1:
                buffer[x, y, :] = materials[closest_sphere] * 255
            else:
                buffer[x, y, :] = 0


class RayTracer:

    def __init__(self):
        pass

    def render(self, screen, scene):
        objects = scene.getObjectsMatrix()
        materials = scene.getMaterialsMatrix()

        # Place the camera location at the origin
        camera = np.array([0.0, 0.0, 0.0])
        renderScene(screen.sizey, screen.sizex, screen.buffer, camera, objects, materials)
