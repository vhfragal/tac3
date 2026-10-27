import pygame
import gc
import os
# Force SDL2 to optimize batch rendering updates
os.environ["SDL_RENDER_BATCHING"] = "1"

SCALE = 3
WIDTH, HEIGHT = (640*SCALE, 360*SCALE)
FPS = 60
BG_COLOR = pygame.Color("#74777481")
RED_ALPHA = (255, 75, 75, 120)    # 120 / 255 opacity
GREEN = (75, 255, 150)
ANTI_ALIASING = 4
RADIUS = 150*ANTI_ALIASING
SPEED = 500 # pixels por segundo * delta time


# Pre-initialize mixer with a 512 or 1024 buffer to minimize CPU timing interruptions
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
flags = pygame.FULLSCREEN | pygame.SCALED
#flags = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
clock = pygame.time.Clock()
running = True

# circulo na tela - pode ser transparente
diametro = (RADIUS*2, RADIUS*2)
surface = pygame.Surface(diametro, flags=pygame.SRCALPHA)
rect = surface.get_frect()
pygame.draw.rect(surface, (0,0,0), rect, 3)

# desenhar no meio da superficie
pygame.draw.circle(surface, GREEN, (RADIUS, RADIUS), RADIUS)
# para antialiasing
surface = pygame.transform.smoothscale_by(surface, 1/ANTI_ALIASING)
# atualiza novo tamanho
rect = surface.get_frect()
rect.center = (WIDTH//2, HEIGHT//2)
#surface.set_alpha(100)

pygame.image.save(surface, 'exemplos/generated/teste_circulo.png')

direction = pygame.math.Vector2(0, 0)
speed_boost = 1

gc.disable()
while running:  
    delta_time = clock.tick_busy_loop(FPS) / 1000.0 

    # tratamento de eventos 
    for event in pygame.event.get():
        # fechar a janela
        if event.type == pygame.QUIT:
            running = False
        # esc para sair...
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect.center = pygame.mouse.get_pos()

    # teclado - fora do loop de eventos- continuo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        direction.x = -1           
    elif keys[pygame.K_RIGHT]:
        direction.x = 1  
    else: 
        direction.x = 0             

    if keys[pygame.K_UP]:
        direction.y = -1            
    elif keys[pygame.K_DOWN]:
        direction.y = 1      
    else:
        direction.y = 0

    if keys[pygame.K_LSHIFT]:
        speed_boost = 2
    else:
        speed_boost = 1

    # Normalizar diagonal
    if direction.x != 0 and direction.y != 0:
        # 0.7071 is approx 1 / sqrt(2)
        direction.x *= 0.7071
        direction.y *= 0.7071

    # aplicar velocidade
    rect.x += direction.x * SPEED * speed_boost * delta_time
    rect.y += direction.y * SPEED * speed_boost * delta_time

            
    screen.fill(BG_COLOR)    
    #desenhe algo
    screen.blit(surface, rect)

    pygame.display.flip()
    clock.tick(FPS)

gc.enable()
pygame.quit()