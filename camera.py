import numpy as np
import math

class Camera():

    def __init__(self):
        self.location = np.array([0.0, 0.0, 0.0], dtype = np.float32)
        self.yaw = 0.0
        self.pitch = 0.0
        #self.lookAt = np.array([100.0, -5.0, -300.0], dtype = np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype = np.float32)
        self.getOrthonormal()

    def getOrthonormal(self):

        # Construct an orthonormal basis to use for ray generation
        xzLen = math.cos(self.pitch)
        x = xzLen * math.cos(self.yaw)
        y = math.sin(self.pitch)
        z = xzLen * math.sin(-self.yaw)
        direction = np.array([x,y,z], dtype=np.float32)
        self.orthoForward = direction / np.linalg.norm(direction)
        self.orthoRight = np.cross(self.orthoForward, self.up)
        self.orthoRight /= np.linalg.norm(self.orthoRight)
        self.orthoUp = np.cross(self.orthoRight, self.orthoForward)





