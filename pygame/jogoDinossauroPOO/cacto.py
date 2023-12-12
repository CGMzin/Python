#encoding: utf-8
import pygame
from pygame.locals import *
import os

dirPrinc = os.path.dirname(__file__)
dirImg = os.path.join(dirPrinc, 'sprites')
spriteSheet = pygame.image.load(os.path.join(dirImg, 'dinoSpritesheet.png'))

class Cacto(pygame.sprite.Sprite):
    def __init__(self, largura, altura, obs, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = spriteSheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (largura, altura - 64)
        self.rect.x = largura
        self.largura = largura
        self.obs = obs
        self.vel = vel

    def update(self):
        if self.obs == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = self.largura
            self.rect.x -= self.vel