import pygame
import random
import sys

# Inicializa os recursos do Pygame.
pygame.init()

# Define o tamanho da janela do jogo.
LARGURA = 1920
ALTURA = 1200
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Caça ao Cristal")

# Controla a velocidade de atualização da tela.
relogio = pygame.time.Clock()
FPS = 60

# Cores usadas nos elementos visuais do jogo.
PRETO = (18, 18, 26)
BRANCO = (245, 245, 245)
AZUL = (50, 140, 255)
AMARELO = (255, 215, 0)
VERMELHO = (230, 60, 60)
CINZA = (80, 80, 90)

# Fontes usadas para escrever textos na tela.
fonte_placar = pygame.font.SysFont("arial", 28, True)
fonte_media = pygame.font.SysFont("arial", 36, True)
fonte_pequena = pygame.font.SysFont("arial", 22)

# Cria o jogador como um retângulo azul.
jogador = pygame.Rect(380, 280, 40, 40)
velocidade_jogador = 5

# Define o tamanho do cristal coletável.
TAMANHO_CRISTAL = 26


def nova_posicao_cristal():
    # Gera uma posição aleatória para o cristal sem nascer sobre o jogador.
    while True:
        x = random.randint(20, LARGURA - TAMANHO_CRISTAL - 20)
        y = random.randint(70, ALTURA - TAMANHO_CRISTAL - 20)
        cristal = pygame.Rect(x, y, TAMANHO_CRISTAL, TAMANHO_CRISTAL)
        if not cristal.colliderect(jogador):
            return cristal


cristal = nova_posicao_cristal()

# Lista que guarda todos os inimigos criados durante a partida.
inimigos = []
velocidade_inimigos = 3


def criar_inimigo():
    # Cria um inimigo em uma borda aleatória da tela.
    tamanho = 32
    lado = random.choice(["cima", "baixo", "esquerda", "direita"])

    if lado == "cima":
        retangulo = pygame.Rect(
            random.randint(0, LARGURA - tamanho), 60, tamanho, tamanho
        )
        velocidade_x = random.choice([-velocidade_inimigos, velocidade_inimigos])
        velocidade_y = velocidade_inimigos
    elif lado == "baixo":
        retangulo = pygame.Rect(
            random.randint(0, LARGURA - tamanho), ALTURA - tamanho, tamanho, tamanho
        )
        velocidade_x = random.choice([-velocidade_inimigos, velocidade_inimigos])
        velocidade_y = -velocidade_inimigos
    elif lado == "esquerda":
        retangulo = pygame.Rect(0, random.randint(60, ALTURA - tamanho), tamanho, tamanho)
        velocidade_x = velocidade_inimigos
        velocidade_y = random.choice([-velocidade_inimigos, velocidade_inimigos])
    else:
        retangulo = pygame.Rect(
            LARGURA - tamanho, random.randint(60, ALTURA - tamanho), tamanho, tamanho
        )
        velocidade_x = -velocidade_inimigos
        velocidade_y = random.choice([-velocidade_inimigos, velocidade_inimigos])

    inimigos.append(
        {
            "retangulo": retangulo,
            "velocidade_x": velocidade_x,
            "velocidade_y": velocidade_y,
        }
    )


def atualizar_velocidade_inimigos():
    # Atualiza a velocidade dos inimigos sem mudar a direção atual deles.
    for inimigo in inimigos:
        inimigo["velocidade_x"] = (
            velocidade_inimigos
            if inimigo["velocidade_x"] > 0
            else -velocidade_inimigos
        )
        inimigo["velocidade_y"] = (
            velocidade_inimigos
            if inimigo["velocidade_y"] > 0
            else -velocidade_inimigos
        )


# Variáveis principais que controlam o estado do jogo.
placar = 0
rodando = True
fim_de_jogo = False


def desenhar_texto(texto, fonte, cor, x, y):
    # Transforma um texto em imagem e desenha na tela.
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def desenhar_cristal(retangulo):
    # Desenha o cristal como um losango amarelo com borda branca.
    centro_x = retangulo.centerx
    centro_y = retangulo.centery
    pontos = [
        (centro_x, retangulo.top),
        (retangulo.right, centro_y),
        (centro_x, retangulo.bottom),
        (retangulo.left, centro_y),
    ]

    pygame.draw.polygon(tela, AMARELO, pontos)
    pygame.draw.polygon(tela, BRANCO, pontos, 2)


def reiniciar_jogo():
    # Reinicia a partida voltando as variáveis principais ao valor inicial.
    global jogador, cristal, inimigos, velocidade_jogador, velocidade_inimigos
    global placar, fim_de_jogo

    jogador = pygame.Rect(380, 280, 40, 40)
    velocidade_jogador = 5
    velocidade_inimigos = 3
    inimigos = []
    placar = 0
    cristal = nova_posicao_cristal()
    fim_de_jogo = False


# Loop principal: mantém o jogo aberto enquanto rodando for verdadeiro.
while rodando:
    relogio.tick(FPS)

    # Captura eventos da janela e do teclado.
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

            if fim_de_jogo and evento.key == pygame.K_RETURN:
                reiniciar_jogo()

    if not fim_de_jogo:
        # Verifica continuamente quais teclas estão pressionadas.
        teclas = pygame.key.get_pressed()

        # Move o jogador e impede que ele saia dos limites da tela.
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.left = max(0, jogador.left - velocidade_jogador)

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.right = min(LARGURA, jogador.right + velocidade_jogador)

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jogador.top = max(60, jogador.top - velocidade_jogador)

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jogador.bottom = min(ALTURA, jogador.bottom + velocidade_jogador)

        # Coleta o cristal, aumenta o placar e ajusta a dificuldade.
        if jogador.colliderect(cristal):
            placar += 1
            cristal = nova_posicao_cristal()
            velocidade_inimigos = 3 + placar * 0.15

            if placar % 2 == 0:
                velocidade_jogador += 0.2

            if placar == 1 or placar % 3 == 0:
                criar_inimigo()

            atualizar_velocidade_inimigos()

        # Move os inimigos, faz eles rebaterem nas paredes e verifica colisão.
        for inimigo in inimigos:
            retangulo = inimigo["retangulo"]
            retangulo.x += inimigo["velocidade_x"]
            retangulo.y += inimigo["velocidade_y"]

            if retangulo.left <= 0:
                retangulo.left = 0
                inimigo["velocidade_x"] = abs(inimigo["velocidade_x"])
            elif retangulo.right >= LARGURA:
                retangulo.right = LARGURA
                inimigo["velocidade_x"] = -abs(inimigo["velocidade_x"])

            if retangulo.top <= 60:
                retangulo.top = 60
                inimigo["velocidade_y"] = abs(inimigo["velocidade_y"])
            elif retangulo.bottom >= ALTURA:
                retangulo.bottom = ALTURA
                inimigo["velocidade_y"] = -abs(inimigo["velocidade_y"])

            if jogador.colliderect(retangulo):
                fim_de_jogo = True

    # Limpa a tela antes de desenhar o próximo quadro.
    tela.fill(PRETO)

    # Desenha a barra superior com o placar e a mensagem do jogo.
    pygame.draw.rect(tela, CINZA, (0, 0, LARGURA, 60))
    desenhar_texto(f"Placar: {placar}", fonte_placar, BRANCO, 15, 15)
    desenhar_texto(
        "Colete os cristais e evite os inimigos", fonte_pequena, BRANCO, 230, 20
    )

    if not fim_de_jogo:
        # Desenha os elementos da partida enquanto o jogo está ativo.
        desenhar_cristal(cristal)

        pygame.draw.rect(tela, AZUL, jogador)
        pygame.draw.rect(tela, BRANCO, jogador, 2)

        for inimigo in inimigos:
            pygame.draw.ellipse(tela, VERMELHO, inimigo["retangulo"])
            pygame.draw.ellipse(tela, BRANCO, inimigo["retangulo"], 2)
    else:
        # Mostra a tela final quando o jogador encosta em um inimigo.
        desenhar_texto("FIM DE JOGO", fonte_media, VERMELHO, 300, 230)
        desenhar_texto(f"Cristais coletados: {placar}", fonte_placar, BRANCO, 300, 285)
        desenhar_texto(
            "Pressione ENTER para reiniciar ou ESC para sair",
            fonte_pequena,
            BRANCO,
            210,
            335,
        )

    # Atualiza a janela com tudo que foi desenhado.
    pygame.display.flip()

pygame.quit()
sys.exit()
