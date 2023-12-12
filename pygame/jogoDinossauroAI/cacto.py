#encoding: utf-8
import pygame
from pygame.locals import *
import os

dirPrinc = os.path.dirname(__file__)
dirImg = os.path.join(dirPrinc, 'sprites')
spriteSheet = pygame.image.load(os.path.join(dirImg, 'dinoSpritesheet.png'))

class Cacto(pygame.sprite.Sprite):
    def __init__(self, largura, altura, obs, vel, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = spriteSheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.num = num
        if self.num == 1:
            self.rect.center = (largura, altura - 64)
            self.rect.x = largura
        else:
            self.rect.center = (largura + self.rect.width, altura - 64)
            self.rect.x = largura + self.rect.width
        self.largura = largura
        self.obs = obs
        self.vel = vel

    def update(self):
        if ((self.obs == 0 or self.obs == 3) and self.num == 1) or (self.obs == 3 and self.num == 2):
            self.rect.x -= self.vel