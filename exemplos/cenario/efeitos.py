import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plataformas com Efeitos Visuais de Partículas")
clock = pygame.time.Clock()

# Cores
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)

# ==========================================
# SISTEMA DE PARTÍCULAS (EFEITOS VISUAIS)
# ==========================================
class Particle:
    def __init__(self, world_x, world_y, color, size=None):
        self.world_x = world_x
        self.world_y = world_y
        self.color = list(color) # Convertido para lista para podermos alterar o Alpha se necessário
        self.size = size if size else random.randint(4, 8)
        
        # Direção e velocidade aleatória para a partícula se espalhar
        self.vel_x = random.uniform(-150, 150)
        self.vel_y = random.uniform(-100, -250) if color == (200, 200, 200) else random.uniform(-150, 150)
        
        # Tempo de vida da partícula em segundos
        self.lifetime = random.uniform(0.3, 0.6)

    def update(self, dt):
        # Move a partícula no mundo real usando DT
        self.world_x += self.vel_x * dt
        self.world_y += self.vel_y * dt
        # Reduz o tempo de vida
        self.lifetime -= dt
        # Diminui o tamanho gradativamente
        if self.size > 0.1:
            self.size -= 5 * dt

    def draw(self, surface, camera_x):
        # Converte a posição do mundo para a tela usando a câmera
        screen_x = int(self.world_x - camera_x)
        screen_y = int(self.world_y)
        
        if self.lifetime > 0 and self.size > 0:
            # Desenha a partícula na tela
            pygame.draw.circle(surface, self.color, (screen_x, screen_y), int(self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_dust(self, world_x, world_y):
        # Cria poeira cinza (pulo normal do chão)
        for _ in range(12):
            self.particles.append(Particle(world_x + random.randint(0, 50), world_y, (200, 200, 200)))

    def spawn_double_jump_energy(self, world_x, world_y):
        # Cria energia azul brilhante (pulo duplo no ar)
        for _ in range(20):
            p = Particle(world_x + 25, world_y + 25, (0, 230, 255), random.randint(5, 10))
            p.vel_y = random.uniform(-200, 200) # Espalha para todas as direções verticais
            self.particles.append(p)

    def update_and_draw(self, surface, camera_x, dt):
        # Atualiza e desenha todas as partículas ativas, removendo as mortas
        self.particles = [p for p in self.particles if p.lifetime > 0 and p.size > 0]
        for p in self.particles:
            p.update(dt)
            p.draw(surface, camera_x)

# Instancia o sistema de efeitos visuais
particle_system = ParticleSystem()

# ==========================================
# CLASSE DA PLATAFORMA FLUTUANTE
# ==========================================
class Platform(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.world_x = world_x
        self.world_y = world_y
        self.rect.y = world_y

    def update(self, camera_x):
        self.rect.x = self.world_x - camera_x

# Grupos de Plataformas
platforms_group = pygame.sprite.Group()
platforms_group.add(Platform(200, 380, 150, 20))
platforms_group.add(Platform(450, 280, 200, 20))

# Parallax Backgrounds
bg_far = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(bg_far, (100, 130, 160), [(0, 600), (200, 300), (400, 600)])
pygame.draw.polygon(bg_far, (90, 120, 150), [(300, 600), (550, 250), (800, 600)])

bg_mid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(bg_mid, (50, 100, 60), (50, 350, 100, 250))
pygame.draw.rect(bg_mid, (45, 95, 55), (350, 380, 120, 220))

# ==========================================
# VARIÁVEIS DO JOGADOR
# ==========================================
player_world_x = 375.0 # Posição real do jogador no mundo
player_y = 400.0
player_width = 50
player_height = 50
player_rect = pygame.Rect(375, player_y, player_width, player_height) # Rect fixo na tela para renderização

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
                # Caso 1: Primeiro pulo (Gera Poeira)
                if on_ground and jumps_left > 0:
                    velocity_y = jump_force
                    jumps_left -= 1
                    on_ground = False
                    particle_system.spawn_dust(player_world_x, player_y + player_height)
                
                # Caso 2: Pulo duplo (Gera Explosão de Energia)
                elif not on_ground and jumps_left > 0:
                    velocity_y = jump_force  
                    jumps_left -= 1
                    particle_system.spawn_double_jump_energy(player_world_x, player_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if velocity_y < 0:
                    velocity_y *= 0.35

    # 2. INPUT DO TECLADO (Atualiza posição X do mundo e Câmera)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= player_speed * dt
        player_world_x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        camera_x += player_speed * dt
        player_world_x += player_speed * dt

    # 3. FÍSICA VERTICAL
    on_ground = False 
    velocity_y += gravity * dt       
    player_y += velocity_y * dt      
    player_rect.y = player_y 

    # 4. COLISÕES
    if velocity_y >= 0:
        for platform in platforms_group:
            if player_rect.colliderect(platform.rect):
                if player_rect.bottom - (velocity_y * dt) <= platform.rect.top + 5:
                    player_y = platform.rect.top - player_height
                    player_rect.y = player_y
                    velocity_y = 0.0
                    on_ground = True
                    jumps_left = MAX_JUMPS
                    break

    if player_y + player_height >= floor_y:
        player_y = floor_y - player_height  
        player_rect.y = player_y
        velocity_y = 0.0                     
        on_ground = True                     
        jumps_left = MAX_JUMPS  

    # Atualiza plataformas
    platforms_group.update(camera_x)

    # 5. RENDERIZAÇÃO (Em ordem de camadas)
    screen.fill(SKY_BLUE)  

    # Parallax Distante
    x_far = -(camera_x * SCROLL_SPEED_FAR) % WIDTH
    screen.blit(bg_far, (x_far, 0))
    screen.blit(bg_far, (x_far - WIDTH, 0))

    # Parallax Médio
    x_mid = -(camera_x * SCROLL_SPEED_MID) % WIDTH
    screen.blit(bg_mid, (x_mid, 0))
    screen.blit(bg_mid, (x_mid - WIDTH, 0))

    # Desenha as plataformas flutuantes
    platforms_group.draw(screen)

    # Parallax Chão
    x_chao = -(camera_x * SCROLL_SPEED_CHAO) % WIDTH
    pygame.draw.rect(screen, GREEN, (x_chao, floor_y, WIDTH, HEIGHT - floor_y))
    pygame.draw.rect(screen, GREEN, (x_chao - WIDTH, floor_y, WIDTH, HEIGHT - floor_y))

    # ATUALIZA E DESENHA AS PARTÍCULAS (Fica atrás do jogador, mas na frente do cenário)
    particle_system.update_and_draw(screen, camera_x, dt)

    # Desenha o Jogador por cima de quase tudo
    pygame.draw.rect(screen, BLUE, player_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
