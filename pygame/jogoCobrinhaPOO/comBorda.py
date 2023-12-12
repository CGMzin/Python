#encoding: utf-8
import pygame
from pygame.locals import *
from sys import exit
from random import * 
import cobra as cb
import maca as mc
import time

continua = True

def jogo():
    dnv = True
    clicou = False
    vivo = True

    largura = 400
    altura = 400
    fundo = pygame.image.load('testes_pygame\jogoCobrinhaPOO\grama.jpg')
    fundo = pygame.transform.scale(fundo, (400, 400))

    sprites1 = pygame.sprite.Group()
    cobra = cb.Cobra(120, 120, 40)
    sprites1.add(cobra)
    cobra.direita()

    sprites2 = pygame.sprite.Group()
    maca = mc.Maca(40, largura, altura)
    sprites2.add(maca)

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jogo da cobrinha")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont('arial', 25, True, True)
    while dnv:
        lista_cobra = []
        comprimento_cobra = 3
        pontos = 0
        cobra.x = 120
        cobra.y = 120
        x = 40
        y = 0

        tela.fill((255, 255, 255))

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        vivo = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        dnv = False

        def aumentarCobra(lista_cobra):
            for XeY in lista_cobra:
                pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 40, 40))

        def morrer():
            tela.fill((255, 255, 255))
            tela.blit(fonte.render("VOCÊ MORREU!!", True, (255, 0, 0)), (50, 50))
            tela.blit(fonte.render("Pressione R para jogar novamente", True, (0, 0, 0)), (10, 215))
            tela.blit(fonte.render("Pressione Esc para voltar ao menu", True, (0, 0, 0)), (10, 265))
            time.sleep(3)
            return False

        while vivo:
            clock.tick(2)
            tela.blit(fundo, (0, 0))
            mensagem = f'Pontos: {pontos}'
            msgForm = fonte.render(mensagem, True, (0, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    if clicou == False:
                        if event.key == K_a or event.key == K_LEFT:
                            if x <= 0:
                                x = -40
                                y = 0
                                clicou = True
                                cobra.esquerda()
                        if event.key == K_d or event.key == K_RIGHT:
                            if x >= 0:
                                x = 40
                                y = 0
                                clicou = True
                                cobra.direita()
                        if event.key == K_w or event.key == K_UP:
                            if y <= 0:
                                y = -40
                                x = 0
                                clicou = True
                                cobra.cima()
                        if event.key == K_s or event.key == K_DOWN:
                            if y >= 0:
                                y = 40
                                x = 0
                                clicou = True
                                cobra.baixo()
                        
            clicou = False

            cobra.x += x
            cobra.y += y

            if cobra.x > 400:
                vivo = morrer()
            if cobra.x < -40:
                vivo = morrer()
            if cobra.y > 400:
                vivo = morrer()
            if cobra.y < -40: 
                vivo = morrer()

            aumentarCobra(lista_cobra)
            sprites1.draw(tela)
            sprites2.draw(tela)

            colisao = pygame.sprite.spritecollide(cobra, sprites2, False, pygame.sprite.collide_circle)
            if colisao:
                maca.novo()
                pontos += 1
                comprimento_cobra +=1

            lista_cabeca = [cobra.x, cobra.y]
            lista_cobra.append(lista_cabeca)

            if len(lista_cobra) > comprimento_cobra:
                del lista_cobra[0]

            tela.blit(msgForm, (250,10))

            cobra.update()
            maca.update()
            pygame.display.flip()
            
            if lista_cobra.count(lista_cabeca) > 1:
                vivo = morrer()
                time.sleep(3)