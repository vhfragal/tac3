import pygame
import sys

# Inicializa o Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Exemplo de Gradiente no Pygame")

def draw_gradient_v(surface, color1, color2, rect):
    """Desenha um gradiente vertical (cima para baixo) dentro de um retângulo."""
    # Cria uma superfície temporária com a largura e altura do retângulo
    gradient_surf = pygame.Surface((rect.width, rect.height))
    
    # Interpola a cor linha por linha
    for y in range(rect.height):
        # Calcula a proporção atual (de 0.0 a 1.0)
        t = y / rect.height
        
        # Interpola os canais R, G e B
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        
        # Desenha uma linha horizontal de 1 pixel de altura com a cor calculada
        pygame.draw.line(gradient_surf, (r, g, b), (0, y), (rect.width, y))
        
    # Copia a superfície do gradiente para a tela/superfície principal
    surface.blit(gradient_surf, rect)

def draw_gradient_h(surface, color1, color2, rect):
    """Desenha um gradiente horizontal (esquerda para direita) dentro de um retângulo."""
    gradient_surf = pygame.Surface((rect.width, rect.height))
    
    # Interpola a cor coluna por coluna
    for x in range(rect.width):
        t = x / rect.width
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        
        # Desenha uma linha vertical de 1 pixel de largura
        pygame.draw.line(gradient_surf, (r, g, b), (x, 0), (x, rect.height))
        
    surface.blit(gradient_surf, rect)

# Definição de cores (RGB)
DEEP_BLUE = (15, 32, 67)
LIGHT_BLUE = (84, 160, 255)
ORANGE = (255, 127, 80)
YELLOW = (255, 242, 0)

# Criando os retângulos de definição para cada lado da tela
left_rect = pygame.Rect(0, 0, WIDTH // 2, HEIGHT)
right_rect = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)

# Loop Principal do Jogo
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Limpa a tela
    screen.fill((0, 0, 0))

    # Lado esquerdo: Gradiente Vertical (Azul Escuro -> Azul Claro)
    draw_gradient_v(screen, DEEP_BLUE, LIGHT_BLUE, left_rect)
    
    # Lado direito: Gradiente Horizontal (Laranja -> Amarelo)
    draw_gradient_h(screen, ORANGE, YELLOW, right_rect)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)
