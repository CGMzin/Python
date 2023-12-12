import pygame

class Obj(pygame.sprite.Sprite):
    def __init__(self, img, pos, *groups):

        super().__init__(*groups)

        self.pos = pos
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)

    def erase(self):
        self.rect.x =  100000000
