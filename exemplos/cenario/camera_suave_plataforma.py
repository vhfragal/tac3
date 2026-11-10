import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# --- CONFIGURAÇÕES DO JOGO ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 3000   # Tamanho grande do mapa
MAP_HEIGHT = 1200
GRAVITY = 0.5

# --- INICIALIZAÇÃO DO PYGAME E OPENGL ---
pygame.init()
display = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Configurando a projeção 2D no OpenGL (Ortogonal)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0) # Inverte o eixo Y para o Pygame padrão (0,0 no topo esquerdo)
glMatrixMode(GL_MODELVIEW)

# --- CLASSES ---
class Player:
    def __init__(self, x, y):
        self.w = 40
        self.h = 60
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 7
        self.jump_power = -12
        self.on_ground = False

    def update(self, platforms):
        # Aplicar gravidade
        self.vy += GRAVITY
        
        # Movimento Horizontal
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[K_LEFT]:  self.vx = -self.speed
        if keys[K_RIGHT]: self.vx = self.speed
        
        # Mover X e checar colisão
        self.x += self.vx
        self.move_and_collide(platforms, 'x')
        
        # Pular
        if keys[K_SPACE] and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

        # Mover Y e checar colisão
        self.y += self.vy
        self.move_and_collide(platforms, 'y')

        # Limites do mapa para o jogador
        if self.x < 0: self.x = 0
        if self.x > MAP_WIDTH - self.w: self.x = MAP_WIDTH - self.w
        if self.y > MAP_HEIGHT - self.h:
            self.y = MAP_HEIGHT - self.h
            self.vy = 0
            self.on_ground = True

    def move_and_collide(self, platforms, direction):
        for p in platforms:
            # Checa interseção AABB
            if (self.x < p[0] + p[2] and self.x + self.w > p[0] and
                self.y < p[1] + p[3] and self.y + self.h > p[1]):
                if direction == 'x':
                    if self.vx > 0: self.x = p[0] - self.w
                    if self.vx < 0: self.x = p[0] + p[2]
                if direction == 'y':
                    if self.vy > 0:
                        self.y = p[1] - self.h
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:
                        self.y = p[1] + p[3]
                        self.vy = 0

    def draw(self):
        # Desenha o jogador em Vermelho
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.w, self.y)
        glVertex2f(self.x + self.w, self.y + self.h)
        glVertex2f(self.x, self.y + self.h)
        glEnd()

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.lerp_factor = 0.1 # Velocidade da fluidez (quanto menor, mais suave/atrasada)

    def target(self, player):
        # Centraliza a câmera no jogador
        target_x = player.x + player.w / 2 - self.width / 2
        target_y = player.y + player.h / 2 - self.height / 2

        # LERP (Interpolação Linear)
        self.x += (target_x - self.x) * self.lerp_factor
        self.y += (target_y - self.y) * self.lerp_factor

        # Limites da câmera no mapa (Clamp)
        if self.x < 0: self.x = 0
        if self.x > MAP_WIDTH - self.width: self.x = MAP_WIDTH - self.width
        if self.y < 0: self.y = 0
        if self.y > MAP_HEIGHT - self.height: self.y = MAP_HEIGHT - self.height

# --- GERAÇÃO DE CENÁRIO (MAPA) ---
# Formato: [x, y, largura, altura]
platforms = [[0, MAP_HEIGHT - 40, MAP_WIDTH, 40]] # Chão principal
# Gerar plataformas aleatórias pelo mapa grande
random.seed(42)
for _ in range(50):
    px = random.randint(100, MAP_WIDTH - 200)
    py = random.randint(200, MAP_HEIGHT - 150)
    pw = random.randint(100, 300)
    ph = 20
    platforms.append([px, py, pw, ph])

def draw_platforms():
    # Desenha as plataformas em Verde
    glColor3f(0.0, 0.8, 0.2)
    glBegin(GL_QUADS)
    for p in platforms:
        glVertex2f(p[0], p[1])
        glVertex2f(p[0] + p[2], p[1])
        glVertex2f(p[0] + p[2], p[1] + p[3])
        glVertex2f(p[0], p[1] + p[3])
    glEnd()

def draw_background_grid():
    # Linhas de grade para perceber o movimento no mapa grande
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for x in range(0, MAP_WIDTH, 100):
        glVertex2f(x, 0)
        glVertex2f(x, MAP_HEIGHT)
    for y in range(0, MAP_HEIGHT, 100):
        glVertex2f(0, y)
        glVertex2f(MAP_WIDTH, y)
    glEnd()

# --- LOOP PRINCIPAL ---
player = Player(100, MAP_HEIGHT - 150)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Atualizações
    player.update(platforms)
    camera.target(player)

    # Renderização OpenGL
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Aplica a matriz de visualização da câmera (Inverte as coordenadas da câmera)
    glTranslatef(-int(camera.x), -int(camera.y), 0)

    # Desenhar elementos do mundo (em coordenadas globais)
    draw_background_grid()
    draw_platforms()
    player.draw()

    pygame.display.flip()

pygame.quit()
