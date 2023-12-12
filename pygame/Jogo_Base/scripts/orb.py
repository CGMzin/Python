import pygame
from scripts.settings import *

spriteSheet = pygame.image.load('pygame/Jogo_Base/assets/player/magic_spell.png')

class Orb(pygame.sprite.Sprite):

    def __init__(self, pos, z, collision_sprite, mpos, look, monsters, *groups):
        super().__init__(*groups)
        
        self.images = []
        for i in range(4):
            img = spriteSheet.subsurface((i*32, 0), (32, 32))
            self.images.append(img)
        self.image = self.images[0]
        
        if look == 'left':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-20))
        else: 
            self.rect = self.image.get_rect(topleft=(pos[0] - 10, pos[1]-20))
        self.zLayer = z
        

        self.rect.size = (32, 32)
        
        self.monsters = monsters

        self.collision_sprite = collision_sprite

        self.direction = pygame.math.Vector2()
        
        self.screen_end_x = (len(WORDMAP_LETTERS[0]) - 1) * TILESET
        self.screen_end_y = (len(WORDMAP_LETTERS) - 1 ) * TILESET
        
        if pos[0] < WIDTH / 2 and pos[1] < HEIGHT / 2:
            self.mpos = mpos
        elif pos[0] < WIDTH / 2:
            self.mpos = (mpos[0], mpos[1] + (pos[1] - HEIGHT / 2))
            if pos[1] > self.screen_end_y - HEIGHT / 2:
                self.mpos = (mpos[0], self.screen_end_y - abs(HEIGHT - mpos[1]))
        elif pos[1] < HEIGHT / 2:
            self.mpos = (mpos[0] + (pos[0] - WIDTH / 2), mpos[1])
            if pos[0] > self.screen_end_x - WIDTH / 2:
                self.mpos = (self.screen_end_x - abs(WIDTH - mpos[0]), mpos[1])
        elif pos[0] > self.screen_end_x - WIDTH / 2 and pos[1] > self.screen_end_y - HEIGHT / 2:
            self.mpos = (self.screen_end_x - abs(WIDTH - mpos[0]), self.screen_end_y - abs(HEIGHT - mpos[1]))
        elif pos[0] > self.screen_end_x - WIDTH / 2:
            self.mpos = (self.screen_end_x - abs(WIDTH - mpos[0]), mpos[1] + (pos[1] - HEIGHT / 2))
        elif pos[1] > self.screen_end_y - HEIGHT / 2:
            self.mpos = (mpos[0] + (pos[0] - WIDTH / 2), self.screen_end_y - abs(HEIGHT - mpos[1]))
        else:
            self.mpos = (mpos[0] + (pos[0] - WIDTH / 2), mpos[1] + (pos[1] - HEIGHT / 2))
        
        if abs(self.mpos[0] - pos[0]) < 55 and abs(self.mpos[1] - pos[1]) < 55:
            if self.mpos[0] > pos[0]:
                self.direction.x = 1
            else:
                self.direction.x = -1
                
            if self.mpos[1] > pos[1]:
                self.direction.y = 1
            else:
                self.direction.y = -1
        else:    
            if abs(self.mpos[0] - pos[0]) < 55:
                self.direction.x = 0
            elif self.mpos[0] > pos[0]:
                self.direction.x = 1
            else:
                self.direction.x = -1
                
            if abs(self.mpos[1] - pos[1]) < 55:
                self.direction.y = 0
            elif self.mpos[1] > pos[1]:
                self.direction.y = 1
            else:
                self.direction.y = -1
        
        self.speed = 3
        self.frame = 0
        
    def animation(self, list, speed, limit):
        self.frame = (self.frame + speed) % limit
        self.image = list[int(self.frame)]

    def move(self):
        self.rect.x += self.direction.x * self.speed  
        self.rect.y += self.direction.y * self.speed
        self.animation(self.images, self.speed, 4)
        
    def collide(self):
        pass
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def update(self):
        self.move()