import pygame, random, datetime
from scripts.player import Player
from scripts.obj import Obj
from scripts.camera import Camera
from scripts.enemy_1 import Enemy
from scripts.settings import *

class Scene:

    def __init__(self):

        self.display = pygame.display.get_surface()
        self.show_sprites = Camera()
        self.collisions_sprite = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.end = False
        self.now = datetime.datetime.now()
        self.random = random.randint(5, 15)
        self.enemy_1_ss = [['pygame/Jogo_Base/assets/enemies/skeleton.png', 8, 'skeleton'], ['pygame/Jogo_Base/assets/enemies/goblin.png', 8, 'goblin'], ['pygame/Jogo_Base/assets/enemies/bat.png', 4, 'bat']]

        self.createMap()
        self.player = Player([random.randint(32, 900), random.randint(32, 950)], LAYERS['player'], self.collisions_sprite, self.monsters, [self.show_sprites])
        Enemy([random.randint(32, 900), random.randint(32, 950)], LAYERS['player'], self.collisions_sprite, self.show_sprites, random.choice(self.enemy_1_ss), [self.show_sprites, self.monsters])

    def createMap(self):
        for letter in WORDMAP_PATHS:
            for i, row in enumerate(WORDMAP_LETTERS):
                for j, col in enumerate(row):
                    x = j * TILESET
                    y = i * TILESET
                    if letter == col:
                        if WORDMAP_PATHS[letter][1] == "block":
                            Obj(WORDMAP_PATHS[letter][0], (x, y), LAYERS['block'], [self.show_sprites, self.collisions_sprite])
                        else:
                            Obj(WORDMAP_PATHS[letter][0], (x, y), LAYERS['ground'], [self.show_sprites])
            
        for sprite in self.show_sprites.sprites():
            sprite.image = pygame.transform.scale(sprite.image, (32, 32))
            sprite.rect.size = (32, 32)
        
        for sprite in self.collisions_sprite.sprites():
            sprite.image = pygame.transform.scale(sprite.image, (32, 32))
            sprite.rect.size = (32, 32)

    def run(self):
        self.show_sprites.costumDraw(self.player)
        
        if self.now + datetime.timedelta(seconds=self.random) < datetime.datetime.now():
            self.now = datetime.datetime.now()
            Enemy([random.randint(32, 900), random.randint(32, 950)], LAYERS['player'], self.collisions_sprite, self.show_sprites, random.choice(self.enemy_1_ss),  [self.show_sprites, self.monsters])
        
        for monster in self.monsters:
            if monster.dying:
                self.monsters.remove(monster)
            
            if abs(monster.rect.centerx - self.player.rect.centerx) < 200 and abs(monster.rect.centery - self.player.rect.centery) < 200:
                monster.find(self.player.rect.center)
            
            if monster.hit:
                monster.hit = False
                self.player.hit(1)
                
            if self.player.life <= 0:
                self.end = True
            
            for spell in self.player.spells:
                if monster.get_mask().overlap(spell.get_mask(), (spell.rect.x - monster.rect.x, spell.rect.y - monster.rect.y)):
                    monster.get_hit(5)
                    spell.direction.x = 1
                    spell.rect.x += 1000000
                    self.player.spells.remove(spell)
                    
            for lightning in self.player.lightnings:
                if abs(monster.rect.centerx - lightning.rect.midbottom[0]) < 20 and abs(monster.rect.centery - (lightning.rect.midbottom[1])) < 20:
                    monster.get_hit(10)
                    self.player.lightnings.remove(lightning)
                         
        self.show_sprites.update()
        self.display.blit(self.player.txt, (200, 10))
        self.display.blit(self.player.lifebarimg, (10, 0))