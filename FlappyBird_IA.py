import pygame
import os
import random
import neat

ai_jogando = True
geracao = 0

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CANO2 = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'Cano flrst(1).png')))
IMAGEM_CANO3 = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'Cano spc(1).png')))

IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_CHAO2 = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'Chão flrst.png')))
IMAGEM_CHAO3 = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'Chão spc(1).png')))

IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEM_BACKGROUND2 = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'Floresta(1).png')))
IMAGEM_BACKGROUND3 = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'Espaço(1).png')))

IMAGENS_PASSARO =[
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo



        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passáro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA

            else:
                if self.angulo > -90:
                    self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passáro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passáro estiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem =  self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x, y):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_TOPO2 = pygame.transform.flip(IMAGEM_CANO2, False, True)
        self.CANO_TOPO3 = pygame.transform.flip(IMAGEM_CANO3, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.CANO_BASE2 = IMAGEM_CANO2
        self.CANO_BASE3 = IMAGEM_CANO3
        self.passou = False
        self.definir_altura()
        self.tempo = 0
        self.y = y


    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_topo2 = self.altura - self.CANO_TOPO2.get_height()
        self.pos_topo3 = self.altura - self.CANO_TOPO3.get_height()
        self.pos_base = self.altura + self.DISTANCIA


    def mover(self):
        self.x -= self.VELOCIDADE

    def mover2(self):
        self.VELOCIDADE = 10
        self.x -= self.VELOCIDADE

    def mover3(self):
        self.VELOCIDADE = 15
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))


    def desenhar2(self, tela):
        tela.blit(self.CANO_TOPO2, (self.x, self.pos_topo2))
        tela.blit(self.CANO_TOPO2, (self.x + 100, self.pos_topo2))

        tela.blit(self.CANO_BASE2, (self.x, self.pos_base))
        tela.blit(self.CANO_BASE2, (self.x + 100, self.pos_base))

    def desenhar3(self, tela):
        tela.blit(self.CANO_TOPO3, (self.x, self.pos_topo3))
        tela.blit(self.CANO_TOPO3, (self.x + 100, self.pos_topo3 - self.x))

        tela.blit(self.CANO_BASE3, (self.x, self.pos_base))
        tela.blit(self.CANO_BASE3, (self.x + 100, self.pos_base + self.x))


    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_maks = pygame.mask.from_surface(self.CANO_BASE)



        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))


        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_maks, distancia_base)



        if base_ponto or topo_ponto:
            return True
        else:
            return False

    def colidir2(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask2 = pygame.mask.from_surface(self.CANO_TOPO2)
        base_maks2 = pygame.mask.from_surface(self.CANO_BASE2)
        distancia_topo2 = (self.x - passaro.x, self.pos_topo2 - round(passaro.y))
        distancia_topo2_duplo = (self.x - passaro.x, self.pos_topo2 - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        distancia_base_duplo = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto2 = passaro_mask.overlap(topo_mask2, distancia_topo2)
        base_ponto2 = passaro_mask.overlap(base_maks2, distancia_base)
        topo_ponto2_duplo = passaro_mask.overlap(topo_mask2, distancia_topo2_duplo)
        base_ponto2_duplo = passaro_mask.overlap(base_maks2, distancia_base_duplo)

        if base_ponto2 or topo_ponto2 or base_ponto2_duplo or topo_ponto2_duplo:
            return True
        else:
            return False


    def colidir3(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask3 = pygame.mask.from_surface(self.CANO_TOPO3)
        base_maks3 = pygame.mask.from_surface(self.CANO_BASE3)

        distancia_topo3 = (self.x - passaro.x, self.pos_topo3 - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        distancia_topo_duplo = ((self.x + 100) - passaro.x, (self.pos_topo3 - self.x) - round(passaro.y))
        distancia_base_duplo = ((self.x + 100) - passaro.x, (self.pos_base + self.x) - round(passaro.y))
        topo_ponto3 = passaro_mask.overlap(topo_mask3, distancia_topo_duplo)
        base_ponto3 = passaro_mask.overlap(base_maks3, distancia_base_duplo)
        topo_ponto_duplo = passaro_mask.overlap(topo_mask3, distancia_topo3)
        base_ponto_duplo = passaro_mask.overlap(base_maks3, distancia_base)

        if base_ponto3 or topo_ponto3 or base_ponto_duplo or topo_ponto_duplo:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO
    LARGURA2 = IMAGEM_CHAO2.get_width()
    IMAGEM2 = IMAGEM_CHAO2
    LARGURA3 = IMAGEM_CHAO3.get_width()
    IMAGEM3 = IMAGEM_CHAO3

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        self.x3 = 0
        self.x4 = self.LARGURA2
        self.x5 = 0
        self.x6 = self.LARGURA3


    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x2 + self.LARGURA

        if self.x3 + self.LARGURA2 < 0:
            self.x3 = self.LARGURA2

        if self.x4 + self.LARGURA2 < 0:
            self.x4 = self.x4 + self.LARGURA2

        if self.x5 + self.LARGURA3 < 0:
            self.x5 = self.LARGURA3

        if self.x6 + self.LARGURA3 < 0:
            self.x6 = self.x6 + self.LARGURA3

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

    def desenhar_2(self, tela):
        tela.blit(self.IMAGEM2, (self.x3, self.y))
        tela.blit(self.IMAGEM2, (self.x4, self.y))

    def desenhar_3(self, tela):
        tela.blit(self.IMAGEM3, (self.x5, self.y))
        tela.blit(self.IMAGEM3, (self.x6, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    if pontos <= 20:
        tela.blit(IMAGEM_BACKGROUND, (0, 0))

    elif pontos > 20 and pontos <= 60:
        tela.blit(IMAGEM_BACKGROUND2, (0, 0))

    elif pontos > 60:
        tela.blit(IMAGEM_BACKGROUND3, (0, 0))


    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        if pontos <= 20:
            cano.desenhar(tela)
        elif pontos > 20 and pontos <= 60:
            cano.desenhar2(tela)
        elif pontos > 60:
            cano.desenhar3(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    if pontos <= 20:
        chao.desenhar(tela)

    elif pontos > 20 and pontos <= 60:
        chao.desenhar_2(tela)

    elif pontos > 60:
        chao.desenhar_3(tela)

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
    canos = [Cano(700, 200)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

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
            if pontos < 6:
                if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                    indice_cano = 1
                elif pontos > 5 and pontos < 11:
                    if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO2.get_width()):
                        indice_cano = 1
                elif pontos > 10:
                    if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO3.get_width()):
                        indice_cano = 1

        else:
            rodando = False
            break

        # mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            # aumentar um pouquinho a fitness do passaro
            if ai_jogando:
                lista_genomas[i].fitness += 0.1
                output = redes[i].activate((passaro.y, abs(passaro.y - canos[indice_cano].altura),abs(passaro.y - canos[indice_cano].pos_base)))
                # -1 e 1 -> se o output for > 0.5, então o passáro pula
                if output[0] > 0.5:
                    passaro.pular()

        chao.mover()


        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if pontos <= 20:
                    if cano.colidir(passaro):
                        passaros.pop(i)
                        if ai_jogando:
                            lista_genomas[i].fitness -= 1
                            lista_genomas.pop(i)
                            redes.pop(i)
                elif pontos > 20 and pontos <= 60:
                    if cano.colidir2(passaro):
                        passaros.pop(i)
                        if ai_jogando:
                            lista_genomas[i].fitness -= 1
                            lista_genomas.pop(i)
                            redes.pop(i)
                elif pontos > 60:
                    if cano.colidir3(passaro):
                        passaros.pop(i)
                        if ai_jogando:
                            lista_genomas[i].fitness -= 1
                            lista_genomas.pop(i)
                            redes.pop(i)
                if not cano.passou and passaro.x > (cano.x + 100):
                    cano.passou = True
                    adicionar_cano = True
            if pontos <= 20:
                cano.mover()
            elif pontos > 20 and pontos <= 60:
                cano.mover2()
            elif pontos > 60:
                cano.mover3()

            if pontos < 21:
                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)
            if pontos > 20 and pontos < 61:
                if cano.x + cano.CANO_TOPO2.get_width() < 0:
                    remover_canos.append(cano)
            if pontos > 60:
                if cano.x + cano.CANO_TOPO3.get_width() < 0:
                    remover_canos.append(cano)


        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600, 200))
            if ai_jogando:
                for genoma in lista_genomas:
                    genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)




def rodar(caminho_config):

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, caminho_config)
        chekpoint = neat.Checkpointer(generation_interval=0, time_interval_seconds=None)
        populacao = neat.Population(config)
        populacao.add_reporter(neat.StdOutReporter(True))
        populacao.add_reporter(neat.StatisticsReporter())
        populacao.add_reporter(chekpoint)



        if ai_jogando:
            if os.path.exists('neat-checkpoint-4'):
                populacao = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
            populacao.run(main, 200)

        else:
            main(None, None)





if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, '03-18 - config.txt')
    rodar(caminho_config)





