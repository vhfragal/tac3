import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulo Variável com Delta Time")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# VARIÁVEIS DO JOGADOR (Floats para precisão com DT)
player_x = 100.0
player_y = 400.0
player_width = 50
player_height = 50
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

player_speed = 300.0  # Pixels por segundo

# Física do Pulo
velocity_y = 0.0        
gravity = 1400.0        # Aumentada levemente para um pulo mais firme
jump_force = -600.0     # Força máxima do pulo (se segurar o botão)
on_ground = False       

# Variável do Chão
floor_y = 500

# Loop principal do jogo
running = True
while running:
    # Calcula Delta Time em segundos (ex: 0.016 a 60 FPS)
    dt = clock.tick(60) / 1000.0

    # 1. TRATAMENTO DE EVENTOS (Essencial para detectar o momento exato do clique/soltura)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # DETECTA O INÍCIO DO PULO (Pressionou o botão)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and on_ground:
                velocity_y = jump_force
                on_ground = False
                
        # DETECTA O CORTE DO PULO (Soltou o botão no ar)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Se o jogador ainda estiver subindo (velocity_y negativo significa subindo)
                if velocity_y < 0:
                    # Multiplicamos por 0.35 para cortar cerca de 65% do impulso restante
                    velocity_y *= 0.35

    # 2. INPUT DO TECLADO (Para movimento contínuo horizontal)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        player_x += player_speed * dt

    # 3. APLICAÇÃO DA FÍSICA (Gravidade e Posição)
    velocity_y += gravity * dt       
    player_y += velocity_y * dt      

    # 4. DETECÇÃO DE COLISÃO COM O CHÃO
    if player_y + player_height >= floor_y:
        player_y = floor_y - player_height  
        velocity_y = 0.0                     
        on_ground = True                     

    # Atualiza o rect para renderização
    player_rect.x = player_x
    player_rect.y = player_y

    # 5. RENDERIZAÇÃO
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, floor_y, WIDTH, HEIGHT - floor_y)) # Chão
    pygame.draw.rect(screen, BLUE, player_rect)                            # Jogador
    
    pygame.display.flip()

pygame.quit()
sys.exit()
