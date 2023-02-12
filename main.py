import pickle
import pygame
import random
import neat
from award import *
from Game import *

WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

class AI:
    def __init__(self,screen,height,width):
        self.game = Game(screen)
        self.height = height
        self.width = width
        
    def test_AI(self):
        run = True
        clock = pygame.time.Clock()
        award_timer_event , t = pygame.USEREVENT+3, 15000
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
        
def eval_genomes(genomes, config):
    pass

def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
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
