#encoding: utf-8
import pygame
from pygame.locals import *

class Cobra(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = []
        self.imgs.append(pygame.image.load('testes_pygame/jogoCobrinhaPOO/sprites/spritesCobrinha/dir_1.png'))
        self.imgs.append(pygame.image.load('testes_pygame/jogoCobrinhaPOO/sprites/spritesCobrinha/dir_2.png'))
        self.imgs.append(pygame.image.load('testes_pygame/jogoCobrinhaPOO/sprites/spritesCobrinha/dir_3.png'))
        self.imgs.append(pygame.image.load('testes_pygame/jogoCobrinhaPOO/sprites/spritesCobrinha/dir_4.png'))
        self.atual = 1
        self.image = self.imgs[self.atual]
        self.image = pygame.transform.scale(self.image, ((scale + 10) , (scale + 10)))
        self.scale = scale
        self.x = x
        self.y = y

        self.radius = scale / 2

        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def cima(self):
        self.atual = 0

    def direita(self):
        self.atual = 1

    def baixo(self):
        self.atual = 2

    def esquerda(self):
        self.atual = 3

    def update(self):
        self.rect.topleft = self.x, self.y
        self.image = self.imgs[self.atual]
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))