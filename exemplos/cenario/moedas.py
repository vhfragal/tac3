import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# --- CONFIGURAÇÕES DO JOGO ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 3000   
MAP_HEIGHT = 1200
GRAVITY = 0.5

pygame.init()
display = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL, vsync=1)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0) 
glMatrixMode(GL_MODELVIEW)

# --- CONFIGURAÇÃO DE ILUMINAÇÃO (OPENGL PIPELINE FIXED) ---
glEnable(GL_LIGHTING)   # Ativa o sistema global de luzes
glEnable(GL_LIGHT0)     # Ativa a primeira fonte de luz (Luz 0)
glEnable(GL_COLOR_MATERIAL) # Permite misturar cores básicas (glColor) com iluminação
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# Propriedades da Luz
light_ambient = [0.3, 0.3, 0.3, 1.0]  # Luz ambiente (revela um pouco das sombras)
light_diffuse = [1.0, 1.0, 1.0, 1.0]  # Luz direta branca (brilho do sol)
light_position = [400.0, 300.0, 500.0, 1.0] # Posicionada à frente da tela (Z positivo)

glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
glLightfv(GL_LIGHT0, GL_POSITION, light_position)

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
        self.health = 100 
        self.score = 0  # Pontuação de moedas coletadas

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

    def check_coin_collisions(self, coins):
        # Caixa de colisão AABB simples do jogador com as moedas ativos
        for coin in coins[:]:
            if (self.x < coin.x + coin.size and self.x + self.w > coin.x and
                self.y < coin.y + coin.size and self.y + self.h > coin.y):
                coins.remove(coin)
                self.score += 1 # Soma pontos
                if self.health < 100: self.health += 5 # Recupera um pouco de vida

    def draw(self):
        glColor3f(1.0, 0.2, 0.2)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0) # Normal apontando para fora da tela
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

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 22

    def draw(self, angle):
        glPushMatrix()
        glTranslatef(self.x + self.size/2, self.y + self.size/2, 0)
        glRotatef(angle, 0.0, 1.0, 0.0) # Rotação no próprio eixo Y
        
        glColor3f(1.0, 0.85, 0.0) # Cor dourada
        
        # Ajustando propriedades de reflexo material do OpenGL para a moeda brilhar
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0) # Quanto maior, mais concentrado é o brilho metálico
        
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0) # Importante para a luz calcular o sombreamento dinâmico
        half = self.size / 2
        glVertex2f(-half, -half)
        glVertex2f(half, -half)
        glVertex2f(half, half)
        glVertex2f(-half, half)
        glEnd()
        
        glPopMatrix()

# --- INTERFACE HUD ---
def draw_hud(player):
    # Desativa temporariamente a iluminação para a HUD não sofrer sombreamentos
    glDisable(GL_LIGHTING)
    
    # Fundo da Barra de Vida (Preto)
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(20, 20)
    glVertex2f(220, 20)
    glVertex2f(220, 35)
    glVertex2f(20, 35)
    glEnd()

    # Barra de Vida Atual (Verde)
    glColor3f(0.0, 1.0, 0.4)
    glBegin(GL_QUADS)
    glVertex2f(20, 20)
    glVertex2f(20 + player.health * 2, 20)
    glVertex2f(20 + player.health * 2, 35)
    glVertex2f(20, 35)
    glEnd()

    # Representação Gráfica Simples do Contador de Pontos (Quadrados Dourados)
    glColor3f(1.0, 0.85, 0.0)
    for i in range(player.score):
        # Desenha pequenos blocos representando as moedas coletadas
        glBegin(GL_QUADS)
        bx = 20 + (i * 15)
        by = 45
        glVertex2f(bx, by)
        glVertex2f(bx + 10, by)
        glVertex2f(bx + 10, by + 10)
        glVertex2f(bx, by + 10)
        glEnd()

    glEnable(GL_LIGHTING) # Reativa para o restante do cenário no próximo ciclo

# --- GERAÇÃO DE MUNDO ---
platforms = [[0, MAP_HEIGHT - 40, MAP_WIDTH, 40]]
random.seed(15)
for _ in range(45):
    px = random.randint(100, MAP_WIDTH - 300)
    py = random.randint(200, MAP_HEIGHT - 150)
    pw = random.randint(120, 300)
    ph = 20
    platforms.append([px, py, pw, ph])

coins = []
for p in platforms[1:]:
    # Gera moedas centralizadas ligeiramente flutuando sobre as plataformas
    coins.append(Coin(p[0] + p[2]/2 - 11, p[1] - 45))

def draw_platforms():
    glColor3f(0.2, 0.5, 0.8) # Plataformas azuis opacas para contrastar com as moedas
    glBegin(GL_QUADS)
    for p in platforms:
        glNormal3f(0.0, 0.0, 1.0)
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

    # Lógica do Jogo
    player.update(platforms)
    player.check_coin_collisions(coins) # Processa as coletas
    camera.target(player)
    coin_angle = (coin_angle + 5) % 360 

    # Renderização
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Atualiza a posição da luz em relação à câmera para o brilho seguir a tela de forma estável
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # CAMADA 1: MUNDO (Com câmera e Iluminação ativa)
    glPushMatrix() 
    glTranslatef(-round(camera.x), -round(camera.y), 0)

    draw_platforms()
    for coin in coins:
        coin.draw(coin_angle)
    player.draw()

    glPopMatrix() 

    # CAMADA 2: HUD (Fixa e plana)
    draw_hud(player)

    pygame.display.flip()

pygame.quit()
