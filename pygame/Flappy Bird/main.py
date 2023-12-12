import pygame, random, neat

#pip install neat-python

ai_jogando = True
geracao = 0

ALTURA_TELA = 800
LARGURA_TELA = 500

IMG_CANO = pygame.transform.scale2x(pygame.image.load('testes_pygame/Flappy Bird/img/pipe.png'))
IMG_CHAO = pygame.transform.scale2x(pygame.image.load('testes_pygame/Flappy Bird/img/base.png'))
IMG_BG = pygame.transform.scale2x(pygame.image.load('testes_pygame/Flappy Bird/img/bg.png'))
IMG_BIRD = [
    pygame.transform.scale2x(pygame.image.load('testes_pygame/Flappy Bird/img/bird1.png')),
    pygame.transform.scale2x(pygame.image.load('testes_pygame/Flappy Bird/img/bird2.png')),
    pygame.transform.scale2x(pygame.image.load('testes_pygame/Flappy Bird/img/bird3.png'))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = IMG_BIRD
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 15
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_da_imagem = 0
        self.img = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura -50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_da_imagem += 1

        if self.contagem_da_imagem < self.TEMPO_ANIMACAO:
            self.img = self.IMGS[0]
        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO*2:
            self.img = self.IMGS[1]
        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO*3:
            self.img = self.IMGS[2]
        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO*4:
            self.img = self.IMGS[1]
        elif self.contagem_da_imagem >= self.TEMPO_ANIMACAO*4+1:
            self.img = self.IMGS[0]
            self.contagem_da_imagem = 0

        if self.angulo <= -80:
            self.img = self.IMGS[1]
            self.contagem_da_imagem = self.TEMPO_ANIMACAO*2

        imagem_rot = pygame.transform.rotate(self.img, self.angulo)
        centro_img = self.img.get_rect(topleft=(self.x, self.y)).center
        ret = imagem_rot.get_rect(center=centro_img)
        tela.blit(imagem_rot, ret.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMG_CANO, False, True)
        self.CANO_BASE = IMG_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE 

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, round(self.pos_topo) - round(passaro.y))
        distancia_base = (self.x - passaro.x, round(self.pos_base) - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:   
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMG_CHAO.get_width()
    IMAGEM = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMG_BG, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", True, (255, 255, 255))
    tela.blit(texto, (LARGURA_TELA-10-texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()

def main(genomas, config):
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))
    else:
        passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pontos = 0
    clock = pygame.time.Clock()

    rodando = True
    while rodando:
        clock.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()
                            
        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break

        for i, passaro in enumerate(passaros):
            passaro.mover()
            lista_genomas[i].fitness += 0.1
            output = redes[i].activate((passaro.y, abs(passaro.y - canos[indice_cano].altura), abs(passaro.y - canos[indice_cano].pos_base)))
            if output[0] > 0.5:
                passaro.pular()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):        
                    passaros.pop(i)
                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            for genoma in lista_genomas:
                genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if passaro.y + passaro.img.get_height() > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    lista_genomas[i].fitness -= 2
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

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
    rodar('testes_pygame/Flappy Bird/config.txt')