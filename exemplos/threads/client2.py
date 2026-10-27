import socket
import sys
import threading
import pygame

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def network_receiver(sock, players_dict, lock):
    print("[REDE] Escutando pacotes UDP...")
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            message = data.decode("utf-8")
            parts = message.split(",")
            p_id = parts[0]

            with lock:
                # Se o comando for para remover o jogador (enviado pelo servidor)
                if parts[1] == "remove":
                    if p_id in players_dict:
                        del players_dict[p_id]
                else:
                    # Atualiza apenas a posição ALVO (target) na rede
                    target_x, target_y = int(parts[1]), int(parts[2])
                    if p_id in players_dict:
                        players_dict[p_id]["target"] = [target_x, target_y]
                    else:
                        # Se for um jogador novo, inicializa a tela onde ele está
                        players_dict[p_id] = {
                            "current": [target_x, target_y],
                            "target": [target_x, target_y],
                        }
        except Exception:
            break


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Multiplayer Client - LERP & Timeout")
    clock = pygame.time.Clock()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Identificação do jogador (Mude para rodar instâncias diferentes)
    my_id = "player_2"
    my_pos = [400, 300]
    speed = 5

    # Dicionário estruturado: {"id": {"current": [x, y], "target": [x, y]}}
    all_players = {
        my_id: {"current": list(my_pos), "target": list(my_pos)}
    }
    data_lock = threading.Lock()

    net_thread = threading.Thread(
        target=network_receiver, args=(client_socket, all_players, data_lock)
    )
    net_thread.daemon = True
    net_thread.start()

    running = True
    while running:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- 1. MOVIMENTAÇÃO LOCAL ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            my_pos[0] -= speed
            moved = True
        if keys[pygame.K_RIGHT]:
            my_pos[0] += speed
            moved = True
        if keys[pygame.K_UP]:
            my_pos[1] -= speed
            moved = True
        if keys[pygame.K_DOWN]:
            my_pos[1] += speed
            moved = True

        if moved:
            with data_lock:
                all_players[my_id]["target"] = list(my_pos)
                all_players[my_id]["current"] = list(my_pos)

            packet = f"{my_id},{my_pos[0]},{my_pos[1]}"
            try:
                client_socket.sendto(
                    packet.encode("utf-8"), (SERVER_IP, SERVER_PORT)
                )
            except:
                pass

        # --- 2. INTERPOLAÇÃO (LERP) ---
        # Executado a cada frame para suavizar os outros jogadores
        LERP_FACTOR = 0.15  # Quanto menor, mais suave (porém gera um micro delay)

        with data_lock:
            for p_id, data in all_players.items():
                if p_id != my_id:  # Não interpolamos nosso próprio boneco local
                    curr = data["current"]
                    targ = data["target"]
                    # Aplica a fórmula do LERP: atual = atual + (alvo - atual) * fator
                    curr[0] += (targ[0] - curr[0]) * LERP_FACTOR
                    curr[1] += (targ[1] - curr[1]) * LERP_FACTOR

        # --- 3. RENDERIZAÇÃO ---
        screen.fill((30, 30, 40))

        with data_lock:
            for p_id, data in all_players.items():
                color = (100, 255, 100) if p_id == my_id else (255, 100, 100)
                # Desenha baseado na posição CURRENT (suavizada)
                draw_pos = (int(data["current"][0]), int(data["current"][1]))
                pygame.draw.circle(screen, color, draw_pos, 20)

        pygame.display.flip()
        clock.tick(60)

    # Envia aviso de saída antes de fechar o app
    try:
        client_socket.sendto(
            f"{my_id},quit".encode("utf-8"), (SERVER_IP, SERVER_PORT)
        )
        client_socket.close()
    except:
        pass
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
