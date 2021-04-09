import pygmsh
from dbray.triangle import Triangle

# This is a compound geometry type
class ExtrudedPolygon():

    def __init__(self, vertices, height):
        self.polygonVertices = vertices
        self.height = height
        self.geometryType = 5
        self.level = 0

        with pygmsh.geo.Geometry() as geom:
            poly = geom.add_polygon(
                vertices,
                mesh_size=500.0,
            )
            geom.extrude(poly, [0.0, height, 0.0], num_layers=1)
            mesh = geom.generate_mesh()

        self.objects = []
        tindices = mesh.cells_dict['triangle']
        tpoints =  mesh.points
        for tri in tindices:
            self.objects.append(Triangle(tpoints[tri[0]], tpoints[tri[1]], tpoints[tri[2]]))

    def setLevel(self, level):
        self.level = level

    def getNumObjects(self):
        return len(self.objects)

