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

    def __init__(self, title, width, height):

        settings.WINDOW['class'] = 'moderngl_window.context.glfw.Window'
        settings.WINDOW['gl_version'] = (4, 6)
        settings.WINDOW['size'] = (width, height)
        settings.WINDOW['aspect_ratio'] = width / height
        settings.WINDOW['title'] = title
        settings.WINDOW['resizable'] = True
        settings.WINDOW['vsync'] = False

        path = os.path.abspath(__file__)
        dirPath = os.path.dirname(os.path.dirname(path))
        resources.register_dir(os.path.normpath(dirPath))

        self.wnd = moderngl_window.create_window_from_settings()
        self.ctx = self.wnd.ctx
        self.wnd.key_event_func = self.key_event
        self.wnd.mouse_press_event_func = self.mouse_press_event
        self.wnd.mouse_release_event_func = self.mouse_release_event
        self.wnd.position = (1640 - self.wnd.size[0]) // 2, (1140 - self.wnd.size[1]) // 2
        self.height = height
        self.width = width
        self.frames = 0
        self.oldTime = 0

        self.wnd.set_icon('resources/icon.png')
        self.camera = camera.Camera(self.wnd.keys)

    def setScene(self, scene):
        self.scene = scene
        self.sceneArray = self.scene.getMatrix()
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
        self.FSProgram['lightPosition'].value = (0.0, 50.0, 200.0)
        self.FSProgram['projScale'].value = 1.5
        ysampInc =1.0 / self.height
        xsampInc = 1.0 / self.width
        samples = []
        numSamples = 4
        numSample1 = int(math.sqrt(numSamples) + 0.1)
        for x in range(numSample1):
            for y in range(numSample1):
                samples.append( ( (x/numSample1) * xsampInc, (y/numSample1) * ysampInc ))

        self.FSProgram['samples'].value = samples

        self.texture = self.ctx.texture([self.sceneArray.shape[1], self.sceneArray.shape[0]], 3,
                                        self.sceneArray.tobytes(), dtype='f4')
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time):

        self.FSProgram['lightPosition'].value = (math.cos(time) * 100.0, 100.0, 100.0)

        cameraChange = self.camera.frame()

        if cameraChange:
            self.cameraPositionUniform.value = tuple(self.camera.location)
            self.cameraOrthoForwardUniform.value = tuple(self.camera.orthoForward)
            self.cameraOrthoRightUniform.value = tuple(self.camera.orthoRight)
            self.cameraOrthoUpUniform.value = tuple(self.camera.orthoUp)

        self.texture.use(location=0)
        self.quad_fs.render(self.FSProgram)

        if time - self.oldTime > 1:
            self.oldTime = time
            print (self.frames)
            self.frames = 0
        self.frames+=1

    def reloadShaders(self):
        self.initGL()

    def mouse_press_event(self, x, y, button):
        print (button)
        if button == 1:
            self.camera.moveForward = True
        else:
            self.camera.moveBackward = True

    def mouse_release_event(self, x, y, button):
        if button == 1:
            self.camera.moveForward = False
        else:
            self.camera.moveBackward = False


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





