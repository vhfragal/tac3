import pygame
import sys
import random
from abc import ABC, abstractmethod

# ==========================================
# 1. ARQUITETURA DO PADRÃO OBSERVER
# ==========================================

# Interface do Observador
class JogoObserver(ABC):
    @abstractmethod
    def notificar(self, evento: str, dados: dict) -> None:
        pass

# Sujeito (O objeto que gera os eventos)
class SujeitoJogo:
    def __init__(self):
        self._observadores = []

    def inscrever(self, observador: JogoObserver):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desinscrever(self, observador: JogoObserver):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def disparar_evento(self, evento: str, dados: dict = None):
        if dados is None:
            dados = {}
        for observador in self._observadores:
            observador.notificar(evento, dados)


# ==========================================
# 2. OBSERVADORES CONCRETOS
# ==========================================

# Observador 1: Cuida estritamente da pontuação
class GerenciadorPlacar(JogoObserver):
    def __init__(self):
        self.pontos = 0

    def notificar(self, evento: str, dados: dict):
        if evento == "coleta_moeda":
            self.pontos += dados.get("valor", 10)
            print(f"🏆 Placar atualizado: {self.pontos} pontos!")


# Observador 2: Cuida de efeitos visuais na tela
class GerenciadorEfeitos(JogoObserver):
    def __init__(self):
        self.cor_fundo_atual = (30, 30, 30)
        self.frames_efeito = 0

    def notificar(self, evento: str, dados: dict):
        if evento == "coleta_moeda":
            # Muda o fundo para uma cor aleatória brilhante ao coletar
            self.cor_fundo_atual = (random.randint(40, 80), random.randint(100, 150), random.randint(40, 80))
            self.frames_efeito = 10  # O efeito dura 10 frames

    def atualizar_efeito(self):
        # Retorna gradualmente à cor escura padrão
        if self.frames_efeito > 0:
            self.frames_efeito -= 1
            if self.frames_efeito == 0:
                self.cor_fundo_atual = (30, 30, 30)


# ==========================================
# 3. ENTIDADES DO JOGO (O JOGADOR É O SUJEITO)
# ==========================================

class Jogador(SujeitoJogo):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocidade = 6

    def mover(self, teclas, limite_largura, limite_altura):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < limite_largura:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.bottom < limite_altura:
            self.rect.y += self.velocidade

    def coletou_moeda(self):
        # O jogador não sabe quem está ouvindo, ele apenas grita que o evento aconteceu!
        self.disparar_evento("coleta_moeda", {"valor": 15})


# ==========================================
# 4. CONFIGURAÇÃO E LOOP DO PYGAME
# ==========================================

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pygame + Pattern Observer")
fonte = pygame.font.SysFont("Arial", 30)
relogio = pygame.time.Clock()

# Instanciando as classes
jogador = Jogador(400, 300)
placar = GerenciadorPlacar()
efeitos = GerenciadorEfeitos()

# Vinculando os observadores ao jogador (Inscrição)
jogador.inscrever(placar)
jogador.inscrever(efeitos)

# Criando a primeira moeda
moeda_rect = pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 20)

# Loop Principal
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Entrada do teclado e movimentação
    teclas = pygame.key.get_pressed()
    jogador.mover(teclas, LARGURA, ALTURA)

    # Verificação de Colisão (Lógica de Negócio)
    if jogador.rect.colliderect(moeda_rect):
        jogador.coletou_moeda()  # Dispara o Observer!
        # Reposiciona a moeda aleatoriamente
        moeda_rect.x = random.randint(50, 750)
        moeda_rect.y = random.randint(50, 550)

    # Atualiza efeitos visuais temporizados do observador
    efeitos.atualizar_efeito()

    # Renderização
    tela.fill(efeitos.cor_fundo_atual) # Cor controlada pelo Gerenciador de Efeitos
    
    # Desenha as entidades
    pygame.draw.rect(tela, (0, 128, 255), jogador.rect)   # Jogador Azul
    pygame.draw.rect(tela, (50, 205, 50), moeda_rect)     # Moeda Verde

    # Desenha o texto do placar na tela (Dados vindos do Gerenciador de Placar)
    texto_pontos = fonte.render(f"Pontos: {placar.pontos}", True, (255, 255, 255))
    tela.blit(texto_pontos, (20, 20))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()
