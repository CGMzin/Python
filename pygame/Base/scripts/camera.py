from scripts.settings import *
import pygame

class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        self.display = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        
        self.limits = {"top": 0, "left": 0, "right": 1024, "bottom": 1200}
        #Arrumar limite

    def costumDraw(self, player):

        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.zLayer == layer:
                    off_rect = sprite.rect.copy()
                    off_rect.center -= self.offset
                    self.display.blit(sprite.image, off_rect)