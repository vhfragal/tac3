import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulo Duplo e Variável com Parallax")
clock = pygame.time.Clock()

# Cores
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)

# ==========================================
# GERADOR DE TEXTURAS DE EXEMPLO (Parallax)
# ==========================================
bg_far = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(bg_far, (100, 130, 160), [(0, 600), (200, 300), (400, 600)])
pygame.draw.polygon(bg_far, (90, 120, 150), [(300, 600), (550, 250), (800, 600)])

bg_mid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(bg_mid, (50, 100, 60), (50, 350, 100, 250))
pygame.draw.rect(bg_mid, (45, 95, 55), (350, 380, 120, 220))

# ==========================================
# VARIÁVEIS DO JOGADOR
# ==========================================
player_x = 375.0  
player_y = 400.0
player_width = 50
player_height = 50
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

player_speed = 400.0  
velocity_y = 0.0        
gravity = 1400.0        
jump_force = -600.0     
on_ground = False       
floor_y = 500

# NOVAS VARIÁVEIS PARA O PULO DUPLO
MAX_JUMPS = 2
jumps_left = MAX_JUMPS

# ==========================================
# VARIÁVEIS DO PARALLAX
# ==========================================
camera_x = 0.0  
SCROLL_SPEED_FAR = 0.15  
SCROLL_SPEED_MID = 0.45  
SCROLL_SPEED_CHAO = 1.0  

# Loop principal do jogo
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # 1. TRATAMENTO DE EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # LÓGICA DE DETECÇÃO DO PULO DUPLO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Caso 1: Primeiro pulo (precisa estar no chão)
                if on_ground and jumps_left > 0:
                    velocity_y = jump_force
                    jumps_left -= 1
                    on_ground = False
                # Caso 2: Pulo no ar (pulo duplo)
                elif not on_ground and jumps_left > 0:
                    velocity_y = jump_force  # Reseta o impulso vertical para cima
                    jumps_left -= 1

        # Pulo Variável (Mantém o corte de velocidade se soltar o botão)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if velocity_y < 0:
                    velocity_y *= 0.35

    # 2. INPUT DO TECLADO (Movimentação Lateral)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        camera_x += player_speed * dt

    # 3. APLICAÇÃO DA FÍSICA VERTICAL
    velocity_y += gravity * dt       
    player_y += velocity_y * dt      

    # COLISÃO COM O CHÃO E RESET DE PULOS
    if player_y + player_height >= floor_y:
        player_y = floor_y - player_height  
        velocity_y = 0.0                     
        on_ground = True                     
        jumps_left = MAX_JUMPS  # <--- RESETAMOS OS PULOS AO TOCAR O CHÃO

    player_rect.y = player_y

    # 4. RENDERIZAÇÃO DO PARALLAX
    screen.fill(SKY_BLUE)  

    x_far = -(camera_x * SCROLL_SPEED_FAR) % WIDTH
    screen.blit(bg_far, (x_far, 0))
    screen.blit(bg_far, (x_far - WIDTH, 0))

    x_mid = -(camera_x * SCROLL_SPEED_MID) % WIDTH
    screen.blit(bg_mid, (x_mid, 0))
    screen.blit(bg_mid, (x_mid - WIDTH, 0))

    x_chao = -(camera_x * SCROLL_SPEED_CHAO) % WIDTH
    pygame.draw.rect(screen, GREEN, (x_chao, floor_y, WIDTH, HEIGHT - floor_y))
    pygame.draw.rect(screen, GREEN, (x_chao - WIDTH, floor_y, WIDTH, HEIGHT - floor_y))

    # Desenha o Jogador
    pygame.draw.rect(screen, BLUE, player_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
