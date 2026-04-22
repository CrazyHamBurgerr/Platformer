import sys
import pygame
import time
import datetime

from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.scoreboard import ScoreBoard

class Game:
    def __init__(self):
        print("started launching game")
        pygame.init()
        
        print("creating game window and variables")
        pygame.display.set_caption("square cubed")
        self.display = pygame.display.set_mode((640, 480)) 
        self.screen = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.movement_x = [False, False]
        self.movement_y = [False, False]

        print("loading assets")
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds')
        } #loads assets

        print("creating player")
        self.player = Player(self, (50, 50), (15, 15))

        print("creating clouds")
        self.clouds = Clouds(self.assets['clouds'], 16)
        
        self.tilemap = Tilemap(self, 16)
        self.load_level(0)

        self.score_board = ScoreBoard()
        #self.score_board.print()
        print("game launched")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 15)

    def load_level(self, map_id):
        self.player.pos = [160, 0]
        self.player.velocity = [0, 0]
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.scroll = [0, 0]
        self.player.dead = 0
        self.transition = 0
        self.starting_time = int(time.time())
        
    def run(self):
        while True:
            self.scroll[0] += (self.player.rect().centerx - self.screen.get_width()/2 - self.scroll[0])/8
            self.scroll[1] += (self.player.rect().centery - self.screen.get_height()/2 - self.scroll[1])/8
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.screen.blit(self.assets['background'])

            self.clouds.update()
            self.clouds.render(self.screen, render_scroll)

            self.tilemap.render(self.screen, render_scroll)

            if self.player.dead:
                self.player.dead += 1
                self.transition += 4
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, 320, self.transition))
                if self.player.dead > 70:
                    self.load_level(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.score_board.save()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_x[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_x[1] = True
                    if event.key == pygame.K_UP:
                        self.movement_y[0] = True
                    if event.key == pygame.K_DOWN:
                        self.player.velocity[1] +=0.3
                        self.player.maximum_fall_velocity = 9
                        self.movement_y[1] = True

                    if event.key == pygame.K_z:
                        self.player.jump_grace = 5
                    if event.key == pygame.K_r:
                        self.player.dead = 1

                    if event.key == pygame.K_x:
                        self.player.dash(self.movement_x[1] - self.movement_x[0], self.movement_y[1] - self.movement_y[0])

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_x[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_x[1] = False
                    if event.key == pygame.K_UP:
                        self.movement_y[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement_y[1] = False
                        self.player.maximum_fall_velocity = 6

                    if event.key == pygame.K_z and self.player.velocity[1] < -1 and self.player.can_dash:
                         self.player.velocity[1] = -1

            if not self.player.dead:
                current_time = int(time.time())

                if self.player.update(self.tilemap, self.score_board, (self.movement_x[1] - self.movement_x[0], 0)):
                    print(f"goal! score: {100 + self.starting_time - current_time}, time taken: {current_time - self.starting_time},",
                          f"date: {datetime.datetime.fromtimestamp(current_time)} ")
                    self.score_board.new_entry(100 + self.starting_time - current_time, current_time)
                    self.player.dead = 1
                self.player.render(self.screen, render_scroll)
            
                timer = self.font.render(str(100 + self.starting_time - current_time), False, 'purple')
                self.screen.blit(timer, (5, 5))
                if current_time - self.starting_time == 100:
                    self.load_level(0)

            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            
            pygame.display.update()
            
            self.clock.tick(60)


Game().run()