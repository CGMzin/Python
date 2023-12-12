#encoding: utf-8
import pygame
from pygame.locals import *
import os

dirPrinc = os.path.dirname(__file__)
dirImg = os.path.join(dirPrinc, 'sprites')
spriteSheet = pygame.image.load(os.path.join(dirImg, 'dinoSpritesheet.png'))

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self, largura, obs, vel, num):
        pygame.sprite.Sprite.__init__(self)
        
        self.imgDino = []
        for i in range(3, 5):
            img = spriteSheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imgDino.append(img)

        self.index = 0
        self.image = self.imgDino[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.largura = largura
        self.num = num
        if self.num == 1:
            self.rect.center = (largura, 250)
            self.rect.x = largura
        else:
            self.rect.center = (largura + self.rect.width + 50, 250)
            self.rect.x = largura + self.rect.width
        self.obs = obs
        self.vel = vel

    def update(self):
        if ((self.obs == 1 or self.obs == 2) and self.num == 1) or (self.obs == 2 and self.num == 2):
            self.rect.x -= self.vel

            if self.index > 1:
                self.index = 0
            self.index += 0.25
            self.image = self.imgDino[int(self.index)]