import pygame

class Quadrado(pygame.sprite.Sprite):
    def __init__(self,x,y,cor):
        super().__init__()
        self.x = x
        self.y = y
        self.cor = cor
        self.image = pygame.Surface((20,20))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update_position(self):
        self.rect.topleft = (self.x,self.y)

    def move(self,x,y):
        self.x = x
        self.y = y
        self.update_position()

class Bloco(pygame.sprite.Sprite):
    def __init__(self, cor):
        super().__init__()
        self.cor = cor
        self.quadrados = pygame.sprite.Group()
        self.forma = 1
    
    def collide_direction(self, screen, quadrados, dx, dy):
        for q in quadrados:
            rgb = screen.get_at((q.x + dx, q.y + dy))
            if rgb != (0, 0, 0, 255):
                return True
        return False

    def collide_at(self,screen,cordenadas):
        for cord in cordenadas:
            rgb = screen.get_at((cord[0],cord[1]))
            if rgb != (0, 0, 0, 255):
                return True
        return False

    def show(self,screen):
        self.quadrados.draw(screen)

    def update_all(self):
        for q in self.quadrados:
            q.update_position()

class BlocoI(Bloco):
    def __init__(self,pos_x,pos_y):
        super().__init__('Yellow')
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        cor = 'Yellow'
        self.q1 = Quadrado(pos_x,pos_y,cor)
        self.q2 = Quadrado(pos_x,pos_y+22,cor)
        self.q3 = Quadrado(pos_x,pos_y+44,cor)
        self.q4 = Quadrado(pos_x,pos_y+66,cor)
        self.quadrados.add(self.q1, self.q2, self.q3, self.q4)
        
        self.rect = pygame.Rect(pos_x, pos_y, 20, 88)

    def update_x(self,direction,screen):
        if direction == 22:
            if self.forma == 1:
                if self.collide_direction(screen,[self.q1,self.q2,self.q3,self.q4],22,0):
                    return
            else:
                if self.collide_direction(screen,[self.q1],22,0):
                    return
        elif direction == -22:
            if self.forma == 1:
                if self.collide_direction(screen,[self.q1,self.q2,self.q3,self.q4],-22,0):
                    return
            else:
                if self.collide_direction(screen,[self.q4],-22,0):
                    return
        for q in self.quadrados:
            q.move(q.x + direction, q.y)

    def update_y(self,screen):
        if self.forma == 1: 
            if self.collide_direction(screen,[self.q4],0,22):
                return True
        else:
            if self.collide_direction(screen,[self.q1,self.q2,self.q3,self.q4],0,22):
                return True
        for q in self.quadrados:
            q.move(q.x, q.y + 22)
        return False

    def rotate(self,screen):
        if self.forma == 1:
            if self.collide_at(screen,[
                (self.q1.x+22,self.q1.y+44),
                (self.q2.x-22,self.q2.y+22),
                (self.q4.x+44,self.q4.y+44)]):
                return
            self.q1.x = self.q1.x+22
            self.q1.y = self.q1.y+44
            self.q2.x = self.q2.x-22
            self.q2.y = self.q2.y+22 
            self.q4.x = self.q4.x-44
            self.q4.y = self.q4.y-22
            self.update_all()
            self.forma = 2
            self.pos_x = self.q1.x
            self.pos_y = self.q1.y
        else:
            if self.collide_at(screen,[
                (self.q1.x-22,self.q1.y-44),
                (self.q2.x+22,self.q2.y-22),
                (self.q4.x+44,self.q4.y+22)]):
                return
            self.q1.x = self.q1.x-22
            self.q1.y = self.q1.y-44
            self.q2.x = self.q2.x+22
            self.q2.y = self.q2.y-22
            self.q4.x = self.q4.x+44
            self.q4.y = self.q4.y+22
            self.update_all()
            self.forma = 1
            self.pos_x = self.q1.x
            self.pos_y = self.q1.y


class BlocoB(Bloco):
    def __init__(self,pos_x,pos_y):
        super().__init__('Red')
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        cor = 'Red'
        self.q1 = Quadrado(pos_x,pos_y,cor)
        self.q2 = Quadrado(pos_x+22,pos_y,cor)
        self.q3 = Quadrado(pos_x,pos_y+22,cor)
        self.q4 = Quadrado(pos_x+22,pos_y+22,cor)
        self.quadrados.add(self.q1, self.q2, self.q3, self.q4)
        
        self.rect = pygame.Rect(pos_x, pos_y, 20, 88)

    def update_x(self,direction,screen):
        if direction == 22:
            if self.collide_direction(screen,[self.q2,self.q4],22,0):
                return
        elif direction == -22:
            if self.collide_direction(screen,[self.q1,self.q3],-22,0):
                return
        for q in self.quadrados:
            q.move(q.x + direction, q.y)

    def update_y(self,screen):
        if self.collide_direction(screen,[self.q4,self.q3],0,22):
            return True
     
        for q in self.quadrados:
            q.move(q.x, q.y + 22)
        return False

    def rotate(self,screen):
        pass

class BlocoZ(Bloco):
    def __init__(self,pos_x,pos_y):
        super().__init__('Red')
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        cor = 'Red'
        self.q1 = Quadrado(pos_x,pos_y,cor)
        self.q2 = Quadrado(pos_x+22,pos_y,cor)
        self.q3 = Quadrado(pos_x+22,pos_y+22,cor)
        self.q4 = Quadrado(pos_x+44,pos_y+22,cor)
        self.quadrados.add(self.q1, self.q2, self.q3, self.q4)
        
        self.rect = pygame.Rect(pos_x, pos_y, 20, 88)

    def update_x(self,direction,screen):
        if direction == 22:
            if self.forma == 1:
                if self.collide_direction(screen,[self.q2,self.q4],22,0):
                    return
            else:
                if self.collide_direction(screen,[self.q1,self.q3,self.q4],22,0):
                    return
        elif direction == -22:
            if self.forma == 1:
                if self.collide_direction(screen,[self.q1,self.q3],-22,0):
                    return
            else:
                if self.collide_direction(screen,[self.q1,self.q2,self.q3],-22,0):
                    return
        for q in self.quadrados:
            q.move(q.x + direction, q.y)

    def update_y(self,screen):
        if self.forma == 1: 
            if self.collide_direction(screen,[self.q1,self.q3,self.q4],0,22):
                return True
        else:
            if self.collide_direction(screen,[self.q3,self.q4],0,22):
                return True
        for q in self.quadrados:
            q.move(q.x, q.y + 22)
        return False

    def rotate(self,screen):
        if self.forma == 1:
            if self.collide_at(screen,[
                (self.q1.x+44,self.q1.y-22),
                (self.q4.x,self.q4.y-22)]):
                return
            self.q1.x = self.q1.x+44
            self.q1.y = self.q1.y-22 
            self.q4.y = self.q4.y-22
            self.update_all()
            self.forma = 2
            self.pos_x = self.q1.x
            self.pos_y = self.q1.y
        else:
            if self.collide_at(screen,[
                (self.q1.x-44,self.q1.y+22),
                (self.q4.x,self.q4.y+22)]):
                return
            self.q1.x = self.q1.x-44
            self.q1.y = self.q1.y+22
            self.q4.y = self.q4.y+22
            self.update_all()
            self.forma = 1
            self.pos_x = self.q1.x
            self.pos_y = self.q1.y

class BlocoS(Bloco):
    def __init__(self,pos_x,pos_y):
        super().__init__('Red')
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        cor = 'Red'
        self.q1 = Quadrado(pos_x,pos_y,cor)
        self.q2 = Quadrado(pos_x-22,pos_y,cor)
        self.q3 = Quadrado(pos_x-22,pos_y+22,cor)
        self.q4 = Quadrado(pos_x-44,pos_y+22,cor)
        self.quadrados.add(self.q1, self.q2, self.q3, self.q4)
        
        self.rect = pygame.Rect(pos_x, pos_y, 20, 88)

    def update_x(self,direction,screen):
        if direction == 22:
            if self.forma == 1:
                if self.collide_direction(screen,[self.q1,self.q3],22,0):
                    return
            else:
                if self.collide_direction(screen,[self.q1,self.q3,self.q4],22,0):
                    return
        elif direction == -22:
            if self.forma == 1:
                if self.collide_direction(screen,[self.q4,self.q2],-22,0):
                    return
            else:
                if self.collide_direction(screen,[self.q4,self.q2,self.q3],-22,0):
                    return
        for q in self.quadrados:
            q.move(q.x + direction, q.y)

    def update_y(self,screen):
        if self.forma == 1: 
            if self.collide_direction(screen,[self.q1,self.q3,self.q4],0,22):
                return True
        else:
            if self.collide_direction(screen,[self.q2,self.q4],0,22):
                return True
        for q in self.quadrados:
            q.move(q.x, q.y + 22)
        return False

    def rotate(self,screen):
        if self.forma == 1:
            if self.collide_at(screen,[
                (self.q3.x,self.q3.y-44),
                (self.q4.x+44,self.q4.y)]):
                return
            self.q3.y = self.q3.y-44 
            self.q4.x = self.q4.x+44
            self.update_all()
            self.forma = 2
            self.pos_x = self.q1.x
            self.pos_y = self.q1.y
        else:
            if self.collide_at(screen,[
                (self.q3.x,self.q3.y+44),
                (self.q4.x-44,self.q4.y)]):
                return
            self.q3.y = self.q3.y+44
            self.q4.x = self.q4.x-44
            self.update_all()
            self.forma = 1
            self.pos_x = self.q1.x
            self.pos_y = self.q1.y