import buffer
import numpy as np
from numba import jit

@jit(nopython=True)
def renderScene(sy, sx, buffer, box):
    for i in range(sy):
        for j in range(sx):

            if box[0] < j < box[1] and box[2] < i < box[3]:
                buffer[i, j, 0] = box[4]
                buffer[i, j, 1] = box[5]
                buffer[i, j, 2] = box[6]


class RayTracer:

    def __init__(self):
        self.boxes = np.array([30, 80, 40, 80, 240, 0, 0])

    def render(self, screen):

        renderScene(screen.sizey, screen.sizex, screen.buffer, self.boxes)
