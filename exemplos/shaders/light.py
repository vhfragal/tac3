import pygame
import sys
import math

# Inicializa o Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efeito de Luz Dinâmica no Pygame")

def create_light_surf(radius, color):
    """Cria uma superfície quadrada contendo um gradiente radial transparente (luz)."""
    # Superfície precisa ter suporte a Alpha (SRCALPHA)
    light_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    
    # Desenha círculos concêntricos de fora para dentro mudando a opacidade
    for r in range(radius, 0, -1):
        # Interpolação não-linear (quadrática) para suavizar a borda da luz
        t = (r / radius) ** 2
        alpha = int(255 * (1 - t))
        
        # Cor da luz com o canal Alpha calculado
        light_color = (color[0], color[1], color[2], alpha)
        
        # Desenha o círculo correspondente a esse raio
        pygame.draw.circle(light_surf, light_color, (radius, radius), r)
        
    return light_surf

# Cores do cenário
DARK_BG = (15, 15, 25)
WALL_COLOR = (70, 70, 85)
LIGHT_COLOR = (255, 230, 180) # Luz quente/amarelada

# Raio da nossa fonte de luz
LIGHT_RADIUS = 200

# Criamos a superfície da luz APENAS UMA VEZ para performance
light_mask = create_light_surf(LIGHT_RADIUS, LIGHT_COLOR)

# Retângulos de obstáculo para simular um cenário
obstacles = [
    pygame.Rect(150, 200, 100, 150),
    pygame.Rect(450, 150, 200, 80),
    pygame.Rect(300, 400, 120, 100)
]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 1. Desenha o fundo escuro e os obstáculos da cena
    screen.fill(DARK_BG)
    for obs in obstacles:
        pygame.draw.rect(screen, WALL_COLOR, obs)

    # 2. Pega a posição do mouse para ser o centro da luz
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 3. Renderiza a luz na tela
    # Subtraímos o raio para alinhar o centro da imagem ao cursor do mouse
    light_pos = (mouse_x - LIGHT_RADIUS, mouse_y - LIGHT_RADIUS)
    
    # O segredo do efeito está no BLEND_RGBA_ADD: 
    # Ele soma os valores de cor da luz com os do cenário, criando um efeito de brilho real
    screen.blit(light_mask, light_pos, special_flags=pygame.BLEND_RGBA_ADD)

    pygame.display.flip()
    clock.tick(60)
