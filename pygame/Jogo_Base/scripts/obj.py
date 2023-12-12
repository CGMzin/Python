import pygame, os

class Obj(pygame.sprite.Sprite):

    def __init__(self, img, pos, z, *groups):

        super().__init__(*groups)

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.zLayer = z
