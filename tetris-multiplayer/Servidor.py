import socket
import threading
import pickle

TCP_HOST = '0.0.0.0'
TCP_PORT = 12345
UDP_PORT = 12346

clientes_tcp = {}
clientes_udp = {}

lock = threading.Lock()

def handle_tcp_connection(conn, addr, jogador_id):
    print(f"Jogador {jogador_id} conectado via TCP: {addr}")
    with lock:
        clientes_tcp[jogador_id] = conn

        if len(clientes_tcp) == 2:
            print("[TCP] Ambos os jogadores conectados! Enviando sinal de início...")
            for sock in clientes_tcp.values():
                try:
                    sock.sendall(pickle.dumps("start"))
                except:
                    pass


def tcp_server():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((TCP_HOST, TCP_PORT))
    tcp_sock.listen()

    print(f"[TCP] Servidor aguardando conexões na porta {TCP_PORT}...")
    jogador_id = 1

    while jogador_id <= 2:
        conn, addr = tcp_sock.accept()
        threading.Thread(target=handle_tcp_connection, args=(conn, addr, jogador_id)).start()
        jogador_id += 1

def udp_server():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((TCP_HOST, UDP_PORT))
    print(f"[UDP] Servidor aguardando mensagens na porta {UDP_PORT}...")

    while True:
        data, addr = udp_sock.recvfrom(4096)
        with lock:
            if addr not in clientes_udp.values():
                # Registra novo cliente UDP
                if 1 not in clientes_udp:
                    clientes_udp[1] = addr
                    print(f"Registrado jogador 1 via UDP: {addr}")
                elif 2 not in clientes_udp:
                    clientes_udp[2] = addr
                    print(f"Registrado jogador 2 via UDP: {addr}")

            # Descobre qual cliente enviou e repassa para o outro
            remetente_id = None
            for id_, udp_addr in clientes_udp.items():
                if udp_addr == addr:
                    remetente_id = id_
                    break

            if remetente_id is not None:
                destinatario_id = 1 if remetente_id == 2 else 2
                if destinatario_id in clientes_udp:
                    udp_sock.sendto(data, clientes_udp[destinatario_id])

if __name__ == '__main__':
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()

    print("Servidor rodando... Pressione Ctrl+C para sair.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Servidor encerrado.")
