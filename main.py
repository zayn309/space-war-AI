import datetime as dt
import pickle
import pygame
import random
import neat
from award import *
from Game import *

FPS = 60

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class AI:
    def __init__(self,screen,height,width):
        self.game = Game(screen)
        self.height = height
        self.width = width
        
    def getLeftInput(self):
        left_x = self.game.yellow.rect.x
        left_y = self.game.yellow.rect.y
        right_x = self.game.red.rect.x
        right_y = self.game.red.rect.y
        award_x = -1
        award_y = -1
        if len(self.game.yellow.award)>0:
            award_x = self.game.yellow.award[0].rect.x
            award_y = self.game.yellow.award[0].rect.y
        bulllet_x = -1 
        bulllet_y = -1
        if len(self.game.red.bullets)>0:
            for bullet in self.game.red.bullets:
                if bullet.x > self.game.yellow.rect.x:
                    bulllet_x = bullet.x
                    bulllet_y = bullet.y
                    break
        return (left_x, left_y, right_x, right_y,award_x,award_y,bulllet_x,bulllet_y)
    
    def getRightInput(self):
        right_x = self.game.red.rect.x
        right_y = self.game.red.rect.y
        left_x = self.game.yellow.rect.x
        left_y = self.game.yellow.rect.y
        award_x = -1
        award_y = -1
        if len(self.game.red.award)>0:
            award_x = self.game.red.award[0].rect.x
            award_y = self.game.red.award[0].rect.y
        bulllet_x = -1 
        bulllet_y = -1
        if len(self.game.yellow.bullets)>0:
            for bullet in self.game.yellow.bullets:
                if bullet.x > self.game.red.rect.x:
                    bulllet_x = bullet.x
                    bulllet_y = bullet.y
                    break
        return ( right_x, right_y,left_x, left_y,award_x,award_y,bulllet_x,bulllet_y)
    
    def test_AI(self):
        run = True
        clock = pygame.time.Clock()
        award_timer_event , t = pygame.USEREVENT+3, int(20000 / FPS)
        pygame.time.set_timer(award_timer_event, t)
        
        while run:
            
            clock.tick(FPS)
            
            if pygame.event.get(pygame.QUIT): run = False
            for event in pygame.event.get():
                if event.type == award_timer_event:
                    if len(self.game.yellow.award) == 0:
                        temp = random.randint(0,2)
                        if temp == 0:
                            self.game.yellow.add_award(bullet_speed(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                        elif temp == 1:
                            self.game.yellow.add_award(bullet_increas(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                        else:
                            self.game.yellow.add_award(health_increase(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                            
                            
                    if len(self.game.red.award) == 0:
                        temp = random.randint(0,2)
                        if temp == 0:
                            self.game.red.add_award(bullet_speed(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                        elif temp == 1:
                            self.game.red.add_award(bullet_increas(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                        else:
                            self.game.red.add_award(health_increase(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                            
                            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        self.game.yellow.fire()
                    if event.key == pygame.K_RCTRL:
                        self.game.red.fire()
                        
            keys_pressed = pygame.key.get_pressed()
            self.game.loop(keys_pressed)
            self.game.draw()
            
            if self.game.rais_winner():
                break
            
            pygame.display.update()
            
        pygame.quit()
    
    def train_AI(self,genome1, genome2,config,draw = False):
        
        award_timer_event , t = pygame.USEREVENT+3, int(20000 / FPS)
        pygame.time.set_timer(award_timer_event, t)
        
        net1 = neat.nn.FeedForwardNetwork.create(genome1,config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2,config)
        clock = pygame.time.Clock()
        run = True
        start = dt.datetime.now()
        while run:
            #clock.tick(FPS)
            output1 = net1.activate(self.getLeftInput())
            decision1 = output1.index(max(output1))
            output2 = net2.activate(self.getRightInput())
            decision2 = output2.index(max(output2))
            
            if pygame.event.get(pygame.QUIT): quit()
            
            for event in pygame.event.get():
                if event.type == award_timer_event: # for the awards
                    if len(self.game.yellow.award) == 0:
                        temp = random.randint(0,2)
                        if temp == 0:
                            self.game.yellow.add_award(bullet_speed(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                        elif temp == 1:
                            self.game.yellow.add_award(bullet_increas(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                        else:
                            self.game.yellow.add_award(health_increase(random.randint(0,BORDER.x),random.randint(0,HEIGHT - 15)))
                            
                    if len(self.game.red.award) == 0:
                        temp = random.randint(0,2)
                        if temp == 0:
                            self.game.red.add_award(bullet_speed(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                        elif temp == 1:
                            self.game.red.add_award(bullet_increas(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                        else:
                            self.game.red.add_award(health_increase(random.randint(BORDER.x+BORDER.width,WIDTH-15),random.randint(0,HEIGHT - 15)))
                # fire 
                if decision1 == 0:
                    self.game.yellow.fire()
                if decision2 == 0:
                    self.game.red.fire()
            if decision1 == 5:
                genome1.fitness -= 0.01 # we want to discourage this 
                pass
            else:
                self.move_left_AI_ship(decision1)
                
            if decision2 == 5:
                genome2.fitness -= 0.01
                pass
            else:
                self.move_right_AI_ship(decision2)
            
            if self.game.yellow.health <= 0 or self.game.red.health <= 0:
                break
            end = dt.datetime.now()
            duration = (end - start).total_seconds()
            self.game.yellow.move_bullets()
            self.game.red.move_bullets()
            # for the bullets collision
            if self.game.red_bullet_collision():
                genome2.fitness -= 1
                genome1.fitness += 1
                duration -= 1 # there is a progress so make the round last longer
            if self.game.yellow_bullet_collision():
                genome2.fitness += 1
                genome1.fitness -= 1
                duration -= 1
            #for the awards collision
            if self.game.yellow_award_collision():
                genome1.fitness += 1
                duration -= 1
            if self.game.red_award_collision():
                genome2.fitness += 1
                duration -= 1
            
            if draw:
                self.game.draw()
                self.draw_round_timer(duration)
                
            if duration >= 3 : # we don't wan't the round to take more than 1 and a half min to speed up the training
                break
            
    def draw_round_timer(self,time):
        text_col = WHITE if time < 20 else RED
        time_text = HEALTH_FONT.render(
            str(int(time)), True, text_col)
        screen.blit(time_text, ( (WIDTH/2) - time_text.get_width()/2, 10))
    def move_left_AI_ship(self,dec):
        if dec == 1  and self.game.yellow.rect.x - self.game.yellow.vel > 0:  # LEFT
            self.game.yellow.move_left()
        if dec == 2 and self.game.yellow.rect.x + self.game.yellow.vel + self.game.yellow.rect.width < BORDER.x:  # RIGHT
            self.game.yellow.move_right()
        if dec == 3 and self.game.yellow.rect.y - self.game.yellow.vel > 0:  # UP
            self.game.yellow.move_up()
        if dec == 4 and self.game.yellow.rect.y + self.game.yellow.vel + self.game.yellow.rect.height <HEIGHT:  # DOWN
            self.game.yellow.move_down()
    def move_right_AI_ship(self,dec):
        if dec == 1  and self.game.red.rect.x - self.game.red.vel > BORDER.x + BORDER.width:  # LEFT
            self.game.red.move_left()
        if dec == 2 and self.game.red.rect.x + self.game.red.vel + self.game.red.rect.width < WIDTH:  # RIGHT
            self.game.red.move_right()
        if dec == 3 and self.game.red.rect.y - self.game.red.vel > 0:  # UP
            self.game.red.move_up()
        if dec == 4 and self.game.red.rect.y + self.game.red.vel + self.game.red.rect.height < HEIGHT:  # DOWN
            self.game.red.move_down()
        
def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    
    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            ai = AI(screen, WIDTH, HEIGHT)
            ai.train_AI(genome1, genome2, config)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)
    #save python object
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config= neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    run_neat(config)


