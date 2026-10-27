import pygame

SCALE = 3
WIDTH, HEIGHT = (640*SCALE, 360*SCALE)
FPS = 60
BG_COLOR = pygame.Color("#74777481")
RED_ALPHA = (255, 75, 75, 120)    # 120 / 255 opacity
GREEN = (75, 255, 150)
ANTI_ALIASING = 4
RADIUS = 150*ANTI_ALIASING

pygame.init()
flags = pygame.FULLSCREEN | pygame.SCALED
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


while running:  
    delta_time = clock.tick(FPS) / 1000.0 

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
            x,y = pygame.mouse.get_pos()
            if rect.collidepoint(x,y):
                rect.center = (x,y)

    # get mouse pos
    mouse_press = pygame.mouse.get_pressed()    
    if mouse_press[0]:
        x, y = pygame.mouse.get_pos()
        if rect.collidepoint(x,y):
            rect.center = (x,y)

            
    screen.fill(BG_COLOR)    
    #desenhe algo
    screen.blit(surface, rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()