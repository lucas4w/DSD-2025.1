import pygame
import entities as ent

pygame.init()
screen = pygame.display.set_mode((800,600))

BACKGROUND_COLOR = (20, 20, 60)
jogador_area = pygame.Rect(100, 50, 232, 500)
adversario_area = pygame.Rect(500, 50, 232, 500)

quadrados = pygame.sprite.Group()
quadrados_pos = {}
bloco = ent.BlocoI(215,0,'Yellow')

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
fall_delay = 75

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
                bloco.update_x(22,screen)
            elif event.key == pygame.K_a:
                bloco.update_x(-22,screen)
            elif event.key == pygame.K_k:
                bloco.rotate()
            elif event.key == pygame.K_r:
                quadrado = quadrados_pos[(105,528)]
                quadrado.move(105,506)

    if fall_time >= fall_delay:
        parou = bloco.update_y(screen)
        fall_time = 0
        if parou:
            quadrados.add(bloco.q1, bloco.q2, bloco.q3, bloco.q4)
            quadrados_pos[(bloco.q1.x,bloco.q1.y)] = bloco.q1
            quadrados_pos[(bloco.q2.x,bloco.q2.y)] = bloco.q2
            quadrados_pos[(bloco.q3.x,bloco.q3.y)] = bloco.q3
            quadrados_pos[(bloco.q4.x,bloco.q4.y)] = bloco.q4
            bloco = ent.BlocoI(215,0,'Yellow')
            detecta_linhas()

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, 'Black', jogador_area)
    pygame.draw.rect(screen, 'Black', adversario_area)
    #screen.set_at((105, 462),(255,0,0,255))
    quadrados.draw(screen)
    bloco.show(screen)
    pygame.display.flip()

pygame.quit()
        