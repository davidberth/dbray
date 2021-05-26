from dbray.triangle import Triangle
from dbray.aabb import AABB
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
# This is a compound geometry type
class Terrain():

    def __init__(self, heightField, scalex, scaley, offsetx, offsety):
        self.heightField = heightField
        self.geometryType = 6
        self.level = 0
        self.objects = []
        self.scalex = scalex
        self.scaley = scaley
        self.offsetx = offsetx
        self.offsety = offsety

        self.normalField = self.getNormalField(heightField)



        self.quadtree(0, heightField.shape[0]-1, 0, heightField.shape[1]-1, heightField, 0, 0, self.objects)
        self.minvec = [0, np.min(heightField), 0]
        self.maxvec = [heightField.shape[0], np.max(heightField), heightField.shape[1]]

    def getNormalField(self, heightField):
        dx = -ndimage.sobel(heightField, 0) / self.scalex # horizontal derivative
        dz = -ndimage.sobel(heightField, 1) / self.scaley # vertical derivative
        dy = np.ones_like(dx)

        # now we place this into a single array
        normalMap = np.dstack([dx, dy, dz])
        mags = np.sqrt((normalMap * normalMap).sum(axis=2))
        normalMap[:, :, 0] /= mags
        normalMap[:, :, 1] /= mags
        normalMap[:, :, 2] /= mags

        return normalMap


    def quadtree(self, xmin, xmax, ymin, ymax, heightField, level, triangles, objects):

        localLevel = level
        localTriangles = triangles
        oldLevel = level
        oldTriangles = triangles
        hsubset = heightField[xmin:xmax+1, ymin:ymax+1]
        hmax = np.max(hsubset)
        hmin = np.min(hsubset)
        scalex = self.scalex
        scaley = self.scaley
        offsetx = self.offsetx
        offsety = self.offsety

        xxmin = xmin * scalex + offsetx
        xxmax = xmax * scalex + offsetx
        yymin = ymin * scaley + offsety
        yymax = ymax * scaley + offsety

        aabb = AABB([xxmin, hmin, yymin], [xxmax + scalex, hmax + 0.00001, yymax + scaley])
        objects.append(aabb)
        currentIndex = len(objects) - 1

        halfx = (xmax - xmin)//2
        halfy = (ymax - ymin)//2

        if (xmax - xmin) * (ymax - ymin) < 5:
            # we are at a leaf so we generate terrain geometries

            for x in range(xmin, xmax):
                for y in range(ymin, ymax):
                    if heightField[x,y] > -1.0 and  heightField[x+1,y] > -1.0 and heightField[x,y+1] > -1.0:
                        xx = x * scalex + offsetx
                        yy = y * scaley + offsety
                        v1 = [xx, heightField[x, y], yy]
                        v2 = [xx + scalex, heightField[x + 1, y], yy]
                        v3 = [xx, heightField[x, y + 1], yy + scaley]

                        triangle = Triangle(v1, v2, v3, self.normalField[x,y], self.normalField[x +1,y], self.normalField[x,y+1])
                        objects.append(triangle)
                        localLevel+=1
                        localTriangles+=1

                    if heightField[x + 1, y] > -1.0 and heightField[x + 1, y + 1] > -1.0 and heightField[x, y + 1] > -1.0:
                        xx = x * scalex + offsetx
                        yy = y * scaley + offsety
                        v1 = [xx + scalex, heightField[x + 1, y], yy]
                        v2 = [xx + scalex, heightField[x + 1, y + 1], yy + scaley]
                        v3 = [xx, heightField[x, y + 1], yy + scaley]

                        triangle = Triangle(v1, v2, v3, self.normalField[x+1,y], self.normalField[x+1,y+1], self.normalField[x,y+1])
                        objects.append(triangle)
                        localLevel+=1
                        localTriangles+1

        else:
            # need to subdivide further and generate AABBs
            qlevel, qtriangles = self.quadtree(xmin, xmin + halfx, ymin, ymin + halfy, heightField, level, triangles, objects)
            localLevel+=qlevel - oldLevel
            localTriangles+=qtriangles - oldTriangles

            qlevel, qtriangles = self.quadtree(xmin + halfx, xmax, ymin, ymin + halfy, heightField, level, triangles, objects)
            localLevel += qlevel - oldLevel
            localTriangles += qtriangles - oldTriangles

            qlevel, qtriangles = self.quadtree(xmin, xmin + halfx, ymin + halfy, ymax, heightField, level, triangles, objects)
            localLevel+=qlevel - oldLevel
            localTriangles+=qtriangles - oldTriangles

            qlevel, qtriangles = self.quadtree(xmin + halfx, xmax, ymin + halfy, ymax, heightField, level, triangles, objects)
            localLevel += qlevel - oldLevel
            localTriangles += qtriangles - oldTriangles


        objects[currentIndex].setLevel(localLevel - oldLevel)
        # No new triangles were created
        if localTriangles == oldTriangles:
            #print ('about to remove')
            #for i in objects:
            #    print (i.geometryType)

            objects.pop()
        else:
            localLevel+=1

        return localLevel, localTriangles

    def getAABB(self):
        return AABB(self.minvec, self.maxvec)

    def setLevel(self, level):
        self.level = level

    def getNumObjects(self):
        return len(self.objects)

