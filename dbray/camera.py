import numpy as np
import math

class Camera():

    def __init__(self, keys):
        self.location = np.array([0.0, 1.0, 0.0], dtype = np.float32)
        # Face in -z direction
        self.yaw = math.pi / 2.0
        self.pitch = 0.0
        self.up = np.array([0.0, 1.0, 0.0], dtype = np.float32)
        self.getOrthonormal()

        self.turnLeft = False
        self.turnRight = False
        self.tiltUp = False
        self.tiltDown = False
        self.moveForward = False
        self.moveBackward = False
        self.strafeRight = False
        self.strafeLeft = False
        self.moveUp = False
        self.moveDown = False

        self.turnSpeed = 0.05
        self.tiltSpeed = 0.025
        self.moveSpeed = 0.5

        self.twopi = math.pi * 2.0

        self.turnLeftKey = keys.A
        self.turnRightKey = keys.D
        self.tiltUpKey = keys.W
        self.tiltDownKey = keys.S
        self.moveForwardKey = keys.UP
        self.moveBackwardKey = keys.DOWN
        self.strafeLeftKey = keys.Q
        self.strafeRightKey = keys.E
        self.moveUpKey = keys.T
        self.moveDownKey = keys.G

    def setPosition(self, pos):
        self.location = np.array(pos)

    def setLookAt(self, lookAt):

        direction = np.array(lookAt) - self.location
        direction/= np.linalg.norm(direction)
        print (direction)
        self.pitch = math.asin(direction[1])
        self.yaw = math.atan2(direction[0], direction[2]) - math.pi / 2.0

        if self.yaw < 0.0:
            self.yaw += self.twopi
        if self.yaw > self.twopi:
            self.yaw -= self.twopi
        if self.pitch > math.pi - 0.01:
            self.pitch = math.pi - 0.01
        if self.pitch < -math.pi + 0.01:
            self.pitch = -math.pi + 0.01

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

    def processKeyEvent(self, key, action, keys):
        if action == keys.ACTION_PRESS:
            keySwitch = True
        else:
            keySwitch = False

        if key == self.turnLeftKey:
            self.turnLeft = keySwitch
        if key == self.turnRightKey:
            self.turnRight = keySwitch
        if key == self.tiltDownKey:
            self.tiltDown = keySwitch
        if key == self.tiltUpKey:
            self.tiltUp = keySwitch
        if key == self.moveForwardKey:
            self.moveForward = keySwitch
        if key == self.moveBackwardKey:
            self.moveBackward = keySwitch
        if key == self.strafeRightKey:
            self.strafeRight = keySwitch
        if key == self.strafeLeftKey:
            self.strafeLeft = keySwitch
        if key == self.moveUpKey:
            self.moveUp = keySwitch
        if key == self.moveDownKey:
            self.moveDown = keySwitch


    def frame(self):
        cameraMoving = self.turnLeft or self.turnRight or self.tiltDown or self.tiltUp or \
                       self.moveForward or self.moveBackward or self.strafeLeft or self.strafeRight or \
                       self.moveUp or self.moveDown

        if cameraMoving:
            if self.moveForward:
                self.location = self.location + self.orthoForward * self.moveSpeed
            if self.moveBackward:
                self.location = self.location - self.orthoForward * self.moveSpeed
            if self.strafeRight:
                self.location = self.location + self.orthoRight * self.moveSpeed
            if self.strafeLeft:
                self.location = self.location - self.orthoRight * self.moveSpeed
            if self.moveUp:
                self.location = self.location + self.orthoUp * self.moveSpeed
            if self.moveDown:
                self.location = self.location - self.orthoUp * self.moveSpeed
            if self.turnRight:
                self.yaw -= self.turnSpeed
                if self.yaw < 0.0:
                    self.yaw += self.twopi
            if self.turnLeft:
                self.yaw += self.turnSpeed
                if self.yaw > self.twopi:
                    self.yaw -= self.twopi
            if self.tiltUp:
                self.pitch += self.tiltSpeed
                if self.pitch > math.pi - 0.01:
                    self.pitch = math.pi - 0.01
            if self.tiltDown:
                self.pitch -= self.tiltSpeed
                if self.pitch < -math.pi + 0.01:
                    self.pitch = -math.pi + 0.01

            self.getOrthonormal()
        return cameraMoving



