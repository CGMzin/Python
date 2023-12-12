import pygame
from scripts.player import Player
from scripts.obj import Obj
from scripts.camera import Camera
from scripts.settings import WORDMAP, TILESET, LAYERS

class Scene:

    def __init__(self):

        self.display = pygame.display.get_surface()
        self.show_sprites = Camera()
        self.collisions_sprite = pygame.sprite.Group()

        self.createMap()
        self.player = Player("pygame/Base/assets/player/idle0.png", [64, 64], LAYERS['player'], self.collisions_sprite, [self.show_sprites])

    def createMap(self):
        for i, row in enumerate(WORDMAP):
            for j, col in enumerate(row):
                x = j * TILESET
                y = i * TILESET

                if col == "X":
                    Obj('pygame/Base/assets/tiles/block.png', (x, y), LAYERS['block'], [self.show_sprites, self.collisions_sprite])
                elif col == "g":
                    Obj('pygame/Base/assets/tiles/ground.png', (x, y), LAYERS['ground'], [self.show_sprites])

    def run(self):
        
        self.show_sprites.costumDraw(self.player)
        self.show_sprites.update()