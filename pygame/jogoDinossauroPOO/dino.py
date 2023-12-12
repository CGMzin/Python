#encoding: utf-8
import pygame
from pygame.locals import *
import os

dirPrinc = os.path.dirname(__file__)
dirImg = os.path.join(dirPrinc, 'sprites')
spriteSheet = pygame.image.load(os.path.join(dirImg, 'dinoSpritesheet.png'))

class Dino(pygame.sprite.Sprite):
    def __init__(self, altura):
        pygame.sprite.Sprite.__init__(self)
        
        self.imgDino = []
        for i in range(3):
            img = spriteSheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imgDino.append(img)

        self.index = 0
        self.image = self.imgDino[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.Yini = altura - 64 - 96 // 2
        self.rect.center = [100, altura - 64]
        self.altura = altura
        self.pulo = False

    def update(self):
        if self.pulo == True:
            if self.rect.y <= self.altura - 220:
                self.pulo = False
            else:
                self.rect.y -= 15
        else:
            if self.rect.y < self.Yini:
                self.rect.y += 15
            else:
                self.rect.y = self.Yini

            
        if self.index > 2:
            self.index = 0
        self.index += 0.25
        self.image = self.imgDino[int(self.index)]

    def pular(self):
        self.pulo = True