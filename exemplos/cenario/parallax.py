import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulo Variável com Efeito Parallax")
clock = pygame.time.Clock()

# Cores
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)

# ==========================================
# GERAÇÃO DE TEXTURAS DE EXEMPLO (Substitutos para suas imagens .png)
# ==========================================
# Camada Longínqua (Montanhas distantes - move bem devagar)
bg_far = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(bg_far, (100, 130, 160), [(0, 600), (200, 300), (400, 600)])
pygame.draw.polygon(bg_far, (90, 120, 150), [(300, 600), (550, 250), (800, 600)])

# Camada Média (Árvores/Estruturas médias - velocidade moderada)
bg_mid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(bg_mid, (50, 100, 60), (50, 350, 100, 250))
pygame.draw.rect(bg_mid, (45, 95, 55), (350, 380, 120, 220))
pygame.draw.rect(bg_mid, (50, 100, 60), (650, 330, 90, 270))

# ==========================================
# VARIÁVEIS DO JOGADOR (Física + Pulo Variável)
# ==========================================
player_x = 375.0  # Mantemos o jogador fixo no centro da tela horizontalmente para o Parallax
player_y = 400.0
player_width = 50
player_height = 50
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

player_speed = 400.0  # Velocidade com que o "mundo" vai se mover
velocity_y = 0.0        
gravity = 1400.0        
jump_force = -600.0     
on_ground = False       
floor_y = 500

# ==========================================
# VARIÁVEIS DO PARALLAX (Posições x dos fundos)
# ==========================================
# Esta variável simula a câmera andando pelo mundo
camera_x = 0.0  

# Fatores de velocidade para cada camada (0 = parado, 1 = velocidade real do jogo)
SCROLL_SPEED_FAR = 0.15  # Montanhas se movem a 15% da velocidade
SCROLL_SPEED_MID = 0.45  # Árvores se movem a 45% da velocidade
SCROLL_SPEED_CHAO = 1.0  # O chão se move a 100% da velocidade

# Loop principal do jogo
running = True
while running:
    # Calcula Delta Time em segundos
    dt = clock.tick(60) / 1000.0

    # 1. TRATAMENTO DE EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Pulo Variável (Início)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and on_ground:
                velocity_y = jump_force
                on_ground = False
                
        # Pulo Variável (Corte do impulso se soltar a tecla)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if velocity_y < 0:
                    velocity_y *= 0.35

    # 2. INPUT DO TECLADO (Move a Câmera pelo mundo, em vez do Jogador)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        camera_x += player_speed * dt

    # 3. APLICAÇÃO DA FÍSICA VERTICAL (O jogador ainda cai e pula verticalmente)
    velocity_y += gravity * dt       
    player_y += velocity_y * dt      

    # Colisão com o Chão
    if player_y + player_height >= floor_y:
        player_y = floor_y - player_height  
        velocity_y = 0.0                     
        on_ground = True                     

    # Atualiza a posição Y do Rect do jogador
    player_rect.y = player_y

    # ==========================================
    # 4. RENDERIZAÇÃO DO PARALLAX (Do fundo para a frente)
    # ==========================================
    screen.fill(SKY_BLUE)  # 1º: Céu estático no fundo

    # 2º: Desenha a Camada Distante (Montanhas) duplicada para efeito infinito
    # O operador '%' faz com que o valor de x fique sempre dentro da largura da tela [0, WIDTH]
    x_far = -(camera_x * SCROLL_SPEED_FAR) % WIDTH
    screen.blit(bg_far, (x_far, 0))
    screen.blit(bg_far, (x_far - WIDTH, 0))

    # 3º: Desenha a Camada Média (Árvores) duplicada
    x_mid = -(camera_x * SCROLL_SPEED_MID) % WIDTH
    screen.blit(bg_mid, (x_mid, 0))
    screen.blit(bg_mid, (x_mid - WIDTH, 0))

    # 4º: Desenha o Chão (Se move na velocidade máxima de 100%)
    x_chao = -(camera_x * SCROLL_SPEED_CHAO) % WIDTH
    # Desenha dois blocos de chão lado a lado para preencher a tela na repetição
    pygame.draw.rect(screen, GREEN, (x_chao, floor_y, WIDTH, HEIGHT - floor_y))
    pygame.draw.rect(screen, GREEN, (x_chao - WIDTH, floor_y, WIDTH, HEIGHT - floor_y))

    # 5º: Desenha o Jogador por cima de tudo
    pygame.draw.rect(screen, BLUE, player_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
