from dbray import window
from dbray import scene

win = window.Window('DBray - David Berthiaume', 1000, 1000)
scene = scene.Scene()
scene.createSampleScene()
win.setScene(scene)
win.run()
