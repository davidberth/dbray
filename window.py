import pygame
import buffer

class Window:

    def __init__(self, screeny, screenx):
        self.screeny = screeny
        self.screenx = screenx
        pygame.init()
        self.screen = pygame.display.set_mode((screeny, screenx))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28)

    def updateFPS(self):
        fps = f'FPS: {int(self.clock.get_fps())}'
        fps_text = self.font.render(fps, False, pygame.Color("white"))
        return fps_text

    def frame(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        self.screen.fill((0, 0, 0))
        surface = pygame.surfarray.make_surface(screen.buffer)
        self.screen.blit(surface, (0, 0))
        self.screen.blit(self.updateFPS(), (0, 0))
        pygame.display.flip()
        self.clock.tick(60)

        return True
