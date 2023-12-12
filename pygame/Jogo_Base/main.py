import pygame, sys
from scripts.scene import Scene
from scripts.settings import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.display = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        self.menu = Scene()

    def run(self):
        #definir condição de morte
        while not self.menu.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.fill("black")
            self.menu.run()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()