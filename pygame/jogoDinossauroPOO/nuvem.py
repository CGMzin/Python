#encoding: utf-8
import pygame
from pygame.locals import *
import os
import random

dirPrinc = os.path.dirname(__file__)
dirImg = os.path.join(dirPrinc, 'sprites')
spriteSheet = pygame.image.load(os.path.join(dirImg, 'dinoSpritesheet.png'))

class Nuvem(pygame.sprite.Sprite):
    def __init__(self, largura, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = spriteSheet.subsurface((7*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(largura, largura * 2)
        self.rect.y = random.randrange(0, 150, 30)
        self.largura = largura
        self.vel = vel

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = random.randint(self.largura, self.largura * 2)
            self.rect.y = random.randrange(0, 150, 30)
        self.rect.x -= self.vel