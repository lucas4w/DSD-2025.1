import pygame, random, socket, pickle, threading
import entities as ent

pygame.init()
font_gameover = pygame.font.SysFont("Arial", 40, bold=True)
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Tetris Multiplayer")


BACKGROUND_COLOR = (20, 20, 60)
jogador_area = pygame.Rect(100, 50, 225, 505)
adversario_area = pygame.Rect(500, 50, 225, 505)
proximo_bloco_area = pygame.Rect(325, 100, 130, 145)

a = pygame.Rect()

# grupo e estado
quadrados = pygame.sprite.Group()
quadrados_pos = {}

# estado do adversário
bloco_adversario = []
quadrados_adversario = []
status_adversario = None

def gerar_bloco_aleatorio(x=215, y=94):
    blocos = [ent.BlocoL]
    return random.choice(blocos)(x, y)

def verifica_game_over(bloco):
    for q in [bloco.q1, bloco.q2, bloco.q3, bloco.q4]:
        if q.y == 116:
            return True
    return False

def apaga_linha(y):
    for x in range(105, 105 + 10*22, 22):
        quadrado = quadrados_pos.pop((x, y), None)
        if quadrado:
            quadrados.remove(quadrado)

def desce_linhas_acima(y_inicial):
    novas_pos = {}
    quadrados_sorted = sorted(list(quadrados), key=lambda q: -q.y)
    for q in quadrados_sorted:
        if q.y < y_inicial:
            q.y += 22
            q.update_position()
        novas_pos[(q.x, q.y)] = q
    quadrados_pos.clear()
    quadrados_pos.update(novas_pos)

def detecta_linhas():
    for y in range(534, 49, -22):
        contador = 0
        for x in range(105, 105 + 10*22, 22):
            if (x, y) in quadrados_pos:
                contador += 1
        if contador == 10:
            apaga_linha(y)
            desce_linhas_acima(y)
            detecta_linhas()
            break

def mostrar_tela_game_over(texto):
    screen.fill((0, 0, 0))
    msg = font_gameover.render(texto, True, (255, 0, 0))
    screen.blit(msg, (screen.get_width() // 2 - msg.get_width() // 2,
                      screen.get_height() // 2 - msg.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

SERVER_IP = '10.25.2.47'
TCP_PORT = 12345
UDP_PORT = 12346

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('', 0))  # bind em uma porta livre
udp_addr = udp_sock.getsockname()

# conexão TCP para registro inicial
""" tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((SERVER_IP, TCP_PORT))
tcp_sock.sendall(pickle.dumps(udp_addr))

print("Aguardando outro jogador...")
while True:
    try:
        resposta = tcp_sock.recv(1024)
        if not resposta:
            continue
        msg = pickle.loads(resposta)
        if msg == "start":
            print("Outro jogador conectado! Iniciando jogo...")
            break
    except:
        continue """

print("Registrado no servidor.")

def receive_udp():
    global status_adversario,bloco_adversario, quadrados_adversario
    while True:
        try:
            data, _ = udp_sock.recvfrom(4096)
            pacote = pickle.loads(data)
            if 'bloco' in pacote:
                bloco_adversario = pacote['bloco']
            if 'fixos' in pacote:
                quadrados_adversario = pacote['fixos']
            if 'status' in pacote:
                status_adversario = pacote['status']
        except:
            continue

threading.Thread(target=receive_udp, daemon=True).start()

# estado do jogo
fall_time = 0
fall_delay = 300
bloco_atual = gerar_bloco_aleatorio()
proximo_bloco = gerar_bloco_aleatorio()

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                bloco_atual.update_x(22, screen)
            elif event.key == pygame.K_a:
                bloco_atual.update_x(-22, screen)
            elif event.key == pygame.K_k:
                bloco_atual.rotate(screen)

    if fall_time >= fall_delay:
        parou = bloco_atual.update_y(screen)
        print(bloco_atual.q1.x,bloco_atual.q1.y)
        fall_time = 0
        # monta dados para envio via UDP
        outgoing_data = {
            'bloco': [
                {'x': bloco_atual.q1.x, 'y': bloco_atual.q1.y, 'cor': bloco_atual.q1.cor},
                {'x': bloco_atual.q2.x, 'y': bloco_atual.q2.y, 'cor': bloco_atual.q2.cor},
                {'x': bloco_atual.q3.x, 'y': bloco_atual.q3.y, 'cor': bloco_atual.q3.cor},
                {'x': bloco_atual.q4.x, 'y': bloco_atual.q4.y, 'cor': bloco_atual.q4.cor},
            ],
            'fixos': [
                {'x': q.x, 'y': q.y, 'cor': q.cor}
                for q in quadrados_pos.values()
            ]
        }
        udp_sock.sendto(pickle.dumps(outgoing_data), (SERVER_IP, UDP_PORT))

        if parou:
            if verifica_game_over(bloco_atual):
                outgoing_data = {'status': 'perdeu'}
                udp_sock.sendto(pickle.dumps(outgoing_data), (SERVER_IP, UDP_PORT))
                mostrar_tela_game_over("Você perdeu!")
                running = False
                break
            for q in [bloco_atual.q1, bloco_atual.q2, bloco_atual.q3, bloco_atual.q4]:
                quadrados.add(q)
                quadrados_pos[(q.x, q.y)] = q
            detecta_linhas()
            bloco_atual = proximo_bloco
            proximo_bloco = gerar_bloco_aleatorio()

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, 'Black', jogador_area)
    pygame.draw.rect(screen, 'Black', adversario_area)
    pygame.draw.rect(screen, 'Cyan', jogador_area, width=1)
    pygame.draw.rect(screen, 'White', adversario_area, width=1) 
    pygame.draw.rect(screen, 'White', proximo_bloco_area, width=2)
    texto = pygame.font.SysFont("Arial", 20).render("Próximo:", True, (255, 255, 255))
    screen.blit(texto, (proximo_bloco_area.x + 10, proximo_bloco_area.y + 5))
    quadrados.draw(screen)
    bloco_atual.show(screen)

    # desenha bloco atual do adversário
    for quad in bloco_adversario:
        pygame.draw.rect(
            screen,
            quad['cor'],
            pygame.Rect(quad['x'] + 400, quad['y'], 20, 20)
        )

    # desenha quadrados fixos do adversário
    for quad in quadrados_adversario:
        pygame.draw.rect(
            screen,
            quad['cor'],
            pygame.Rect(quad['x'] + 400, quad['y'], 20, 20)
        )
    
    for quad in [proximo_bloco.q1, proximo_bloco.q2, proximo_bloco.q3, proximo_bloco.q4]:
        offset_x = 372 
        offset_y = 140
        pygame.draw.rect(
            screen,
            quad.cor,
            pygame.Rect(quad.x - 215 + offset_x, quad.y - 94 + offset_y, 20, 20)
        )
    if status_adversario == 'perdeu':
        mostrar_tela_game_over("Você venceu!")
        running = False
    pygame.display.flip()

pygame.quit()
