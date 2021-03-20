import numpy as np

class Material:

    def __init__(self, red, green, blue):
        self.updateColor(red, green, blue)

    def updateColor(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def toVector(self):
        return [[self.red, self.green, self.blue]]