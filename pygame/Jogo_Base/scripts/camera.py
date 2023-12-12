from scripts.settings import *
import pygame

class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        self.display = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        
        self.limits = {"top": 0, "left": 0, "right": len(WORDMAP_LETTERS[0]) * TILESET - WIDTH, "bottom": len(WORDMAP_LETTERS) * TILESET - HEIGHT}

    def costumDraw(self, player):

        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.zLayer == layer:
                    off_rect = sprite.rect.copy()
                    off_rect.center -= self.offset 
                    if self.offset.x <= self.limits['left']:
                        off_rect.x = sprite.rect.copy().x
                    elif self.offset.x >= self.limits['right']:
                        off_rect.x = sprite.rect.copy().x - self.limits['right']
                        
                    if self.offset.y <= self.limits['top']:
                        off_rect.y = sprite.rect.copy().y
                    elif self.offset.y >= self.limits['bottom']:
                        off_rect.y = sprite.rect.copy().y - self.limits['bottom']
                    self.display.blit(sprite.image, off_rect)