#encoding: utf-8
import pygame
from pygame.locals import *
from random import * 

class Maca(pygame.sprite.Sprite):
    def __init__(self, scale, screenW, screenH):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('testes_pygame\jogoCobrinhaPOO\sprites\spritesMaca\maca3.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.scale = scale
        self.screenW = screenW
        self.screenH = screenH
        self.xA = randint(scale, (screenW - scale)) 
        self.yA = randint(scale, (screenH - scale)) 
        self.x = self.xA - (self.xA % scale)
        self.y = self.yA - (self.yA % scale)

        self.radius = scale / 2

        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def novo(self):
        self.xA = randint(self.scale, (self.screenW - self.scale)) 
        self.yA = randint(self.scale, (self.screenH - self.scale)) 
        self.x = self.xA - (self.xA % self.scale)
        self.y = self.yA - (self.yA % self.scale)

    def update(self):
        self.rect.topleft = self.x, self.y
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))