
from abc import ABC, abstractmethod
import os
import pygame


BULLET_SPEED_AWARD = (255,0,0)
BULLET_COUNT_AWARD = (0,0,255)
HEALTH_INCREASE = (0,255,255)


temp = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'download.png')),(40,55))

class award(ABC):
    def __init__(self,color,x,y):
        self.color = color
        self.rect = temp.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = temp
        

    @abstractmethod
    def action(self,spaceship):
        pass

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class bullet_speed(award):
    def __init__(self,x,y):
        super().__init__(BULLET_SPEED_AWARD,x,y)

    def action(self,spaceship):
        spaceship.increase_bullet_speed()

class health_increase(award):
    def __init__(self,x,y):
        super().__init__(BULLET_SPEED_AWARD,x,y)

    def action(self,spaceship):
        spaceship.health += 1

class bullet_increas(award):
    def __init__(self,x,y):
        super().__init__(BULLET_COUNT_AWARD,x,y)
    def action(self, spaceship):
        if spaceship.max_bullets <5:
            spaceship.increase_max_bullets()
