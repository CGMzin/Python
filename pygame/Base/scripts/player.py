import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, img, pos, z, collision_sprite, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.zLayer = z

        self.collision_sprite = collision_sprite

        self.direction = pygame.math.Vector2()
        self.speed = 3

        self.frame = 0
        
        self.status = 'idle'
        self.look = 'right'
        
    def action(self):
        if self.direction.x != 0 or self.direction.y != 0:
            self.status = 'walk'
        else:
            self.status = 'idle'
            
        if self.status == 'idle':
            self.animation("pygame/Base/assets/player/idle", 0.1, 2)
        elif self.status == 'walk':
            self.animation("pygame/Base/assets/player/Walkright", 0.2, 2)
            
        if self.look == 'right':
            self.image = pygame.transform.flip(self.image, False, False)
        elif self.look == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

    def collide(self, path):
        if path == 'horizontal':
            for sprite in self.collision_sprite:
                if sprite.rect.colliderect(self.rect):
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

    def animation(self, path, speed, limit):
        self.frame = (self.frame + speed) % limit
        self.image = pygame.image.load(f'{path}{int(self.frame)}.png').convert_alpha()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.look = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.look = 'left'
        elif keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            
            self.direction.x = 0
            self.direction.y = 0


    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collide('horizontal')
        
        self.rect.y += self.direction.y * self.speed
        self.collide('vertical')

    def update(self):
        self.action()
        self.input()
        self.move()
