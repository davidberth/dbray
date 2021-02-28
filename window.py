import pygame

class Window:

    def __init__(self, screenx, screeny):
        self.screenx = screenx
        self.screeny = screeny
        pygame.init()
        self.screen = pygame.display.set_mode((screenx, screeny))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 38)

    def updateFPS(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, False, pygame.Color("white"))
        return fps_text

    def frame(self, buffer):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        self.screen.fill((0, 0, 0))
        surface = pygame.surfarray.make_surface(buffer)
        self.screen.blit(surface, (0, 0))
        self.screen.blit(self.updateFPS(), (0, 0))
        pygame.display.flip()
        self.clock.tick(10)

        return True
