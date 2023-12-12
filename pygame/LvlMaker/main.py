import pygame, sys, random
from settings import *
from obj import Obj

# --------- ARRUMAR SCROLL ------------

#get images
img_paths = ['pygame/Jogo_Base/assets/tiles0/', 'pygame/Jogo_Base/assets/tiles1/']
game_tiles = []
for l in range(len(img_paths)):
    for j in range(1000):
        try:
            img = pygame.transform.scale(pygame.image.load(f"{img_paths[l]}tile_{str(j).zfill(4)}.png"), (16, 16))
            game_tiles.append([img, 0, f"{img_paths[l]}tile_{str(j).zfill(4)}.png"])
        except:
            pass
        
    for i in range(len(game_tiles)):
        if i%5 == 0: 
            for j in range(5):
                try:
                    game_tiles[i+j][1] = game_tiles[i+j][0].get_rect(topleft=(((j/2) * 64) + 20, ((i/5) * 64) + 200))
                except:
                    pass


pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
exp_sprites = []
for i in range(40):
    new_row = []
    for j in range(60):
        new_row.append("")
    exp_sprites.append(new_row)
actual = None

#ToolBar
toolbar0 = pygame.Surface(BAR_TOOLS_0_SIZE)
toolbar0.fill(BG_COLOR)

toolbar1 = pygame.Surface(BAR_TOOLS_1_SIZE)
toolbar1.fill(BG_COLOR)

toolbar2 = pygame.Surface(BAR_TOOLS_2_SIZE)
toolbar2.fill(BG_COLOR)

#Canvas
canvas = pygame.Surface(CANVAS_SIZE)
canvas.fill(BG_COLOR)

#TileList
tilelist = pygame.Surface((160, 500))
tilelist.fill(TILELIST_COLOR)
trect = tilelist.get_rect(topleft=(10, 180))

#Buttons
pencil = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/pencilrb.png'), (48, 48))
pencil_rect = pencil.get_rect(topleft=(25, 25))

eraser = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/eraserrb.png'), (48, 48))
eraser_rect = eraser.get_rect(topleft=(110, 25))

file_code = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/file-coderb.png'), (48, 48))
file_code_rect = file_code.get_rect(topleft=(25, 110))

bucket = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/bucketrb.png'), (48, 48))
bucket_rect = bucket.get_rect(topleft=(110, 110))

#Tools
status = ''
drawning = False
size = 16
color = 'white'
x = 0
y = 0

def fill_all():
    global exp_sprites
    if actual != None:
        exp_sprites = []
        for sprite in all_sprites:    
            sprite.erase()
            all_sprites.remove(sprite)
        
        for i in range((int(CANVAS_SIZE[1] / size))):
            new_row = []
            for j in range((int(CANVAS_SIZE[0] / size))):
                Obj(actual[0], (256 + (j * size), 40 + (i * size)), [all_sprites])
                new_row.append(actual[1])
            exp_sprites.append(new_row)
                
while True:
    display.fill((0, 0, 0))
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if ev.type == pygame.MOUSEBUTTONDOWN:
            x = ev.pos[0]
            y = ev.pos[1]
            if ev.button == 1:
                if pencil_rect.collidepoint(x, y):
                    status = 'draw'
                elif eraser_rect.collidepoint(x, y):
                    status = 'erase'
                elif bucket_rect.collidepoint(x, y):
                    fill_all()
                elif file_code_rect.collidepoint(x, y):
                    num = 0
                    with open('pygame\LvlMaker\output\len.txt', 'r') as file:
                        num = int(file.read())
                        
                    with open(f'pygame\LvlMaker\output\map{num+1}.txt', 'w') as file:
                        paths = []
                        for i in range(40):
                            for j in range(60):
                                if exp_sprites[i][j] not in paths:
                                    paths.append(exp_sprites[i][j])
                                    
                        opt = LETTERS
                        letters = []
                        for i in range(len(paths)):
                            letter = random.choice(opt)
                            letters.append(letter)
                            opt.remove(letter)
                            
                        file.write('WORDMAP_LETTERS = [')
                        exp_letters = exp_sprites
                        for i in range(40):
                            file.write('[')
                            for j in range(60):  
                                file.write(f'"{letters[paths.index(exp_sprites[i][j])]}"' + ",")
                            file.write('],\n')
                        file.write(']')
                            
                        file.write('\n\n\n')
                            
                             
                        file.write('WORDMAP_PATHS = {')
                        for i in range(len(paths)):
                            file.write(f'"{letters[i]}": ["{paths[i]}", "ground"],\n')
                        file.write('}')
                            
                    with open('pygame\LvlMaker\output\len.txt', 'w') as file:
                        file.write(str(num + 1))
                        
                for tile in game_tiles:
                        if tile[1].collidepoint(x, y):
                            actual = [tile[0], tile[2]]
                drawning = True
            if ev.button == 4: 
                if trect.collidepoint(x, y) and game_tiles[0][1].y < 180:
                    for tile in game_tiles:
                        tile[1].y += 32
            if ev.button == 5 and game_tiles[-1][1].y > 680: 
                if trect.collidepoint(x, y):
                    for tile in game_tiles:
                        tile[1].y -= 32
                
                
        if ev.type == pygame.MOUSEMOTION:
            x = ev.pos[0]
            y = ev.pos[1]
            if pencil_rect.collidepoint(x, y):
                pencil = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/pencil_white.png'), (48, 48))
            else:
                pencil = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/pencilrb.png'), (48, 48))
                
            if eraser_rect.collidepoint(x, y):
                eraser = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/eraser_white.png'), (48, 48))
            else:
                eraser = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/eraserrb.png'), (48, 48))
                
            if file_code_rect.collidepoint(x, y):
                file_code = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/file-code_white.png'), (48, 48))
            else:
                file_code = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/file-coderb.png'), (48, 48))
            
            if bucket_rect.collidepoint(x, y):
                bucket = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/bucket_white.png'), (48, 48))
            else:
                bucket = pygame.transform.scale(pygame.image.load('pygame/LvlMaker/assets/menu/bucketrb.png'), (48, 48))
                        
        if ev.type == pygame.MOUSEBUTTONUP:
            drawning = False
                
    if status == 'draw' and drawning: 
        if actual != None:
            objects = None
            can = True
            canvas_rect = canvas.get_rect(topleft=(256, 40))
            offsetx = x - (x % size)
            if (y % size) > 6:
                offsety = y - (y % size) + size
            else:
                offsety = y - (y % size)
                
            for sprite in all_sprites:
                    if sprite.rect.collidepoint(offsetx, offsety):      
                        sprite.erase()
                        all_sprites.remove(sprite)
                
            if canvas_rect.collidepoint(offsetx, offsety):
                if len(all_sprites) != 0:
                    for sprite in all_sprites:
                        if sprite.rect.collidepoint(offsetx, offsety):      
                            can = False
                    if can:
                        obj = Obj(actual[0], (offsetx, offsety - size / 2), [all_sprites]) 
                        objects = [obj]
                else:
                    obj = Obj(actual[0], (offsetx, offsety - size / 2), [all_sprites])
                    objects = [obj]
                    if objects != None:
                        exp_sprites[int((int(offsety - size / 2) - 40) / size)][int((int(offsetx) - 256) / size)] = actual[1]
                
                if objects != None and can:
                    exp_sprites[int((int(offsety - size / 2) - 40) / size)][int((int(offsetx) - 256) / size)] = actual[1] 
                        
    if status == 'erase' and drawning: 
        have = True
        canvas_rect = canvas.get_rect(topleft=(256, 40))
        offsetx = x - (x % size)
        if (y % size) > 6:
            offsety = y - (y % size) + size
        else:
            offsety = y - (y % size)
        if canvas_rect.collidepoint(offsetx, offsety):
            if len(all_sprites) != 0:
                for sprite in all_sprites:
                    if sprite.rect.collidepoint(offsetx, offsety):      
                        sprite.erase()
                        all_sprites.remove(sprite)
            
    display.blit(toolbar1, (0, 180))
    display.blit(canvas, (256, 40))
    display.blit(tilelist, trect)
    for i in range(len(game_tiles)):
        display.blit(game_tiles[i][0], game_tiles[i][1])
    display.blit(toolbar0, (0, 0))
    display.blit(toolbar2, (0, 680))
    all_sprites.draw(display)
    display.blit(pencil, pencil_rect)
    display.blit(eraser, eraser_rect)
    display.blit(file_code, file_code_rect)
    display.blit(bucket, bucket_rect)
    pygame.display.update()