import multiprocessing
import sys
import time
import pygame

# 1. Função que rodará em um PROCESSADOR SEPARADO (Processo Filho)
def render_logic_worker(output_queue):
    """Calcula lógica pesada fora da thread principal do Pygame."""
    x, y = 100, 250
    speed_x, speed_y = 5, 3

    while True:
        # Simula uma carga pesada de CPU (ex: física complexa ou IA)
        time.sleep(0.01)

        x += speed_x
        y += speed_y

        # Quica nas bordas (janela de 800x600, quadrado de 50x50)
        if x <= 0 or x >= 750:
            speed_x *= -1
        if y <= 0 or y >= 550:
            speed_y *= -1

        # Envia as novas coordenadas de forma segura para o processo principal
        output_queue.put((x, y))

# 2. Processo Principal (Pygame, Renderização e Eventos)
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame + Multiprocessing Exemplo")
    clock = pygame.time.Clock()

    # Cria uma fila segura para comunicação entre processos
    communication_queue = multiprocessing.Queue()

    # Inicializa e inicia o processo secundário
    worker_process = multiprocessing.Process(
        target=render_logic_worker, args=(communication_queue,)
    )
    worker_process.daemon = (
        True  # Garante que o processo fecha se o principal fechar
    )
    worker_process.start()

    # Posição inicial padrão do quadrado
    rect_pos = [100, 250]

    running = True
    while running:
        # Tratamento de eventos (OBRIGATÓRIO na thread principal)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Verifica se há novas posições calculadas pelo outro processador
        # Usamos um loop para pegar a posição mais recente e esvaziar a fila
        while not communication_queue.empty():
            rect_pos = communication_queue.get()

        # Desenho na tela (OBRIGATÓRIO na thread principal)
        screen.fill((30, 30, 30))  # Fundo escuro
        pygame.draw.rect(
            screen, (0, 255, 128), (*rect_pos, 50, 50)
        )  # Quadrado verde

        pygame.display.flip()
        clock.tick(60)  # Mantém o jogo a 60 FPS estáveis

    # Finalização limpa
    worker_process.terminate()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Necessário no Windows/macOS para evitar loops infinitos de criação de processos
    multiprocessing.freeze_support()
    main()
