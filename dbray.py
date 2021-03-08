import os
from moderngl_window import geometry
import moderngl_window as mglw
import moderngl as mgl
import scene
import numpy as np

class DBRay(mglw.WindowConfig):
    gl_version = (4, 6)
    aspect_ratio = 1.0
    title = 'DBRay - David Berthiaume'
    window_size = (600,600)
    aspect_ratio = None
    resizable = False
    vsync = True
    resource_dir = os.path.normpath('c:/dbray')

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        # Center the window on the screen
        # TODO find a way to read the screen resolution
        atHome = True
        if atHome:
            self.wnd.position = (3640 - self.wnd.size[0]) // 2, (1440 - self.wnd.size[1]) // 2
        else:
            # closer to the top of the screen
            self.wnd.position = (1920 - self.wnd.size[0]) // 2, (1024 - self.wnd.size[1]) // 2

        self.scene = scene.Scene()
        self.scene.createSampleScene()

        self.wnd.set_icon('resources/icon.png')
        # For rendering a simple textured quad
        self.vertexShaderFile = 'shaders/vertex.glsl'
        self.fragmentShaderFile = 'shaders/fragment.glsl'
        self.FSProgram = self.load_program(vertex_shader=self.vertexShaderFile,
                                           fragment_shader=self.fragmentShaderFile)
        self.FSProgram['cameraPosition'].value = (0.0, 0.0, 0.0)
        self.sceneArray = np.array([[0.0, 0.0, -1.0, 0.25],[0.4, 0.4, -1.0, 0.35],[-1.0, -1.0, -2.0, 0.45]], dtype=np.float32)
        self.texture = self.ctx.texture((4,3), 1, self.sceneArray.tobytes(), dtype='f4')
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.texture.swizzle = 'RRR1'  # What components texelFetch will get from the texture (in shader)
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.texture.use(location=0)
        self.quad_fs.render(self.FSProgram)

    def reloadShaders(self):
        self.FSProgram = self.load_program(vertex_shader=self.vertexShaderFile,
                                           fragment_shader=self.fragmentShaderFile)

    def key_event(self, key, action, modifiers):
        if key == self.wnd.keys.R and action == self.wnd.keys.ACTION_PRESS:
            print('Reloading shaders')
            self.reloadShaders()


    @classmethod
    def run(cls):
        mglw.run_window_config(cls)

if __name__ == '__main__':
    DBRay.run()




