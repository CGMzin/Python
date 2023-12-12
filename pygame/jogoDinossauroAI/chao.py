#encoding: utf-8
import pygame
from pygame.locals import *
import os

dirPrinc = os.path.dirname(__file__)
dirImg = os.path.join(dirPrinc, 'sprites')
spriteSheet = pygame.image.load(os.path.join(dirImg, 'dinoSpritesheet.png'))

class Chao(pygame.sprite.Sprite):
    def __init__(self, largura, altura, i, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = spriteSheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.x = 64 * i
        self.rect.y = altura - 64
        self.largura = largura
        self.vel = vel

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = self.largura
        self.rect.x -= self.vel