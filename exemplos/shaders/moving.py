import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plataformas Móveis Estáveis com Delta Time")
clock = pygame.time.Clock()

# --- CONFIGURAÇÕES DO MUNDO ---
MAP_WIDTH, MAP_HEIGHT = 3000, 1200  
GRAVIDADE_NORMAL = 1500                    
GRAVIDADE_QUEDA_RAPIDA = 4000  

# --- CONFIGURAÇÕES DO JOGADOR ---
pos_jogador = pygame.math.Vector2(200, 800)
vel_jogador = pygame.math.Vector2(0, 0)
VELOCIDADE_CORRIDA = 400
FORCA_PULO = -650              
esta_no_chao = False
raio_jogador = 20
direcao_olhar = 1 

# --- PLATAFORMAS FIXAS ---
plataformas_fixas = [
    pygame.Rect(0, 1000, 3000, 200),     
    pygame.Rect(400, 850, 200, 30),      
    pygame.Rect(1900, 750, 400, 30),     
]

# --- CLASSE DA PLATAFORMA MÓVEL ---
class PlataformaMovel:
    def __init__(self, x1, y1, x2, y2, width, height, velocidade):
        self.ponto_a = pygame.math.Vector2(x1, y1)
        self.ponto_b = pygame.math.Vector2(x2, y2)
        self.pos = pygame.math.Vector2(x1, y1)
        self.rect = pygame.Rect(x1, y1, width, height)
        
        self.velocidade_base = velocidade
        self.alvo = self.ponto_b
        self.deslocamento_frame = pygame.math.Vector2(0, 0) # Deslocamento exato feito NESTE frame

    def update(self, dt):
        direcao = self.alvo - self.pos
        distancia = direcao.length()
        
        if distancia > 1:
            direcao = direcao.normalize()
            self.deslocamento_frame = direcao * self.velocidade_base * dt
            
            # Evita que ultrapasse o ponto alvo
            if self.deslocamento_frame.length() > distancia:
                self.deslocamento_frame = direcao * distancia
                
            self.pos += self.deslocamento_frame
        else:
            # Inverte o destino ao chegar muito perto
            self.alvo = self.ponto_a if self.alvo == self.ponto_b else self.ponto_b
            self.deslocamento_frame = pygame.math.Vector2(0, 0)

        # Sincroniza o rect de colisão com a posição matemática float
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

# Criando duas plataformas móveis para testes
plataformas_moveis = [
    PlataformaMovel(x1=700, y1=850, x2=1300, y2=850, width=200, height=30, velocidade=150),  # Horizontal
    PlataformaMovel(x1=1500, y1=950, x2=1500, y2=650, width=200, height=30, velocidade=120)  # Vertical (Elevador)
]

# --- CONFIGURAÇÕES DA CÂMERA ---
offset_camera = pygame.math.Vector2(pos_jogador.x - SCREEN_WIDTH / 2, pos_jogador.y - SCREEN_HEIGHT / 2)
TAXA_SUAVIZACAO_X = 4.0   
TAXA_SUAVIZACAO_Y = 8.0   
DISTANCIA_LOOK_AHEAD = 150 

# Loop principal
running = True
while running:
    dt = clock.tick(60) / 1000.0

    keys = pygame.key.get_pressed()
    botao_pulo_pressionado = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP) and esta_no_chao:
                vel_jogador.y = FORCA_PULO
                esta_no_chao = False

    # ==========================================
    # 1. ATUALIZAR E MOVER AS PLATAFORMAS MÓVEIS
    # ==========================================
    plataforma_piso = None
    for plat in plataformas_moveis:
        plat.update(dt)
        
        # Checa se o jogador estava pisando nela no frame anterior
        # (Um pixel abaixo do pé do jogador para validar o contato firme)
        rect_sensor_pe = pygame.Rect(pos_jogador.x - raio_jogador, pos_jogador.y + raio_jogador, raio_jogador * 2, 2)
        if rect_sensor_pe.colliderect(plat.rect) and vel_jogador.y >= 0:
            plataforma_piso = plat

    # ==========================================
    # 2. TRANSPORTE DA PLATAFORMA PARA O JOGADOR
    # ==========================================
    if plataforma_piso:
        # Move o jogador exatamente com o mesmo deslocamento da plataforma
        pos_jogador.x += plataforma_piso.deslocamento_frame.x
        pos_jogador.y += plataforma_piso.deslocamento_frame.y

    # ==========================================
    # 3. MOVIMENTO DO PRÓPRIO JOGADOR (INPUT + FÍSICA)
    # ==========================================
    vel_jogador.x = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vel_jogador.x = -VELOCIDADE_CORRIDA
        direcao_olhar = -1 
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vel_jogador.x = VELOCIDADE_CORRIDA
        direcao_olhar = 1  

    # Gravidade Variável
    if vel_jogador.y < 0 and not botao_pulo_pressionado:
        vel_jogador.y += GRAVIDADE_QUEDA_RAPIDA * dt
    else:
        vel_jogador.y += GRAVIDADE_NORMAL * dt

    # --- RESOLUÇÃO DE COLISÃO X ---
    pos_jogador.x += vel_jogador.x * dt
    pos_jogador.x = max(raio_jogador, min(pos_jogador.x, MAP_WIDTH - raio_jogador))
    rect_jogador = pygame.Rect(pos_jogador.x - raio_jogador, pos_jogador.y - raio_jogador, raio_jogador * 2, raio_jogador * 2)
    
    for plat in plataformas_fixas:
        if rect_jogador.colliderect(plat):
            if vel_jogador.x > 0: pos_jogador.x = plat.left - raio_jogador
            if vel_jogador.x < 0: pos_jogador.x = plat.right + raio_jogador

    for plat in plataformas_moveis:
        if rect_jogador.colliderect(plat.rect):
            if vel_jogador.x > 0: pos_jogador.x = plat.rect.left - raio_jogador
            if vel_jogador.x < 0: pos_jogador.x = plat.rect.right + raio_jogador

    # --- RESOLUÇÃO DE COLISÃO Y ---
    pos_jogador.y += vel_jogador.y * dt
    pos_jogador.y = max(raio_jogador, min(pos_jogador.y, MAP_HEIGHT - raio_jogador))
    rect_jogador = pygame.Rect(pos_jogador.x - raio_jogador, pos_jogador.y - raio_jogador, raio_jogador * 2, raio_jogador * 2)
    
    esta_no_chao = False

    for plat in plataformas_fixas:
        if rect_jogador.colliderect(plat):
            if vel_jogador.y > 0: 
                pos_jogador.y = plat.top - raio_jogador
                vel_jogador.y = 0
                esta_no_chao = True
            elif vel_jogador.y < 0: 
                pos_jogador.y = plat.bottom + raio_jogador
                vel_jogador.y = 0

    for plat in plataformas_moveis:
        if rect_jogador.colliderect(plat.rect):
            if vel_jogador.y > 0: 
                pos_jogador.y = plat.rect.top - raio_jogador
                vel_jogador.y = 0
                esta_no_chao = True
            elif vel_jogador.y < 0: 
                pos_jogador.y = plat.rect.bottom + raio_jogador
                vel_jogador.y = 0

    # 4. CÂMERA LERP COM LOOK AHEAD
    shift_horizontal = direcao_olhar * DISTANCIA_LOOK_AHEAD
    alvo_camera = pygame.math.Vector2(
        pos_jogador.x - SCREEN_WIDTH / 2 + shift_horizontal,
        pos_jogador.y - (SCREEN_HEIGHT * 0.6)
    )
    offset_camera.x = pygame.math.lerp(offset_camera.x, alvo_camera.x, 1.0 - math.exp(-TAXA_SUAVIZACAO_X * dt))
    offset_camera.y = pygame.math.lerp(offset_camera.y, alvo_camera.y, 1.0 - math.exp(-TAXA_SUAVIZACAO_Y * dt))
    offset_camera.x = max(0, min(offset_camera.x, MAP_WIDTH - SCREEN_WIDTH))
    offset_camera.y = max(0, min(offset_camera.y, MAP_HEIGHT - SCREEN_HEIGHT))

    # 5. RENDERIZAÇÃO
    screen.fill((20, 24, 30))

    # Borda do Mapa
    borda_mapa = pygame.Rect(0 - int(offset_camera.x), 0 - int(offset_camera.y), MAP_WIDTH, MAP_HEIGHT)
    pygame.draw.rect(screen, (40, 45, 60), borda_mapa, 4)

    # Desenhar Plataformas Fixas (Cinza)
    for plat in plataformas_fixas:
        pos_render = pygame.Rect(plat.x - int(offset_camera.x), plat.y - int(offset_camera.y), plat.width, plat.height)
        pygame.draw.rect(screen, (100, 110, 130), pos_render)
        pygame.draw.rect(screen, (0, 180, 255), pos_render, 2)

    # Desenhar Plataformas Móveis (Amarelo Neon)
    for plat in plataformas_moveis:
        pos_render_movel = pygame.Rect(plat.rect.x - int(offset_camera.x), plat.rect.y - int(offset_camera.y), plat.rect.width, plat.rect.height)
        pygame.draw.rect(screen, (200, 180, 50), pos_render_movel)
        pygame.draw.rect(screen, (255, 255, 0), pos_render_movel, 2)

    # Desenhar o Personagem
    pos_jogador_render = (int(pos_jogador.x - offset_camera.x), int(pos_jogador.y - offset_camera.y))
    pygame.draw.circle(screen, (255, 200, 0), pos_jogador_render, raio_jogador)
    pygame.draw.circle(screen, (0, 0, 0), (pos_jogador_render[0] + (direcao_olhar * 12), pos_jogador_render[1] - 4), 4)

    pygame.display.flip()

pygame.quit()
sys.exit()
