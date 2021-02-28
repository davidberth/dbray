import numpy as np

class Buffer:

    def __init__(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.buffer = np.zeros((sizex, sizey, 3), dtype=np.uint8)

    def clear(self):
        self.buffer[:,:,:] = 0

