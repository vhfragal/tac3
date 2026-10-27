import pygame
import sys

# 1. CONFIGURAÇÕES GLOBAIS
WIDTH, HEIGHT = 1920, 1080
FPS = 60
BG_COLOR = (30, 30, 40)      # Azul escuro/cinza
PLAYER_COLOR = (255, 100, 100) # Vermelho pastel

class Player(pygame.sprite.Sprite):
    """Classe que gerencia o personagem, suas físicas básicas e inputs."""
    def __init__(self, x, y):
        super().__init__()
        # Cria um quadrado temporário enquanto não há sprites carregados
        self.image = pygame.Surface((40, 60))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_frect(topleft=(x, y))
        
        # Vetores de movimento e física
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300  # Pixels por segundo (multiplicado pelo delta time)
        self.gravity = 1200
        self.jump_speed = -500
        self.is_grounded = False

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Movimentação Horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Pulo
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.is_grounded:
            self.direction.y = self.jump_speed
            self.is_grounded = False

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y * dt

    def update(self, dt):
        self.get_input()
        
        # Atualiza posição horizontal baseada no tempo delta (dt)
        self.rect.x += self.direction.x * self.speed * dt
        self.apply_gravity(dt)
        
        # Simulação temporária de colisão com o "chão" da tela
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.direction.y = 0
            self.is_grounded = True


class GameEngine:
    """A Engine Pura: Controla o ciclo de vida, janelas, eventos e loops."""
    def __init__(self):
        pygame.init()
        # Define a janela do jogo
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
        pygame.display.set_caption("Minha Custom Engine 2D - Pygame")
        
        # Relógio para controle de quadros e cálculo de Delta Time
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicialização de entidades usando os Grupos do Pygame (Otimização nativa)
        self.player = Player(100, 100)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        """O Game Loop Principal"""
        while self.running:
            # Captura o tempo decorrido desde o último quadro em segundos (Delta Time)
            # Limita o FPS máximo para não estressar o processador desnecessariamente
            dt = self.clock.tick(FPS) / 1000.0 
            
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Loop de Eventos: Inputs globais do sistema e interrupções"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        """Loop de Atualização: Onde a lógica matemática acontece"""
        self.all_sprites.update(dt)

    def draw(self):
        """Loop de Renderização: Onde desenhamos na tela"""
        self.screen.fill(BG_COLOR)  # Limpa a tela com a cor de fundo
        
        # Desenha uma linha simulando o chão da fase
        pygame.draw.line(self.screen, (100, 100, 100), (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 4)
        
        # Desenha todas as entidades registradas no grupo de sprites
        self.all_sprites.draw(self.screen)
        
        # Atualiza o buffer da tela para o monitor do jogador
        pygame.display.flip()


if __name__ == "__main__":
    # Instancia e roda o motor de jogo
    engine = GameEngine()
    engine.run()