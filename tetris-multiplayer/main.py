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

def apaga_linha(screen,x,y):
    print('apaga')


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
        print(count)
        if count == 10:
            apaga_linha(screen,x,y)
    count = 0
    x = cx
    y -= 22

        

fall_time = 0
fall_delay = 100

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
                bloco.group.remove(bloco.q1)
    
    if fall_time >= fall_delay:
        parou = bloco.update_y(screen)
        fall_time = 0
        if parou:
            quadrados.add(bloco.q1, bloco.q2, bloco.q3, bloco.q4)
            quadrados_pos[bloco.q4] = (bloco.q4.x,bloco.q4.y)
            bloco = ent.BlocoI(215,0,'Yellow')
            detecta_linhas(screen)

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, 'Black', jogador_area)
    pygame.draw.rect(screen, 'Black', adversario_area)


    quadrados.update()
    quadrados.draw(screen)
    screen.set_at((105,528),'Red')
    bloco.show(screen)
    pygame.display.flip()

pygame.quit()
        