import queue
import threading
import pygame

# Inicialização do Pygame e do Mixer de Áudio
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# --- DICIONÁRIOS GLOBAIS DE ASSETS ---
# Seu código usará esses dicionários para desenhar ou tocar sons depois
ASSETS = {"images": {}, "sounds": {}}

# Lista detalhada dos assets que precisamos carregar
ASSETS_TO_LOAD = [
    {"type": "image", "key": "player", "path": "assets/player.png"},
    {"type": "image", "key": "background", "path": "assets/bg.png"},
    {"type": "image", "key": "enemy", "path": "assets/enemy.png"},
    {"type": "sound", "key": "laser", "path": "assets/laser.wav"},
    {"type": "sound", "key": "explosion", "path": "assets/explosion.wav"},
]


def asset_loader_thread(assets_list, result_queue):
    """Thread secundária: Carrega os arquivos do disco rígido sem travar o FPS."""
    total_files = len(assets_list)

    for index, asset in enumerate(assets_list):
        asset_type = asset["type"]
        key = asset["key"]
        path = asset["path"]

        # Variável para guardar o objeto carregado temporariamente
        loaded_obj = None

        try:
            # Em um cenário real, descomente as linhas abaixo.
            # Aqui usamos try/except caso o arquivo não exista no seu PC ainda.
            if asset_type == "image":
                # Carrega o arquivo, mas NÃO chama .convert() aqui dentro!
                # loaded_obj = pygame.image.load(path)
                loaded_obj = pygame.Surface(
                    (100, 100)
                )  # MOCK: Cria superfície vazia para teste
                loaded_obj.fill((0, 200, 255))
            elif asset_type == "sound":
                # Carrega o som na memória do mixer
                # loaded_obj = pygame.mixer.Sound(path)
                loaded_obj = "MOCK_SOUND_OBJECT"  # MOCK: Simula objeto de som

            # Simula um pequeno atraso de leitura de disco (remova no seu jogo real)
            pygame.time.wait(300)

        except Exception as e:
            print(f"Erro ao carregar {path}: {e}")

        # Calcula a porcentagem de progresso
        progress = int(((index + 1) / total_files) * 100)

        # Envia o item carregado de volta para a Main Thread
        result_queue.put(
            {
                "done": False,
                "progress": progress,
                "type": asset_type,
                "key": key,
                "object": loaded_obj,
            }
        )

    # Avisa que terminou tudo
    result_queue.put({"done": True, "progress": 100})


# --- INICIALIZAÇÃO DA FILA E DA THREAD ---
asset_queue = queue.Queue()
loading_thread = threading.Thread(
    target=asset_loader_thread, args=(ASSETS_TO_LOAD, asset_queue)
)
loading_thread.start()

# Variáveis de controle de estado
game_state = "LOADING"
current_progress = 0

# --- LOOP PRINCIPAL DO JOGO ---
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # 1. Eventos do Sistema
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Processamento da Fila de Carregamento (Apenas se estiver carregando)
    if game_state == "LOADING":
        try:
            while True:
                data = asset_queue.get_nowait()
                current_progress = data["progress"]

                if data["done"]:
                    game_state = "PLAYING"
                    break

                # Recebe o asset bruto da thread
                asset_type = data["type"]
                key = data["key"]
                obj = data["object"]

                if obj:
                    if asset_type == "image":
                        # CRUCIAL: Convertemos a imagem para o formato da tela
                        # Apenas a Main Thread tem permissão para fazer isso eficientemente
                        optimized_surface = obj.convert_alpha()
                        ASSETS["images"][key] = optimized_surface
                    elif asset_type == "sound":
                        ASSETS["sounds"][key] = obj

                asset_queue.task_done()
        except queue.Empty:
            pass

    # 3. Desenho e Renderização
    screen.fill((15, 15, 25))

    if game_state == "LOADING":
        # Renderiza o texto e a barra de progresso
        txt = font.render(
            f"Carregando Recursos: {current_progress}%", True, (240, 240, 240)
        )
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 40))

        # Desenha a barra de carregamento
        pygame.draw.rect(screen, (50, 50, 70), (WIDTH // 2 - 200, HEIGHT // 2, 400, 20))
        fill_w = int((current_progress / 100) * 400)
        pygame.draw.rect(
            screen, (0, 180, 255), (WIDTH // 2 - 200, HEIGHT // 2, fill_w, 20)
        )

    elif game_state == "PLAYING":
        # O jogo começou! Agora podemos usar os assets salvos no dicionário global
        txt = font.render(
            "Carregamento concluído com sucesso!", True, (0, 255, 150)
        )
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 60))

        # Exemplo: Desenhando um asset que foi carregado pela thread
        if "player" in ASSETS["images"]:
            screen.blit(
                ASSETS["images"]["player"],
                (WIDTH // 2 - 50, HEIGHT // 2),
            )

    pygame.display.flip()

pygame.quit()
