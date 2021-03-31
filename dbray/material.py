class Material:

    def __init__(self, red, green, blue, ambient, diffuse, specular, shininess):
        self.updateColor(red, green, blue)
        self.updateLighting(ambient, diffuse, specular, shininess)

    def updateColor(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def updateLighting(self, ambient, diffuse, specular, shininess):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def toVector(self):
        return [[self.red, self.green, self.blue], [self.ambient, self.diffuse, self.specular], [self.shininess, 0.0, 0.0]]