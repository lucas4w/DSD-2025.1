import pygame, random
import entities as ent

pygame.init()
screen = pygame.display.set_mode((800,600))

BACKGROUND_COLOR = (20, 20, 60)
jogador_area = pygame.Rect(100, 50, 232, 500)
adversario_area = pygame.Rect(500, 50, 232, 500)

quadrados = pygame.sprite.Group()
quadrados_pos = {}

def gerar_bloco_aleatorio(x=215, y=100):
    blocos = [
        ent.BlocoI,
        ent.BlocoB,
    ]
    classe_bloco = random.choice(blocos)

    return classe_bloco(x, y)

def apaga_linha(y):
    for x in range(105, 105 + 10*22, 22):
        quadrado = quadrados_pos.pop((x, y), None)
        if quadrado:
            quadrados.remove(quadrado)

def desce_linhas_acima(y_inicial):
    novas_pos = {}
    for (x, y), quadrado in sorted(quadrados_pos.items(), key=lambda item: -item[0][1]):
        if y < y_inicial:
            quadrado.y += 22
            quadrado.update_position()
            novas_pos[(x, y + 22)] = quadrado
        else:
            novas_pos[(x, y)] = quadrado
    quadrados_pos.clear()
    quadrados_pos.update(novas_pos)

def detecta_linhas():
    for y in range(528, 49, -22):
        count = 0
        for x in range(105, 105 + 10*22, 22):
            if (x, y) in quadrados_pos:
                count += 1
        if count == 10:
            apaga_linha(y)
            desce_linhas_acima(y)
            detecta_linhas()
            break

        
fall_time = 0
fall_delay = 125

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
                bloco_atual.update_x(22,screen)
            elif event.key == pygame.K_a:
                bloco_atual.update_x(-22,screen)
            elif event.key == pygame.K_k:
                bloco_atual.rotate(screen)
            elif event.key == pygame.K_r:
                quadrado = quadrados_pos[(105,528)]
                quadrado.move(105,506)

    if fall_time >= fall_delay:
        parou = bloco_atual.update_y(screen)
        fall_time = 0
        if parou:
            quadrados.add(bloco_atual.q1, bloco_atual.q2, bloco_atual.q3, bloco_atual.q4)
            quadrados_pos[(bloco_atual.q1.x,bloco_atual.q1.y)] = bloco_atual.q1
            quadrados_pos[(bloco_atual.q2.x,bloco_atual.q2.y)] = bloco_atual.q2
            quadrados_pos[(bloco_atual.q3.x,bloco_atual.q3.y)] = bloco_atual.q3
            quadrados_pos[(bloco_atual.q4.x,bloco_atual.q4.y)] = bloco_atual.q4
            detecta_linhas()
            bloco_atual = proximo_bloco
            proximo_bloco = gerar_bloco_aleatorio()

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, 'Black', jogador_area)
    pygame.draw.rect(screen, 'Black', adversario_area)
    quadrados.draw(screen)
    bloco_atual.show(screen)
    pygame.display.flip()

pygame.quit()
        