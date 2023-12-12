import pygame, random, datetime
from scripts.lifebar import Lifebar

class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, z, collision_sprite, show_sprite, spritesheet, *groups):
        super().__init__(*groups)
        
        self.ss = spritesheet
        self.spriteSheet = pygame.image.load(self.ss[0])
        
        self.idles = []
        for i in range(4):
            img = self.spriteSheet.subsurface((i*32, 0), (32, 32))
            self.idles.append(img)
        self.image = self.idles[0]
        
        self.walks = []
        for i in range(spritesheet[1]):
            img = self.spriteSheet.subsurface((i*32, 32), (32, 32))
            self.walks.append(img)
            
        self.hits = []
        for i in range(4):
            img = self.spriteSheet.subsurface((i*32, 64), (32, 32))
            self.hits.append(img)
            
        self.dies = []
        for i in range(4):
            img = self.spriteSheet.subsurface((i*32, 96), (32, 32))
            self.dies.append(img)
        
        self.rect = self.image.get_rect(topleft=pos)
        self.zLayer = z

        self.now = datetime.datetime.now()

        self.rect.size = (32, 32)

        self.collision_sprite = collision_sprite

        self.direction = pygame.math.Vector2()
        self.speed = 1.5

        self.life = 10
        self.dead = False
        self.hit = False
        self.attacking = False
        self.dying = False

        self.frame = 0
        
        self.status = 'idle'
        self.look = 'right'
        self.isimg = False
        self.count = 0
        self.see = False
        self.ppos = []
        self.cooldown = datetime.datetime.now() 
        
        self.lifebar = Lifebar(self.rect.topleft, 4, 10, show_sprite)
        
    def action(self):            
        if self.status == 'idle':
            if self.ss[1] == 4:
                self.animation(self.idles, 0.2, 4)
            else:
                self.animation(self.idles, 0.1, 4)
        elif self.status == 'walk':
            if self.count <= 3:
                self.animation(self.walks, 0.3, self.ss[1])
            else:
                self.status = 'idle'
                self.count = 0
                self.now = datetime.datetime.now()
        elif self.status == 'attack':
            self.speed = 1
            if not self.isimg and self.attacking:
                self.animation(self.hits, 0.4, 4)
                self.speed = 0
            else:
                self.attacking = False
                self.animation(self.walks, 0.3, self.ss[1])
            if abs(self.rect.centerx - self.ppos[0][0]) < 20 and abs(self.rect.centery - self.ppos[0][1]) < 20 and self.cooldown + datetime.timedelta(seconds=2) < datetime.datetime.now() and not self.attacking:
                self.hit = True
                self.attacking = True
                self.isimg = False
                self.frame = 0
                self.see = False
                self.cooldown = datetime.datetime.now()
            self.status = 'idle'
        elif self.status == 'dead':
            if not self.isimg and self.dying:
                self.animation(self.dies, 0.1, 4)
            else:
                self.rect.x = 1000000
                self.dead = True

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
                        
    def get_hit(self, dmg):
        self.life -= dmg
        
    def animation(self, list, speed, limit):
        if self.frame == 0:
            pass
            #rodar som 
        self.frame = (self.frame + speed) % limit
        
        if self.frame > limit - speed:
            self.isimg = True
            self.frame = limit - speed
        
            if self.status == 'walk':
                self.count += 1
        else:
            self.isimg = False
            
        if self.look == 'right':
            self.image = list[int(self.frame)]
        elif self.look == 'left':
            self.image = pygame.transform.flip(list[int(self.frame)], True, False)

    def think(self):
        self.speed = 1.5
        if not self.dead and self.now + datetime.timedelta(seconds=random.randint(5, 15)) < datetime.datetime.now() and self.status != 'walk':
            keys = [1, 2, 3, 4, 5, 6, 7, 8]
            key = random.choice(keys)
                
            if not self.see:
                if key == 1 or key == 5 or key == 6:
                    self.direction.x = 1
                    self.look = 'right'
                elif key == 2 or key == 7 or key == 8:
                    self.direction.x = -1
                    self.look = 'left'
                else:
                    self.direction.x = 0
                    
                if key == 3 or key == 5 or key == 8:
                    self.direction.y = -1
                elif key == 4 or key == 6 or key == 7:
                    self.direction.y = 1
                else:
                    self.direction.y = 0
            
            acts = [0, 1]
            act = random.choice(acts)
            
            if act == 0:
                self.status = 'walk'
            elif act == 1:
                self.status = 'idle'
                self.direction.x = 0
                self.direction.y = 0      
                    
    def find(self, pos):
        if self.life > 0:
            
            self.status = 'attack'
            self.see = True
            for _ in self.ppos:
                self.ppos.pop()
            self.ppos.append(pos)
            
            if abs(self.rect.centerx - pos[0]) < 10:
                self.direction.x = 0
            elif self.rect.centerx > pos[0]:
                self.direction.x = -1
                self.look = 'left'
            else:
                self.direction.x = 1
                self.look = 'right'
                
            if abs(self.rect.centery - pos[1]) < 10:
                self.direction.y = 0
            elif self.rect.centery > pos[1]:
                self.direction.y = -1
            else:
                self.direction.y = 1

    def move(self):
        if self.status == 'walk' or (self.see and not self.attacking):
            self.rect.x += self.direction.x * self.speed
            if self.ss[2] != 'bat':
                self.collide('horizontal')
            
            self.rect.y += self.direction.y * self.speed
            if self.ss[2] != 'bat':
                self.collide('vertical')
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def check_life(self):
        if self.life <= 0:
            self.see = True
            self.direction.x = 0
            self.direction.y = 0
            self.speed = 1
            self.status = 'dead'
            self.dying = True
            self.lifebar.rect.x = 100000000

    def update(self):
        if self.see == False:
            self.think()
        self.action()
        if not self.dead:
            self.move()
            self.see = False
            self.lifebar.rect.topleft = (self.rect.topleft[0] - 10, self.rect.topleft[1] -10)
            self.lifebar.verify(self.life)
            self.ppos = []
        self.check_life()
