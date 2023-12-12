import pygame, datetime
from scripts.settings import *
from scripts.orb import Orb
from scripts.lightning import Lightning

pygame.mixer.init()
passo = pygame.mixer.Sound('pygame/Jogo_Base/assets/sounds/passo.wav')
agua = pygame.mixer.Sound('pygame/Jogo_Base/assets/sounds/boladeagua.wav')

spriteSheet = pygame.image.load('pygame/Jogo_Base/assets/player/wizard.png')
spriteSheetLife = pygame.image.load('pygame/Jogo_Base/assets/enemies/monster_lifebar-removebg-preview.png')

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, z, collision_sprite, monsters, *groups):
        super().__init__(*groups)
        
        self.idles = []
        for i in range(4):
            img = spriteSheet.subsurface((i*32, 32), (32, 32))
            self.idles.append(img)
        self.image = self.idles[0]
   
        self.lifebar = []
        for i in range(5):
            img = spriteSheetLife.subsurface((28, i*35 + 22), (166, 35))
            self.lifebar.append(img)
        self.lifebarimg = self.lifebar[0]
        
        self.walks = []
        for i in range(8):
            img = spriteSheet.subsurface((i*32, 64), (32, 32))
            self.walks.append(img)
            
        self.hits = []
        for i in range(4):
            img = spriteSheet.subsurface((i*32, 96), (32, 32))
            self.hits.append(img)
            
        self.power = []
        for i in range(7):
            img = spriteSheet.subsurface((i*32, 128), (32, 32))
            self.power.append(img)
        for _ in range(2):
            for i in range(1, 4):
                img = spriteSheet.subsurface((i*32 + 96, 128), (32, 32))
                self.power.append(img)
            
        self.dies = []
        for i in range(4):
            img = spriteSheet.subsurface((i*32, 160), (32, 32))
            self.dies.append(img)
        
        self.rect = self.image.get_rect(topleft=pos)
        self.zLayer = z
        
        self.monsters = monsters

        self.rect.size = (32, 32)

        self.collision_sprite = collision_sprite

        self.direction = pygame.math.Vector2()
        self.speed = 2
        self.life = 10

        self.frame = 0
        
        self.status = 'idle'
        self.look = 'right'
        self.imgname = 'right'
        self.isimg = False
        self.mana = 20
        self.count = 0
        self.mpos = [(0, 0)]
        self.pos = [(0, 0)]
        self.now = datetime.datetime.now()
        self.block = ''
        self.waiting = False
        
        self.spells = pygame.sprite.Group()
        self.lightnings = pygame.sprite.Group()
        self.screen_end_x = (len(WORDMAP_LETTERS[0]) - 1) * TILESET
        
        self.fonte = pygame.font.get_default_font()             
        self.fontesys = pygame.font.SysFont(self.fonte, 40)
        self.txt = self.fontesys.render(f"Mana: {int(self.mana)}", True, (255,255,255))  
        
    def action(self):
        if self.direction.x != 0 or self.direction.y != 0:
            self.status = 'walk'
        elif self.status != 'attack' and self.status != 'lightning':
            self.status = 'idle'
            
        if self.waiting and self.now + datetime.timedelta(seconds=2) < datetime.datetime.now():
            lightning = Lightning(self.pos[0], 3, self.mpos[0], self.groups())
            self.lightnings.add(lightning)
            self.waiting = False
        
        if self.status == 'idle':
            self.animation(self.idles, 0.1, 4)
        elif self.status == 'walk':
            self.animation(self.walks, 0.2, 8)
            self.status = 'idle'
        elif self.status == 'attack':
            if self.rect.center[0] > WIDTH / 2 and self.rect.center[0] < self.screen_end_x - WIDTH / 2:
                if self.mpos[0][0] + (self.rect.center[0] - WIDTH / 2) < self.rect.center[0]:
                    self.look = 'left'
                else: 
                    self.look = 'right'
            elif self.rect.center[0] > self.screen_end_x - WIDTH / 2:
                if self.screen_end_x - abs(WIDTH - self.mpos[0][0]) < self.rect.center[0]:
                    self.look = 'left'
                else: 
                    self.look = 'right'
            else:
                if self.mpos[0][0] < self.rect.center[0]:
                    self.look = 'left'
                else: 
                    self.look = 'right'
            self.animation(self.hits, 0.2, 4)
            if self.isimg:
                self.status = 'idle'
                self.mana -= 5
                pygame.mixer.Sound.play(agua)
                orb = Orb(self.rect.center, 3, self.collision_sprite, self.mpos[0], self.look, self.monsters, self.groups())
                self.spells.add(orb)
        elif self.status == 'lightning':
            self.animation(self.power, 0.2, 13)
            if self.isimg:
                self.status = 'idle'
                self.mana -= 15
                if self.mpos[0][0] < self.rect.center[0]:
                    self.look = 'left'
                else: 
                    self.look = 'right'

    def collide(self, path):
        if path == 'horizontal':
            for sprite in self.collision_sprite:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        
        if path == 'vertical':                
            for sprite in self.collision_sprite:
                if sprite.rect.colliderect(self.rect):     
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
        
    def animation(self, list, speed, limit):
        self.frame = (self.frame + speed) % limit
        
        if self.status == 'walk':
            self.count += 1
            if self.count == 20:
                pygame.mixer.Sound.play(passo)
                self.count = 0
        
        if self.frame > limit - (speed * 2):
            self.isimg = True
            self.frame = 0
        else:
            self.isimg = False
            
        if self.look == 'right':
            self.image = list[int(self.frame)]
        elif self.look == 'left':
            self.image = pygame.transform.flip(list[int(self.frame)], True, False)
            
    def hit(self, dmg):
        self.life -= dmg
        if self.life <= 2:
            self.lifebarimg = self.lifebar[4]
        elif self.life <= 4:
            self.lifebarimg = self.lifebar[3]
        elif self.life <= 6:
            self.lifebarimg = self.lifebar[2]
        elif self.life <= 8:
            self.lifebarimg = self.lifebar[1]
        else:
            self.lifebarimg = self.lifebar[0]    

    def input(self):
        
        mouse = pygame.mouse.get_pressed()
        
        if self.block == 'left' and not mouse[0]:
            self.block = ''
        if self.block == 'right' and not mouse[2]:
            self.block = ''
        
        if self.status != 'attack' and self.status != 'lightning' and self.block == '':
            if mouse[0] and self.mana >= 5:
                self.status = 'attack'
                self.direction.x = 0
                self.direction.y = 0
                self.mpos.pop()
                self.mpos.append(pygame.mouse.get_pos())   
                self.block = 'left'    
            elif mouse[2] and self.mana >= 15:
                self.now = datetime.datetime.now()
                self.waiting = True
                self.status = 'lightning'
                self.direction.x = 0
                self.direction.y = 0
                self.mpos.pop()
                self.mpos.append(pygame.mouse.get_pos())        
                self.pos.pop()
                self.pos.append(self.rect.center)  
                self.block = 'right'
                    
        
        keys = pygame.key.get_pressed()
            
        if self.status == 'idle':
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.look = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.look = 'left'
            else:
                self.direction.x = 0
                
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0


    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collide('horizontal')
        
        self.rect.y += self.direction.y * self.speed
        self.collide('vertical')
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def update(self):
        self.input()
        self.action()
        self.move()
        if self.mana < 20:
            self.mana += 0.05
        self.txt = self.fontesys.render(f"Mana: {int(self.mana)}", True, (255,255,255))  
