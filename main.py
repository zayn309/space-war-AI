import pygame
import random

from award import *
from Game import *


WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

run = True
clock = pygame.time.Clock()

award_timer_event , t = pygame.USEREVENT+3, 15000
pygame.time.set_timer(award_timer_event, t)

game = Game(screen)
while run:

    clock.tick(FPS)

    if pygame.event.get(pygame.QUIT): run = False
    for event in pygame.event.get():
        if event.type == award_timer_event:
            if len(game.yellow.award) == 0:
                temp = random.randint(0,2)
                if temp == 0:
                    game.yellow.add_award(bullet_speed(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                elif temp == 1:
                    game.yellow.add_award(bullet_increas(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                else:
                    game.yellow.add_award(health_increase(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))

            if len(game.red.award) == 0:
                temp = random.randint(0,2)
                if temp == 0:
                    game.red.add_award(bullet_speed(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                elif temp == 1:
                    game.red.add_award(bullet_increas(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                else:
                    game.red.add_award(health_increase(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                game.yellow.fire()
            if event.key == pygame.K_RCTRL:
                game.red.fire()
    
    keys_pressed = pygame.key.get_pressed()
    game.loop(keys_pressed)
    game.draw()
    if game.rais_winner():
        break
    pygame.display.update()

pygame.quit()


    
