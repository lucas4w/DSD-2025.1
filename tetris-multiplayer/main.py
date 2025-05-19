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

def move_quadrados(screen,y):
    x,cx = 105
    for _ in range(0,20):
        for _ in range(0,10):
            if screen.get_at((x,y)) != (0,0,0,255):
                quadrado = quadrados_pos[(x,y)]
                del quadrados_pos[(x,y)]
                quadrados_pos[(x,y+22)] = quadrado
                quadrado.move(x,y+22)
            x+=22
        y -= 22
        x = cx
 
def apaga_linha(y,screen):
    x = 105
    for _ in range(0,10):
        quadrado = quadrados_pos[(x,y)]
        quadrados.remove(quadrado)
        x += 22
    move_quadrados(screen,y-22)

def detecta_linhas(screen):
    x, y = 105,528
    cx = x
    count = 0
    for _ in range(0,20):
        for _ in range(0,10):
            if screen.get_at((x,y)) != (0,0,0,255):
                count += 1
            else:
                break
            x += 22
        if count == 10:
            apaga_linha(y,screen)
        count = 0
        x = cx
        y -= 22

        

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
                bloco.update_x(22)
            elif event.key == pygame.K_a:
                bloco.update_x(-22)
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
            detecta_linhas(screen)

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, 'Black', jogador_area)
    pygame.draw.rect(screen, 'Black', adversario_area)
    screen.set_at((105, 462),(255,0,0,255))
    quadrados.draw(screen)
    bloco.show(screen)
    pygame.display.flip()

pygame.quit()
        