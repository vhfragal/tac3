import pygame
import sys

# Inicializa o Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Objeto com Brilho Verde - Corrigido")

def create_glow_source(radius, core_color, glow_color):
    """Cria uma superfície contendo o objeto central e seu brilho verde ao redor."""
    surf_size = radius * 2
    # Garante suporte completo a transparência (Alpha)
    glow_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
    
    center = (radius, radius)
    
    # 1. Desenha o efeito de brilho (de fora para dentro)
    for r in range(radius, 0, -1):
        t = (r / radius) ** 1.5
        alpha = int(140 * (1 - t))  # Opacidade máxima de 140
        
        # Desempacota os canais da cor e adiciona o Alpha manualmente
        current_glow = (glow_color[0], glow_color[1], glow_color[2], alpha)
        pygame.draw.circle(glow_surf, current_glow, center, r)
        
    # 2. Desenha o núcleo sólido do objeto no centro
    core_radius = int(radius * 0.25)
    pygame.draw.circle(glow_surf, core_color, center, core_radius)
    
    # Ponto de luz branca no centro
    pygame.draw.circle(glow_surf, (220, 255, 220), center, int(core_radius * 0.4))
    
    return glow_surf

# Definição estrita de cores (Tuplas RGB normais)
BACKGROUND_DARK = (10, 16, 12)
GLOW_GREEN = (0, 255, 100)       
CORE_GREEN = (150, 255, 180)     

# Gera o objeto brilhante
GREEN_ORB_RADIUS = 120
green_orb = create_glow_source(GREEN_ORB_RADIUS, CORE_GREEN, GLOW_GREEN)

# Posição centralizada
orb_pos = (WIDTH // 2 - GREEN_ORB_RADIUS, HEIGHT // 2 - GREEN_ORB_RADIUS)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Preenche a tela de fundo
    screen.fill(BACKGROUND_DARK)

    # Renderiza o objeto na tela
    screen.blit(green_orb, orb_pos)

    pygame.display.flip()
    clock.tick(60)
