import numpy as np

class Buffer:

    def __init__(self, sizey, sizex):
        self.sizey = sizey
        self.sizex = sizex
        self.buffer = np.zeros((sizey, sizex, 3), dtype=np.uint8)

    def clear(self):
        self.buffer[:,:,:] = 0

