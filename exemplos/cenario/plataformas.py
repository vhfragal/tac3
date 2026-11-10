import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plataformas Flutuantes com Parallax")
clock = pygame.time.Clock()

# Cores
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)

# ==========================================
# CLASSE DA PLATAFORMA FLUTUANTE
# ==========================================
class Platform(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        
        # Posição fixa no "mundo real" do jogo
        self.world_x = world_x
        self.world_y = world_y
        
        self.rect.y = world_y

    def update(self, camera_x):
        # Atualiza a posição na tela com base na movimentação da câmera
        self.rect.x = self.world_x - camera_x

# ==========================================
# CONFIGURAÇÃO DOS GRUPOS E TEXTURAS
# ==========================================
# Criando as plataformas no mundo (Mundo X, Mundo Y, Largura, Altura)
platforms_group = pygame.sprite.Group()
platforms_group.add(Platform(200, 380, 150, 20))
platforms_group.add(Platform(450, 280, 200, 20))
platforms_group.add(Platform(750, 350, 150, 20))

# Texturas geradas dinamicamente para o Parallax do fundo
bg_far = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(bg_far, (100, 130, 160), [(0, 600), (200, 300), (400, 600)])
pygame.draw.polygon(bg_far, (90, 120, 150), [(300, 600), (550, 250), (800, 600)])

bg_mid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(bg_mid, (50, 100, 60), (50, 350, 100, 250))
pygame.draw.rect(bg_mid, (45, 95, 55), (350, 380, 120, 220))

# ==========================================
# VARIÁVEIS DO JOGADOR
# ==========================================
player_x = 375.0  # Fixo no centro horizontal da tela
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

MAX_JUMPS = 2
jumps_left = MAX_JUMPS

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
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if on_ground and jumps_left > 0:
                    velocity_y = jump_force
                    jumps_left -= 1
                    on_ground = False
                elif not on_ground and jumps_left > 0:
                    velocity_y = jump_force  
                    jumps_left -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if velocity_y < 0:
                    velocity_y *= 0.35

    # 2. INPUT DO TECLADO (Câmera)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        camera_x += player_speed * dt

    # 3. APLICAÇÃO DA FÍSICA VERTICAL (Antes das colisões)
    on_ground = False # Resetamos a flag para testar as colisões neste frame
    
    velocity_y += gravity * dt       
    player_y += velocity_y * dt      
    player_rect.y = player_y # Atualiza o rect para o teste de colisão

    # 4. DETECÇÃO DE COLISÕES
    
    # Caso A: Colisão com as Plataformas Flutuantes (Apenas quando estiver caindo)
    if velocity_y >= 0:
        for platform in platforms_group:
            # Verifica se o rect do jogador intercepta a plataforma
            if player_rect.colliderect(platform.rect):
                # Garante que o jogador estava acima da plataforma antes de colidir (colisão unidirecional)
                if player_rect.bottom - (velocity_y * dt) <= platform.rect.top + 5:
                    player_y = platform.rect.top - player_height
                    player_rect.y = player_y
                    velocity_y = 0.0
                    on_ground = True
                    jumps_left = MAX_JUMPS
                    break

    # Caso B: Colisão com o Chão Principal
    if player_y + player_height >= floor_y:
        player_y = floor_y - player_height  
        player_rect.y = player_y
        velocity_y = 0.0                     
        on_ground = True                     
        jumps_left = MAX_JUMPS  

    # Atualiza a posição de todas as plataformas baseado na câmera
    platforms_group.update(camera_x)

    # 5. RENDERIZAÇÃO
    screen.fill(SKY_BLUE)  

    # Parallax Fundo
    x_far = -(camera_x * SCROLL_SPEED_FAR) % WIDTH
    screen.blit(bg_far, (x_far, 0))
    screen.blit(bg_far, (x_far - WIDTH, 0))

    x_mid = -(camera_x * SCROLL_SPEED_MID) % WIDTH
    screen.blit(bg_mid, (x_mid, 0))
    screen.blit(bg_mid, (x_mid - WIDTH, 0))

    # Desenha as plataformas flutuantes atualizadas
    platforms_group.draw(screen)

    # Parallax Chão
    x_chao = -(camera_x * SCROLL_SPEED_CHAO) % WIDTH
    pygame.draw.rect(screen, GREEN, (x_chao, floor_y, WIDTH, HEIGHT - floor_y))
    pygame.draw.rect(screen, GREEN, (x_chao - WIDTH, floor_y, WIDTH, HEIGHT - floor_y))

    # Desenha o Jogador
    pygame.draw.rect(screen, BLUE, player_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
