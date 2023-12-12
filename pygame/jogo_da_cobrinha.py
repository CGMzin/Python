#encoding: utf-8
import pygame
from pygame.locals import *
from sys import exit
from random import * 

pygame.init()
dnv = True
clicou = False

largura = 640
altura = 480
vivo = True

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da cobrinha")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', 25, True, True)
while dnv:
    lista_cobra = []
    comprimento_cobra = 3
    pontos = 0
    x = 20
    y = 0
    x_cobra = (largura/2 - 10) - ((largura/2 - 10) % 20)
    y_cobra = (altura/2 - 10) - ((altura/2 - 10) % 20)
    x_aleatorio = randint(40, 600) 
    y_aleatorio = randint(40, 430) 
    x_maca = x_aleatorio - (x_aleatorio % 20)
    y_maca = y_aleatorio - (y_aleatorio % 20)

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_r:
                    vivo = True

    def aumentarCobra(lista_cobra):
        for XeY in lista_cobra:
            pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))

    while vivo:
        clock.tick(5    )
        tela.fill((255, 255, 255))
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
                            x = -20
                            y = 0
                            clicou = True
                    if event.key == K_d or event.key == K_RIGHT:
                        if x >= 0:
                            x = 20
                            y = 0
                            clicou = True
                    if event.key == K_w or event.key == K_UP:
                        if y <= 0:
                            y = -20
                            x = 0
                            clicou = True
                    if event.key == K_s or event.key == K_DOWN:
                        if y >= 0:
                            y = 20
                            x = 0
                            clicou = True
                    
        clicou = False
        '''if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
            x_cobra -= 20
        if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
            x_cobra += 20
        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
            y_cobra -= 20
        if pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_DOWN]:
            y_cobra += 20'''            
        x_cobra += x
        y_cobra += y

        if x_cobra > 620:
            x_cobra = 0
        if x_cobra < 0:
            x_cobra = 620
        if y_cobra > 460:
            y_cobra = 0
        if y_cobra < 0: 
            y_cobra = 460

        cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 20, 20))
        maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

        if cobra.colliderect(maca):
            x_aleatorio = randint(40, 600) 
            y_aleatorio = randint(40, 430) 
            x_maca = x_aleatorio - (x_aleatorio % 20)
            y_maca = y_aleatorio - (y_aleatorio % 20)
            pontos += 1
            comprimento_cobra +=1

        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)

        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        aumentarCobra(lista_cobra)
        tela.blit(msgForm, (500,10))

        if lista_cobra.count(lista_cabeca) > 1:
            vivo = False
            tela.fill((255, 255, 255))
            tela.blit(fonte.render("Você morreu, Aperte R para jogar novamente", True, (0, 0, 0)), (50, 210))

        pygame.display.update()