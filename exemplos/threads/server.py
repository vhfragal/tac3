import socket
import time

HOST = "127.0.0.1"
PORT = 5555
TIMEOUT_LIMIT = 5.0  # Segundos até desconectar por inatividade


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    server_socket.settimeout(1.0)  # Evita que o recvfrom trave para sempre

    # Dicionário de clientes: {"player_id": {"address": (ip, porta), "last_seen": timestamp}}
    clients = {}

    print(f"[SERVIDOR] Rodando com Timeout em {HOST}:{PORT}")

    while True:
        current_time = time.time()

        try:
            # 1. Tenta receber dados da rede
            data, client_address = server_socket.recvfrom(1024)
            message = data.decode("utf-8")

            # Protocolo de movimento: "player_id,x,y"
            # Protocolo de desconexão voluntária: "player_id,quit"
            parts = message.split(",")
            player_id = parts[0]

            if parts[1] == "quit":
                if player_id in clients:
                    del clients[player_id]
                    # Avisa os outros para removerem esse jogador
                    disconnect_msg = f"{player_id},remove"
                    for c_id, c_info in clients.items():
                        server_socket.sendto(
                            disconnect_msg.encode("utf-8"), c_info["address"]
                        )
                    print(f"[LOGOUT] {player_id} saiu voluntariamente.")
                continue

            # Atualiza ou registra o jogador
            if player_id not in clients:
                print(f"[CONEXÃO] {player_id} conectado.")

            clients[player_id] = {
                "address": client_address,
                "last_seen": current_time,
            }

            # BROADCAST do movimento para os outros jogadores
            for c_id, c_info in clients.items():
                if c_id != player_id:
                    server_socket.sendto(data, c_info["address"])

        except socket.timeout:
            # Executado a cada 1 segundo se a rede estiver silenciosa
            pass
        except Exception as e:
            print(f"[ERRO] {e}")

        # 2. Verificação de TIMEOUT (Limpeza de Inativos)
        disconnected_players = []
        for p_id, p_info in list(clients.items()):
            if current_time - p_info["last_seen"] > TIMEOUT_LIMIT:
                disconnected_players.append(p_id)

        for p_id in disconnected_players:
            print(f"[TIMEOUT] {p_id} desconectado por inatividade.")
            del clients[p_id]
            # Avisa a rede para remover o fantasma
            disconnect_msg = f"{p_id},remove"
            for c_id, c_info in clients.items():
                server_socket.sendto(
                    disconnect_msg.encode("utf-8"), c_info["address"]
                )


if __name__ == "__main__":
    main()
