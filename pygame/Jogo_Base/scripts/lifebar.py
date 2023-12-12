import pygame
from scripts.settings import *

spriteSheet = pygame.image.load('pygame/Jogo_Base/assets/enemies/monster_lifebar-removebg-preview.png')

class Lifebar(pygame.sprite.Sprite):

    def __init__(self, pos, z, life, *groups):
        super().__init__(*groups)
        
        self.images = []
        for i in range(5):
            img = pygame.transform.scale_by(spriteSheet.subsurface((28, i*35 + 22), (166, 35)), 0.25)
            self.images.append(img)
        self.image = self.images[0]
        
        self.rect = self.image.get_rect(topleft=(pos[0] - 10, pos[1] -10))
            
        self.zLayer = z
        
        self.life = life


    def verify(self, life):
        if life <= self.life/5:
            self.image = self.images[4]
        elif life <= (self.life/5) * 2:
            self.image = self.images[3]
        elif life <= (self.life/5) * 3:
            self.image = self.images[2]
        elif life <= (self.life/5) * 4:
            self.image = self.images[1]
        else:
            self.image = self.images[0]  