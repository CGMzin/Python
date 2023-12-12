#encoding: utf-8
import pygame
from pygame.locals import *
from sys import exit
import comBorda as borda
import semBorda as sborda
pygame.init()

largura = 640
altura = 480

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da cobrinha")
fonte = pygame.font.SysFont('arial', 25, True, True)
clock = pygame.time.Clock()

while True:
    clock.tick(7)
    tela = pygame.display.set_mode((largura, altura))
    tela.fill((255, 255, 255))

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_1:
                    sborda.jogo()
                if event.key == K_2:
                    borda.jogo()

    msg1 = fonte.render("ESCOLHA O MODO DE JOGO", True, (0, 0, 0))
    msg2 = fonte.render("Sem borda - Pressione 1", True, (0, 0, 0))
    msg3 = fonte.render("Com borda - Pressione 2", True, (0, 0, 0))
    tela.blit(msg1, (140, 100))
    tela.blit(msg2, (170, 215))
    tela.blit(msg3, (170, 265))


    pygame.display.update()
