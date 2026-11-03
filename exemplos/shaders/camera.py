import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Câmera Fluida com Limites de Mapa (Clamping)")
clock = pygame.time.Clock()

# --- CONFIGURAÇÕES DO MAPA ---
# Definimos o tamanho total do nosso mundo do jogo
MAP_WIDTH, MAP_HEIGHT = 2000, 1500

# --- CONFIGURAÇÕES DO JOGADOR ---
# Começa no centro do mapa gigante
pos_jogador = pygame.math.Vector2(MAP_WIDTH / 2, MAP_HEIGHT / 2)
VELOCIDADE_JOGADOR = 500  

# --- CONFIGURAÇÕES DA CÂMERA ---
offset_camera = pygame.math.Vector2(pos_jogador.x - SCREEN_WIDTH / 2, pos_jogador.y - SCREEN_HEIGHT / 2)
TAXA_SUAVIZACAO_CAMERA = 5.0  

# --- ELEMENTOS DO CENÁRIO ---
# Blocos espalhados pelo mapa para dar noção de espaço
blocos_cenario = [
    pygame.Rect(100, 100, 80, 80),
    pygame.Rect(1800, 200, 100, 60), # Próximo à borda direita
    pygame.Rect(200, 1300, 120, 80), # Próximo à borda inferior
    pygame.Rect(900, 700, 150, 150),  # Centro do mapa
]

# Loop principal
running = True
while running:
    # 1. CÁLCULO DO DELTA TIME
    dt = clock.tick(60) / 1000.0

    # 2. EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. MOVIMENTAÇÃO E TRAVA DO JOGADOR
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pos_jogador.x -= VELOCIDADE_JOGADOR * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        pos_jogador.x += VELOCIDADE_JOGADOR * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        pos_jogador.y -= VELOCIDADE_JOGADOR * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        pos_jogador.y += VELOCIDADE_JOGADOR * dt

    # Garante que o JOGADOR não saia das bordas do mapa
    pos_jogador.x = max(0, min(pos_jogador.x, MAP_WIDTH))
    pos_jogador.y = max(0, min(pos_jogador.y, MAP_HEIGHT))

    # 4. CÁLCULO DA CÂMERA FLUIDA (Com os limites!)
    # Alvo ideal: centralizar o jogador
    alvo_camera = pygame.math.Vector2(
        pos_jogador.x - SCREEN_WIDTH / 2,
        pos_jogador.y - SCREEN_HEIGHT / 2
    )

    # Interpolação suave em direção ao alvo
    fator_tempo = 1.0 - math.exp(-TAXA_SUAVIZACAO_CAMERA * dt)
    offset_camera = offset_camera.lerp(alvo_camera, fator_tempo)

    # TRAVA DA CÂMERA (Clamping):
    # O limite mínimo é (0, 0) para não mostrar nada antes do início do mapa.
    # O limite máximo é o tamanho do mapa menos o tamanho da tela do jogador.
    limite_max_x = MAP_WIDTH - SCREEN_WIDTH
    limite_max_y = MAP_HEIGHT - SCREEN_HEIGHT

    offset_camera.x = max(0, min(offset_camera.x, limite_max_x))
    offset_camera.y = max(0, min(offset_camera.y, limite_max_y))

    # 5. RENDERIZAÇÃO
    screen.fill((30, 30, 30))  # Fundo cinza escuro

    # Desenhar uma borda visível para o mapa (para você ver o limite visual funcionando)
    borda_mapa = pygame.Rect(0 - int(offset_camera.x), 0 - int(offset_camera.y), MAP_WIDTH, MAP_HEIGHT)
    pygame.draw.rect(screen, (50, 50, 50), borda_mapa, 4) # Retângulo vazado mostrando a borda do mundo

    # Desenhar os blocos do cenário
    for bloco in blocos_cenario:
        pos_render = pygame.Rect(
            bloco.x - int(offset_camera.x),
            bloco.y - int(offset_camera.y),
            bloco.width,
            bloco.height
        )
        pygame.draw.rect(screen, (70, 70, 80), pos_render)

    # Desenhar o jogador
    pos_jogador_render = (
        int(pos_jogador.x - offset_camera.x),
        int(pos_jogador.y - offset_camera.y)
    )
    pygame.draw.circle(screen, (0, 255, 150), pos_jogador_render, 25)

    pygame.display.flip()

pygame.quit()
sys.exit()
