import os
from moderngl_window import geometry
import moderngl_window as mglw
import moderngl as mgl
import scene
import camera
import numpy as np


class DBRay(mglw.WindowConfig):
    gl_version = (4, 6)
    aspect_ratio = 1.0
    title = 'DBRay - David Berthiaume'
    window_size = (800, 700)
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
        self.sceneArray = self.scene.getMatrix()

        self.wnd.set_icon('resources/icon.png')
        # For rendering a simple textured quad
        self.vertexShaderFile = 'shaders/vertex.glsl'
        self.fragmentShaderFile = 'shaders/fragment.glsl'
        self.FSProgram = self.load_program(vertex_shader=self.vertexShaderFile,
                                           fragment_shader=self.fragmentShaderFile)

        self.camera = camera.Camera()
        self.cameraPositionUniform = self.FSProgram['cameraPosition']
        self.cameraOrthoForwardUniform = self.FSProgram['cameraForward']
        self.cameraOrthoRightUniform = self.FSProgram['cameraRight']
        self.cameraOrthoUpUniform = self.FSProgram['cameraUp']

        self.cameraPositionUniform.value =tuple(self.camera.location)
        self.cameraOrthoForwardUniform.value = tuple(self.camera.orthoForward)
        self.cameraOrthoRightUniform.value = tuple(self.camera.orthoRight)
        self.cameraOrthoUpUniform.value = tuple(self.camera.orthoUp)

        self.FSProgram['numObjects'] = self.scene.getNumObjects()

        self.texture = self.ctx.texture([self.sceneArray.shape[1], self.sceneArray.shape[0]], 3, self.sceneArray.tobytes(), dtype='f4')
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        #self.texture.swizzle = 'RGB1'  # What components texelFetch will get from the texture (in shader)
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time):

        self.camera.yaw = time
        self.camera.getOrthonormal()
        # TODO move this into the camera class?
        self.cameraPositionUniform.value = tuple(self.camera.location)
        self.cameraOrthoForwardUniform.value = tuple(self.camera.orthoForward)
        self.cameraOrthoRightUniform.value = tuple(self.camera.orthoRight)
        self.cameraOrthoUpUniform.value = tuple(self.camera.orthoUp)

        self.texture.use(location=0)
        self.quad_fs.render(self.FSProgram)

    def reloadShaders(self):
        self.FSProgram = self.load_program(vertex_shader=self.vertexShaderFile,
                                           fragment_shader=self.fragmentShaderFile)
        self.cameraPositionUniform = self.FSProgram['cameraPosition']
        self.cameraPositionUniform.value = (0.0, 0.0, 0.0)
        self.FSProgram['numSpheres'] = self.scene.getNumSpheres()

        self.texture = self.ctx.texture([self.sceneArray.shape[2], self.sceneArray.shape[0]], 3,
                                        self.sceneArray.tobytes(), dtype='f4')
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.quad_fs = geometry.quad_fs()

    def key_event(self, key, action, modifiers):
        if key == self.wnd.keys.R and action == self.wnd.keys.ACTION_PRESS:
            print('Reloading shaders')
            self.reloadShaders()


    @classmethod
    def run(cls):
        mglw.run_window_config(cls)

if __name__ == '__main__':
    DBRay.run()




