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
    
    def collideDown(self,screen,x,y):
        raise NotImplementedError()
    
    def collideLeft(self,screen,x,y):
        raise NotImplementedError()
    
    def collideRight(self,screen,x,y):
        raise NotImplementedError()


    def show(self,screen):
        self.quadrados.draw(screen)

class BlocoI(Bloco):
    def __init__(self,pos_x,pos_y,cor):
        super().__init__(cor)
        self.pos_x = pos_x 
        self.pos_y = pos_y 

        self.q1 = Quadrado(pos_x,pos_y,cor)
        self.q2 = Quadrado(pos_x,pos_y+22,cor)
        self.q3 = Quadrado(pos_x,pos_y+44,cor)
        self.q4 = Quadrado(pos_x,pos_y+66,cor)
        self.quadrados.add(self.q1, self.q2, self.q3, self.q4)
        
        self.rect = pygame.Rect(pos_x, pos_y, 20, 88)

    def collideDown(self, screen, x, y):
        rgb = screen.get_at((x,y+22))
        if rgb != (0,0,0,255):
            return True
        return False
    
    def collideLeft(self, screen, x, y):
        rgb = screen.get_at((x-22,y))
        if rgb != (0,0,0,255):
            return True
        return False
    
    def collideRight(self, screen, x, y):
        rgb = screen.get_at((x+22,y))
        if rgb != (0,0,0,255):
            return True
        return False

    def update_x(self,direction,screen):
        #if direction == 22:
           # if self.collideRight():
            #    return
        #elif direction == -22:
            #if self.collideLeft():
               # return
        for q in self.quadrados:
            q.move(q.x + direction, q.y)

    def update_y(self,screen):
        if self.collideDown(screen,self.q4.x,self.q4.y):
            return True
        for q in self.quadrados:
            q.move(q.x, q.y + 22)
        return False

    def rotate(self):
        if self.forma == 1:    
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
            pass
        
    def update_all(self):
        self.q1.update_position()
        self.q2.update_position()
        self.q3.update_position()
        self.q4.update_position()
    