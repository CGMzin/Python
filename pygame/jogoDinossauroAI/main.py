#encoding: utf-8
import pygame, neat, random
from pygame.locals import *
from sys import exit
import dino as dn
import nuvem as nv
import chao as ch
import cacto as ct
import dinoVoador as dv

pygame.init()

LARGURA = 640
ALTURA = 400

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do dinossauro")

BRANCO = (255, 255, 255)

obstaculo = random.randint(0, 3)
ai_jogando = True
pontos = 0
vel = 10

def exibirMensagem(msg, tamanho, cor):
    '''Retorna o texto formatado.'''
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    txtForm = fonte.render(mensagem, True, cor)
    return txtForm

def reiniciarJogo(dinoVoador, cactos):
    global vel, pontos, obstaculo
    vel = 10
    pontos = 0
    for dinv in dinoVoador:
        if dinv.num == 1:
            dinv.rect.x = LARGURA
        else:
            dinv.rect.x = LARGURA + dinv.rect.width

    for cacto in cactos:
        if cacto.num == 1:
            cacto.rect.x = LARGURA
        else:
            cacto.rect.x = LARGURA + cacto.rect.width


def main(genomas, config):
    global vel, pontos, obstaculo
    obstaculo = random.randint(0, 3)
    todasSprites = pygame.sprite.Group()

    if ai_jogando:
        redes = []
        lista_genomas = []
        dinos = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            dino = dn.Dino(ALTURA)
            dinos.append(dino) 
            todasSprites.add(dino)
    else:
        dinos = [dn.Dino(ALTURA)]
        todasSprites.add(dinos[0])

    for i in range(4):
        nuvem = nv.Nuvem(LARGURA, vel)
        todasSprites.add(nuvem)

    for i in range(20):
        chao = ch.Chao(LARGURA, ALTURA, i,vel)
        todasSprites.add(chao)

    cactos = [ct.Cacto(LARGURA, ALTURA, obstaculo, vel, 1), ct.Cacto(LARGURA, ALTURA, obstaculo, vel, 2)]
    todasSprites.add(cactos[0])
    todasSprites.add(cactos[1])

    dinoVoador = [dv.DinoVoador(LARGURA, obstaculo, vel, 1), dv.DinoVoador(LARGURA, obstaculo, vel, 2)]
    todasSprites.add(dinoVoador[0])
    todasSprites.add(dinoVoador[1])

    spritesObstaculos = pygame.sprite.Group()
    spritesObstaculos.add(cactos[0])
    spritesObstaculos.add(cactos[1])
    spritesObstaculos.add(dinoVoador[0])
    spritesObstaculos.add(dinoVoador[1])

    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        clock.tick(20)
        tela.fill(BRANCO)

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if not ai_jogando:
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE or event.key == K_UP:
                            if dinos[0].rect.y == ALTURA - 64 - 96 // 2:
                                dinos[0].pular()

                        if event.key == K_r and len(dinos) < 1:
                            reiniciarJogo(dinoVoador, cactos)
                            dinos.append(dn.Dino(ALTURA))
                            todasSprites.add(dinos[0])
        
        if ai_jogando:
            for i, dino in enumerate(dinos):
                if pygame.sprite.spritecollide(dino, spritesObstaculos, False, pygame.sprite.collide_mask):
                    dinos.pop(i)
                    todasSprites.remove(dino)
                    lista_genomas[i].fitness -= 2
                    lista_genomas.pop(i)
                    redes.pop(i)
        else:
            for i, dino in enumerate(dinos):
                if pygame.sprite.spritecollide(dino, spritesObstaculos, False, pygame.sprite.collide_mask):
                    todasSprites.remove(dino)
                    dinos.pop(i)

        chegou = False
        for cacto in cactos:
            for dinv in dinoVoador:
                if obstaculo == 2 or obstaculo == 3:
                    if cactos[1].rect.topright[0] <= 0 or dinoVoador[1].rect.topright[0] <= 0:
                        chegou = True
                        obstaculo = random.randint(0, 3)
                        cactos[0].rect.x = LARGURA
                        cactos[1].rect.x = LARGURA + cacto.rect.width

                        dinoVoador[0].rect.x = LARGURA
                        dinoVoador[1].rect.x = LARGURA + dinv.rect.width + 50
                    for cacto in cactos:
                        for dinv in dinoVoador:
                            cacto.obs = obstaculo
                            dinv.obs = obstaculo
                            chegou = False
                else:
                    if cactos[0].rect.topright[0] <= 0 or dinoVoador[0].rect.topright[0] <= 0:
                        chegou = True
                        obstaculo = random.randint(0, 3)
                        cactos[0].rect.x = LARGURA
                        cactos[1].rect.x = LARGURA + cacto.rect.width

                        dinoVoador[0].rect.x = LARGURA
                        dinoVoador[1].rect.x = LARGURA + dinv.rect.width + 50
                    for cacto in cactos:
                        for dinv in dinoVoador:
                            cacto.obs = obstaculo
                            dinv.obs = obstaculo
                            chegou = False

        if ai_jogando:
            for i, dino in enumerate(dinos):
                lista_genomas[i].fitness += 0.1
                output = redes[i].activate((dino.rect.y, dino.rect.x, abs(dino.rect.x - dinoVoador[0].rect.x), abs(dino.rect.x - dinoVoador[1].rect.x), abs(dino.rect.x - cactos[0].rect.x), abs(dino.rect.x - cactos[1].rect.x), abs(dino.rect.y - dinoVoador[0].rect.y), abs(dino.rect.y - dinoVoador[1].rect.y), abs(dino.rect.y - cactos[0].rect.y), abs(dino.rect.y - cactos[1].rect.y)))
                if output[0] > 0.5:
                    dino.pular()

        todasSprites.draw(tela)

        if len(dinos) < 1:
            if ai_jogando:
                rodando = False
                break
            if pontos % 100 == 0:
                pontos += 1
                                                    
            tela.blit(exibirMensagem(f'GAME OVER', 40, (0, 0, 0)), (200, 120))
            tela.blit(exibirMensagem(f'Pressione R para reiniciar', 20, (0, 0, 0)), (200, 180))

        else:
            pontos += 1
            todasSprites.update()
            txtPontos = exibirMensagem(f"pontos: {pontos}", 25, (0, 0, 0))

        if pontos % 100 == 0 and pontos <= 2500:
            if ai_jogando:
                for genoma in lista_genomas:
                    genoma.fitness += 10
            vel += 1
            nuvem.vel = vel
            for cacto in cactos:
                for dinv in dinoVoador:
                    dinv.vel = vel
                    cacto.vel = vel

        tela.blit(txtPontos, (430, 10))

        pygame.display.flip()

def rodar(caminho):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, caminho)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main)
    else:
        main(None, None)

if __name__ == "__main__":
    rodar('testes_pygame/jogoDinossauroAI/config.txt')