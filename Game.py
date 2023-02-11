import pygame
import os
from spaceship import *

pygame.font.init()

WIDTH, HEIGHT = 900, 500
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('arial', 30)
WINNER_FONT = pygame.font.SysFont('arial', 100)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
        os.path.join('Assets', 'spaceship_yellow.png'))

RED_SPACESHIP_IMAGE = pygame.image.load(
        os.path.join('Assets', 'spaceship_red.png'))

SPACE = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
        YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

class Game:
    
    def __init__(self,screen):
        self.yellow = leftSpaceShip(YELLOW_SPACESHIP,100,300,YELLOW)
        self.red = rightSpaceShipe(RED_SPACESHIP,700,300,RED)
        self.screen= screen
        self.winner_text = ""
        
    def red_bullet_collision(self):
        for bullet in self.yellow.bullets:
            if self.red.rect.colliderect(bullet):
                self.red.health -=1
                self.yellow.bullets.remove(bullet)
                return True
            
    def yellow_bullet_collision(self):
        for bullet in self.red.bullets:
            if self.yellow.rect.colliderect(bullet):
                self.yellow.health -=1
                self.red.bullets.remove(bullet)
                return True
            
    def yellow_award_collision(self):
        for a in self.yellow.award:
            if self.yellow.rect.colliderect(a):
                a.action(self.yellow)
                self.yellow.award.remove(a)
                return True
            
    def red_award_collision(self):
        for a in self.red.award:
            if self.red.rect.colliderect(a):
                a.action(self.red)
                self.red.award.remove(a)
                return True
            
    def draw_health(self):
        red_health_text = HEALTH_FONT.render(
            "Health: " + str(self.red.health), True, WHITE)
        yellow_health_text = HEALTH_FONT.render(
            "Health: " + str(self.yellow.health), True, WHITE)
        self.screen.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        self.screen.blit(yellow_health_text, (10, 10))

    def draw_winner(self):
        draw_text = WINNER_FONT.render(self.winner_text, True, WHITE)
        self.screen.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                            2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
    def loop(self,keys_pressed):
        # runs a single game loop to draw
        self.yellow.move(keys_pressed)
        self.red.move(keys_pressed)
        self.yellow.move_bullets()
        self.red.move_bullets()
        self.red_bullet_collision()
        self.red_award_collision()
        self.yellow_bullet_collision()
        self.yellow_award_collision()

    def rais_winner(self):
        if self.red.health <= 0:
            self.winner_text = "Yellow Wins!"

        if self.yellow.health <= 0:
            self.winner_text = "Red Wins!"

        if self.winner_text != "":
            self.draw_winner()
            return True
        else:
            return False

    def draw(self): 
        self.screen.blit(SPACE, (0, 0))
        pygame.draw.rect(self.screen, BLACK, BORDER)
        self.red.draw(self.screen)
        self.yellow.draw(self.screen)
        self.draw_health()

