from gcube import pcube
from gcube import exportcube
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import geopandas as gpd

import random
from dbray import window
from dbray import scene
from dbray.material import Material
from dbray.sphere import Sphere
from dbray.plane import Plane
from dbray.extpolygon import ExtrudedPolygon
from dbray.terrain import Terrain
import sys

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:gcube@localhost:5432/gcube')

print (engine)
scalex, scaley = 100, 100

#pcube.createCube(cubename = 'test', clipbounds = [-72.0946708075911, -72.02921181250076, 42.10445197355287, 42.135192408339655], layers = ['building', 'elevation', 'tree', 'grid100'])
exportcube.exportCube(cubename = 'test', group = 'grid100', fileFormat = 'preview')
a=pd.read_sql_query('select elevation_mean1 as y, st_x(st_centroid(geom)) as x, st_y(st_centroid(geom)) as z from cube_test._c_temp__preview',con=engine)
exportcube.exportCube(cubename = 'test', group = 'building', fileFormat = 'preview')
sql = f"select geom, " \
      f"elevation_mean1, building_area_overlap from cube_test._c_temp__preview"
df = gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='geom')
print (df)

del engine

amin = a.min()

xmin = amin['x']
ymin = amin['y']
zmin = amin['z']

# Sample one data point per cell
a['x'] = (a['x'] - xmin) / 100
a['z'] = (a['z'] - zmin) / 100
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

win = window.Window('DBray: Real Scene Example - David Berthiaume', 1000,800)
scene = scene.Scene()

terrain = Terrain(grid, scalex, scaley, offsetx, offsety, xmin, zmin)

scene.addObject(terrain, Material(1.0, 1.0, 1.0, 0.0, 0.6, 0.4, 10.0))

for e, item in df.iterrows():
      elev = item['elevation_mean1']
      xx, yy = item['geom'].exterior.coords.xy

      # get the polygon
      coords = []
      for x, y in zip(xx, yy):
            coords.append([x, y])

      x = coords[0][0] + offsetx
      y = coords[0][1] + offsety

      rx, ry, rz = terrain.getRenderCoordinates(x,y)

      scene.addObject(Sphere((rx, ry + 10.0, rz), 10.0), Material(1.0, 0.0, 0.0, 0.9, 0.6, 0.4, 10.0))



#scene.addObject(Sphere((50, yAverage + 500, 50),  400.0), Material(1.0, 0.0, 0.0, 0.9, 0.6, 0.6, 60.0))

win.camera.setPosition((0.0, yAverage + 1900.0, 0.0))
win.camera.setLookAt((0.0, yAverage, 100.0))

win.setScene(scene)
win.run()