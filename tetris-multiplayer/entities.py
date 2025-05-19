import pygame

class Quadrado(pygame.sprite.Sprite):
    def __init__(self,x,y,cor):
        super().__init__()
        self.x = x
        self.y = y;
        self.cor = cor
        self.image = pygame.Surface((20,20))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update_position(self):
        self.rect.topleft = (self.x,self.y)

class BlocoI(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,cor):
        super().__init__()
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        self.cor = cor
        self.forma = 1

        self.q1 = Quadrado(pos_x,pos_y,cor)
        self.q2 = Quadrado(pos_x,pos_y+22,cor)
        self.q3 = Quadrado(pos_x,pos_y+44,cor)
        self.q4 = Quadrado(pos_x,pos_y+66,cor)

        self.group = pygame.sprite.Group()
        self.group.add(self.q1, self.q2, self.q3, self.q4)
        
        self.rect = pygame.Rect(pos_x, pos_y, 20, 88)
        
    def show(self,screen):
        self.group.draw(screen)
        
    def update_x(self,direction):
        self.pos_x += direction
        if self.forma == 1:
                self.q1.x = self.pos_x
                self.q2.x = self.pos_x
                self.q3.x = self.pos_x
                self.q4.x = self.pos_x
        else:
            if direction == 22:
                self.q1.x = self.pos_x
                self.q2.x = self.pos_x-22
                self.q3.x = self.pos_x-44
                self.q4.x = self.pos_x-66
            else:
                self.q1.x = self.pos_x
                self.q2.x = self.pos_x-22
                self.q3.x = self.pos_x-44
                self.q4.x = self.pos_x-66       
        self.update_all()

    def update_y(self,screen):
        if self.forma == 1:
            if self.collideDown(screen,self.q4.y,self.q4.x):
                return True
            self.pos_y += 22
            self.q1.y = self.pos_y
            self.q2.y = self.pos_y+22
            self.q3.y = self.pos_y+44
            self.q4.y = self.pos_y+66
        else:
            self.pos_y += 22
            self.q1.y = self.pos_y
            self.q2.y = self.pos_y
            self.q3.y = self.pos_y
            self.q4.y = self.pos_y
        self.update_all()
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
        
    def collideDown(self,screen,y,x):
        rgb = screen.get_at((x,y+22))
        if (rgb != (0,0,0,255)):
            return True
        
        #screen.set_at((x,y+22),(255,0,0))
        #print(self.q1.x,self.q1.y)