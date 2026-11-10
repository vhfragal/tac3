import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# --- CONFIGURAÇÕES DO JOGO ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 3000   
MAP_HEIGHT = 1200
GRAVITY = 0.5

pygame.init()
display = (SCREEN_WIDTH, SCREEN_HEIGHT)
# vsync=1 ativado para remover os flickers/rasgos de tela comentados antes
pygame.display.set_mode(display, DOUBLEBUF | OPENGL, vsync=1)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0) 
glMatrixMode(GL_MODELVIEW)

# --- CLASSES EXISTENTES (PLAYER & CAMERA) ---
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
        self.health = 80  # Vida do jogador (máximo 100)

    def update(self, platforms):
        self.vy += GRAVITY
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[K_LEFT]:  self.vx = -self.speed
        if keys[K_RIGHT]: self.vx = self.speed
        
        self.x += self.vx
        self.move_and_collide(platforms, 'x')
        
        if keys[K_SPACE] and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

        self.y += self.vy
        self.move_and_collide(platforms, 'y')

        if self.x < 0: self.x = 0
        if self.x > MAP_WIDTH - self.w: self.x = MAP_WIDTH - self.w
        if self.y > MAP_HEIGHT - self.h:
            self.y = MAP_HEIGHT - self.h
            self.vy = 0
            self.on_ground = True

    def move_and_collide(self, platforms, direction):
        for p in platforms:
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
        self.lerp_factor = 0.1

    def target(self, player):
        target_x = player.x + player.w / 2 - self.width / 2
        target_y = player.y + player.h / 2 - self.height / 2
        self.x += (target_x - self.x) * self.lerp_factor
        self.y += (target_y - self.y) * self.lerp_factor

        if self.x < 0: self.x = 0
        if self.x > MAP_WIDTH - self.width: self.x = MAP_WIDTH - self.width
        if self.y < 0: self.y = 0
        if self.y > MAP_HEIGHT - self.height: self.y = MAP_HEIGHT - self.height

# --- NOVA CLASSE: MOEDA (COIN) ---
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20

    def draw(self, angle):
        # Usamos Push/Pop para isolar a translação e rotação APENAS para esta moeda
        glPushMatrix()
        
        # 1. Move a origem para o CENTRO da moeda no mundo global
        glTranslatef(self.x + self.size/2, self.y + self.size/2, 0)
        
        # 2. Rotaciona no eixo Y (gira horizontalmente como uma moeda 3D)
        glRotatef(angle, 0.0, 1.0, 0.0)
        
        # Desenha a moeda centralizada em (0,0) local
        glColor3f(1.0, 0.85, 0.0) # Cor Dourada
        glBegin(GL_QUADS)
        half = self.size / 2
        glVertex2f(-half, -half)
        glVertex2f(half, -half)
        glVertex2f(half, half)
        glVertex2f(-half, half)
        glEnd()
        
        glPopMatrix() # Restaura o estado da matriz do mundo/câmera

# --- ELEMENTOS HUD FIXED ---
def draw_hud(player):
    # Como esta função é chamada FORA do bloco da câmera, ela renderiza fixo na tela
    # Fundo da Barra de Vida (Preto)
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(20, 20)
    glVertex2f(220, 20)
    glVertex2f(220, 40)
    glVertex2f(20, 40)
    glEnd()

    # Barra de Vida Atual (Verde)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(20, 20)
    glVertex2f(20 + player.health * 2, 20) # Redimensiona baseado na vida atual
    glVertex2f(20 + player.health * 2, 40)
    glVertex2f(20, 40)
    glEnd()

# --- GERAÇÃO DE MUNDO ---
platforms = [[0, MAP_HEIGHT - 40, MAP_WIDTH, 40]]
random.seed(42)
for _ in range(50):
    px = random.randint(100, MAP_WIDTH - 200)
    py = random.randint(200, MAP_HEIGHT - 150)
    pw = random.randint(100, 300)
    ph = 20
    platforms.append([px, py, pw, ph])

# Gerar moedas flutuando acima das plataformas
coins = []
for p in platforms[1:]: # Ignora o chão principal
    coins.append(Coin(p[0] + p[2]/2 - 10, p[1] - 40))

def draw_platforms():
    glColor3f(0.0, 0.8, 0.2)
    glBegin(GL_QUADS)
    for p in platforms:
        glVertex2f(p[0], p[1])
        glVertex2f(p[0] + p[2], p[1])
        glVertex2f(p[0] + p[2], p[1] + p[3])
        glVertex2f(p[0], p[1] + p[3])
    glEnd()

# --- LOOP PRINCIPAL ---
player = Player(100, MAP_HEIGHT - 150)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
clock = pygame.time.Clock()
coin_angle = 0
running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Atualizações
    player.update(platforms)
    camera.target(player)
    coin_angle = (coin_angle + 4) % 360 # Incrementa o ângulo para animar as moedas

    # Renderização OpenGL
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # -------------------------------------------------------------
    # CAMADA 1: MUNDO DO JOGO (Movimentado pela Câmera usando LERP)
    # -------------------------------------------------------------
    glPushMatrix() # <-- SALVA o estado zerado do OpenGL (Coordenadas da Tela)
    
    # Desloca todo o cenário de acordo com a câmera (arredondado para evitar jitter)
    glTranslatef(-round(camera.x), -round(camera.y), 0)

    # Desenha o mundo (A câmera se aplica a tudo aqui dentro)
    draw_platforms()
    
    for coin in coins:
        coin.draw(coin_angle) # Cada moeda gerencia seu próprio Push/Pop internamente
        
    player.draw()

    glPopMatrix() # <-- RESTAURA para o estado da tela (Ignora o movimento da câmera)

    # -------------------------------------------------------------
    # CAMADA 2: HUD / INTERFACE (Fixo na tela, ignora a câmera)
    # -------------------------------------------------------------
    draw_hud(player) # Renderizado em coordenadas absolutas da janela (0 a 800)

    pygame.display.flip()

pygame.quit()
