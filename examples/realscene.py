from gcube import pcube
from gcube import exportcube
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

import random
from dbray import window
from dbray import scene
from dbray.material import Material
from dbray.sphere import Sphere
from dbray.plane import Plane
from dbray.extpolygon import ExtrudedPolygon
from dbray.terrain import Terrain

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:gcube@localhost:5432/gcube')

print (engine)
scalex, scaley = 100, 100

#pcube.createCube(cubename = 'test', clipsource = 'zipcode', clipitem = '01562', layers = ['building', 'elevation', 'tree', 'grid100'])


#exportcube.exportCube(cubename = 'test', group = 'grid100', fileFormat = 'preview')

a=pd.read_sql_query('select elevation_mean1 as y, st_x(st_centroid(geom)) as x, st_y(st_centroid(geom)) as z from cube_test._c_temp__preview',con=engine)

amin = a.min()

xmin = amin['x']
ymin = amin['y']
zmin = amin['z']

# Sample one data point per cell
a['x'] = (a['x'] - xmin) / 100
a['z'] = (a['z'] - zmin) / 100
#a['y'] = (a['y'] - ymin) / 10.0
amax = a.max()
xmax = amax['x']
zmax = amax['z']

x = a['x'].values
y = a['y'].values
z = a['z'].values

points = np.vstack([x,z]).T

grid_x, grid_y = np.mgrid[0:xmax, 0:zmax]

offsetx = -(xmax/2) * scalex
offsety = -(zmax/2) * scaley

yAverage = np.mean(y)

grid = griddata(points, y, (grid_x, grid_y), method='linear', fill_value=-10.0)
#grid = np.zeros( (int(xmax), int(zmax)))
#for i in range(0, int(xmax)):
#    for j in range(0, int(zmax)):
#        grid[i, j] = np.sqrt((xmax/2 - i) ** 2 + (zmax/2 - j) ** 2) ** 2.0

#plt.imshow(grid)
#plt.show()



win = window.Window('DBray: Real Scene Example - David Berthiaume', 800,800)
scene = scene.Scene()

scene.addObject(Terrain(grid, scalex, scaley, offsetx, offsety), Material(1.0, 1.0, 1.0, 0.0, 0.6, 0.6, 60.0))
scene.addObject(Sphere((50, yAverage + 500, 50),  400.0), Material(1.0, 0.0, 0.0, 0.9, 0.6, 0.6, 60.0))

win.camera.setPosition((0.0, yAverage + 1900.0, 0.0))
win.camera.setLookAt((0.0, yAverage, 100.0))

win.setScene(scene)
win.run()