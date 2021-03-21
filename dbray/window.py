import os
from moderngl_window import geometry
import moderngl_window
from moderngl_window.conf import settings
from moderngl_window.timers.clock import Timer
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription
import moderngl as mgl
import math
from dbray import scene
from dbray import camera


class Window():

    def __init__(self, **kwargs):

        settings.WINDOW['class'] = 'moderngl_window.context.glfw.Window'
        settings.WINDOW['gl_version'] = (4, 6)
        settings.WINDOW['size'] = (800, 800)
        settings.WINDOW['aspect_ratio'] = 1.0
        settings.WINDOW['title'] = 'DBray - David Berthiaume'
        settings.WINDOW['resizable'] = False
        settings.WINDOW['vsync'] = True
        path = os.path.abspath(__file__)
        dirPath = os.path.dirname(os.path.dirname(path))
        resources.register_dir(os.path.normpath(dirPath))

        self.wnd = moderngl_window.create_window_from_settings()
        self.ctx = self.wnd.ctx
        self.wnd.key_event_func = self.key_event

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
        self.camera = camera.Camera(self.wnd.keys)
        self.initGL()

    def initGL(self):
        self.vertexShaderFile = 'dbray/shaders/vertex.glsl'
        self.fragmentShaderFile = 'dbray/shaders/fragment.glsl'

        self.FSProgram = resources.programs.load(
            ProgramDescription(
                vertex_shader=self.vertexShaderFile,
                fragment_shader=self.fragmentShaderFile,
            )
        )

        self.cameraPositionUniform = self.FSProgram['cameraPosition']
        self.cameraOrthoForwardUniform = self.FSProgram['cameraForward']
        self.cameraOrthoRightUniform = self.FSProgram['cameraRight']
        self.cameraOrthoUpUniform = self.FSProgram['cameraUp']

        self.cameraPositionUniform.value = tuple(self.camera.location)
        self.cameraOrthoForwardUniform.value = tuple(self.camera.orthoForward)
        self.cameraOrthoRightUniform.value = tuple(self.camera.orthoRight)
        self.cameraOrthoUpUniform.value = tuple(self.camera.orthoUp)

        self.FSProgram['numObjects'] = self.scene.getNumObjects()
        self.FSProgram['lightPosition'].value = (0.0, 50.0, 15.0)

        self.texture = self.ctx.texture([self.sceneArray.shape[1], self.sceneArray.shape[0]], 3,
                                        self.sceneArray.tobytes(), dtype='f4')
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time):

        self.FSProgram['lightPosition'].value = (math.cos(time) * 100.0, 100.0, -10.0 + math.sin(time) * 100.0)

        cameraChange = self.camera.frame()

        if cameraChange:
            self.cameraPositionUniform.value = tuple(self.camera.location)
            self.cameraOrthoForwardUniform.value = tuple(self.camera.orthoForward)
            self.cameraOrthoRightUniform.value = tuple(self.camera.orthoRight)
            self.cameraOrthoUpUniform.value = tuple(self.camera.orthoUp)

        self.texture.use(location=0)
        self.quad_fs.render(self.FSProgram)

    def reloadShaders(self):
        self.initGL()

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.P:
                print('Reloading shaders')
                self.reloadShaders()

        if action == self.wnd.keys.ACTION_PRESS or action == self.wnd.keys.ACTION_RELEASE:
            self.camera.processKeyEvent(key, action, self.wnd.keys)


    def run(self):
        timer = Timer()
        timer.start()

        while not self.wnd.is_closing:
            self.wnd.clear()
            time, frame_time = timer.next_frame()
            self.render(time, frame_time)
            self.wnd.swap_buffers()

        self.wnd.destroy()

if __name__ == '__main__':
    win = Window()
    win.run()




