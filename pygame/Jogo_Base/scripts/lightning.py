import pygame
from scripts.settings import *

spriteSheet = pygame.image.load('pygame/Jogo_Base/assets/player/lightning.png')

class Lightning(pygame.sprite.Sprite):
    def __init__(self, pos, z, mpos, *groups):
        super().__init__(*groups)
        
        self.images = []
        for i in range (3):
            for i in range(4):
                img = pygame.transform.rotate(spriteSheet.subsurface((0, i*32), (128, 32)), 90)
                self.images.append(img)
        self.image = self.images[0]
        
        if pos[0] < WIDTH / 2 and pos[1] < HEIGHT / 2:
            self.rect = self.image.get_rect(midbottom=mpos)
        elif pos[0] < WIDTH / 2:
            self.rect = self.image.get_rect(midbottom=(mpos[0], mpos[1] + (pos[1] - HEIGHT / 2)))
        elif pos[1] < HEIGHT / 2:
            self.rect = self.image.get_rect(midbottom=(mpos[0] + (pos[0] - WIDTH / 2), mpos[1]))
        else:
            self.rect = self.image.get_rect(midbottom=(mpos[0] + (pos[0] - WIDTH / 2), mpos[1] + (pos[1] - HEIGHT / 2)))
        
        self.zLayer = z

        self.rect.size = (32, 128)
        
        self.speed = 2
        self.frame = 0
        self.delay = 0
    
    def collide(self):
        pass
        
    def animation(self, list, speed, limit):
        self.frame = (self.frame + speed) % limit
        self.image = list[int(self.frame)]
        if self.frame > limit - (speed * 2):
            self.collide()
            self.rect.x = 1000000

    def update(self):
        self.animation(self.images, 0.2, 12)