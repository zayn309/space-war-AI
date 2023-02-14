
from abc import ABC, abstractmethod
import pygame

VEL = 5
BULLET_VEL = 7.0
MAX_BULLETS = 3
WIDTH, HEIGHT = 900, 500
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

class spaceship(ABC):
    def __init__(self,image,x,y,bullet_color, leftSide = True):
        self.image = image
        self.vel = VEL
        self.health = 10
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.award = []
        self.bullet_color = bullet_color
        self.leftSide = leftSide
        self.bullets = []
        self.bullet_vel = BULLET_VEL
        self.max_bullets = MAX_BULLETS
    def add_award(self,award):
        self.award.append(award)
    def move_left(self):
        self.rect.x -= self.vel
    def move_right(self):
        self.rect.x += self.vel
    def move_up(self):
        self.rect.y -= self.vel
    def move_down(self):
        self.rect.y += self.vel
    @abstractmethod
    def move(self,keys_pressed):
        pass
    
    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += self.bullet_vel * (1 if self.leftSide else -1) 
            if bullet.x > WIDTH or bullet.x<0:
                self.bullets.remove(bullet)
    def fire(self):
        if len(self.bullets) < self.max_bullets:
            bullet = pygame.Rect(self.rect.x + (self.rect.width * int(self.leftSide)),
                                self.rect.y + self.rect.height//2 - 2,10,5)
            self.bullets.append(bullet)
    def increase_max_bullets(self):
        self.max_bullets += 1
    def increase_bullet_speed(self):
        self.bullet_vel += 0.5

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, self.bullet_color, bullet)
        for a in self.award:
            a.draw(screen)
        

class leftSpaceShip(spaceship):
    def __init__(self,image,x,y,bullet_color):
        super().__init__(image,x,y,bullet_color)
    #override the abstract methods 
    def move(self,keys_pressed ): 
        if keys_pressed[pygame.K_a] and self.rect.x - self.vel > 0:  # LEFT
            self.move_left()
        if keys_pressed[pygame.K_d] and self.rect.x + self.vel + self.rect.width < BORDER.x:  # RIGHT
            self.move_right()
        if keys_pressed[pygame.K_w] and self.rect.y - self.vel > 0:  # UP
            self.move_up()
        if keys_pressed[pygame.K_s] and self.rect.y + self.vel + self.rect.height <HEIGHT:  # DOWN
            self.move_down()
    

class rightSpaceShipe(spaceship):

    def __init__(self,image,x,y,bullet_color):
        super().__init__(image,x,y,bullet_color,leftSide= False)
    def move(self,keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.x - self.vel > BORDER.x + BORDER.width:  # LEFT
            self.move_left()
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + self.vel + self.rect.width < WIDTH:  # RIGHT
            self.move_right()
        if keys_pressed[pygame.K_UP] and self.rect.y - self.vel > 0:  # UP
            self.move_up()
        if keys_pressed[pygame.K_DOWN] and self.rect.y + self.vel + self.rect.height < HEIGHT:  # DOWN
            self.move_down()
