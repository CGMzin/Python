#encoding: utf-8
import pygame
from pygame.locals import *
from sys import exit
import random
import dino as dn
import nuvem as nv
import chao as ch
import cacto as ct
import dinoVoador as dv

pygame.init()

largura = 640
altura = 400

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do dinossauro")

branco = (255, 255, 255)

obstaculo = random.choice([0, 1])

pontos = 2000
vel = 30
colidiu = False

def exibirMensagem(msg, tamanho, cor):
    '''Retorna o texto formatado.'''
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    txtForm = fonte.render(mensagem, True, cor)
    return txtForm

def reiniciarJogo():
    global vel, pontos, colidiu, obstaculo
    vel = 10
    pontos = 0
    colidiu = False
    dinoVoador.rect.x = largura
    cacto.rect.x = largura
    dino.rect.y = dino.Yini
    obstaculo = random.choice([0, 1])
    dino.pulo = False

todasSprites = pygame.sprite.Group()
dino = dn.Dino(altura)
todasSprites.add(dino)

for i in range(4):
    nuvem = nv.Nuvem(largura, vel)
    todasSprites.add(nuvem)

for i in range(20):
    chao = ch.Chao(largura, altura, i,vel)
    todasSprites.add(chao)

cacto = ct.Cacto(largura, altura, obstaculo, vel)
todasSprites.add(cacto)

dinoVoador = dv.DinoVoador(largura, obstaculo, vel)
todasSprites.add(dinoVoador)

spritesObstaculos = pygame.sprite.Group()
spritesObstaculos.add(cacto)
spritesObstaculos.add(dinoVoador)

clock = pygame.time.Clock()
while True:
    clock.tick(20)
    tela.fill(branco)

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
             
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    if dino.rect.y == altura - 64 - 96 // 2:
                        dino.pular()

                if event.key == K_r and colidiu == True:
                    reiniciarJogo()
            
    colisao = pygame.sprite.spritecollide(dino, spritesObstaculos, False, pygame.sprite.collide_mask)
        
    todasSprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dinoVoador.rect.topright[0] <= 0:
        obstaculo = random.randint(0, 1)
        cacto.rect.x = largura
        dinoVoador.rect.x = largura
        cacto.obs = obstaculo
        dinoVoador.obs = obstaculo

    if colisao:
        colidiu = True
        if pontos % 100 == 0:
            pontos += 1
                                                
        tela.blit(exibirMensagem(f'GAME OVER', 40, (0, 0, 0)), (200, 120))
        tela.blit(exibirMensagem(f'Pressione R para reiniciar', 20, (0, 0, 0)), (200, 180))

    else:
        pontos += 1
        todasSprites.update()
        txtPontos = exibirMensagem(f"pontos: {pontos}", 25, (0, 0, 0))

    if pontos % 100 == 0 and pontos <= 2500:
        vel += 1
        nuvem.vel = vel
        dinoVoador.vel = vel
        cacto.vel = vel

    tela.blit(txtPontos, (430, 10))

    pygame.display.flip()
