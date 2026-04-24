import sys
import pygame
import time
import datetime

from scripts.clouds import Clouds
from scripts.entities import PhysicsEntity, Player
from scripts.eventhandler import game_event_handler
from scripts.scoreboard import ScoreBoard
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images

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
        self.iris_pos = (245, 185)
        
        print("loading level")
        self.tilemap = Tilemap(self, 16)
        self.load_level(0)

        self.score = 6000
        self.score_board = ScoreBoard()

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
        self.score = 6000

    def player_death(self):
        self.player.dead += 1
        self.transition += 4
        pygame.draw.rect(self.screen, (0 + self.player.dead, 0, 0 + self.player.dead), 
                         pygame.Rect(0, 0, 320, self.transition))
        self.screen.blit(self.assets['decor'][5], (152, 112))
        if self.player.dead > 80:
            self.load_level(0)
        
    def run(self):
        while True:
            self.scroll[0] += (self.player.rect().centerx - self.screen.get_width() / 2 - self.scroll[0]) / 12
            self.scroll[1] += (self.player.rect().centery - self.screen.get_height() / 2 - self.scroll[1]) / 12
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.screen.blit(self.assets['background'])
            pygame.draw.circle(self.screen, (255, 255, 255), 
                               (self.iris_pos[0] - (self.iris_pos[0] - self.player.pos[0] + render_scroll[0]) / 30, 
                                self.iris_pos[1] - (self.iris_pos[1] - self.player.pos[1] + render_scroll[1]) / 60), 15, 1)

            self.clouds.update()
            self.clouds.render(self.screen, render_scroll)

            self.tilemap.render(self.screen, render_scroll)

            if self.player.dead:
                self.player_death()

            for event in pygame.event.get():
                game_event_handler(self, event)

            if not self.player.dead:
                current_time = int(time.time())

                if self.player.update(self.tilemap, (self.movement_x[1] - self.movement_x[0], 0)):
                    print(f"goal! score: {self.score}", 
                          f"time taken: {current_time - self.starting_time},",
                          f"date: {datetime.datetime.fromtimestamp(current_time)}")
                    self.score_board.new_entry(self.score, current_time)
                    self.player.dead = 1
                self.player.render(self.screen, render_scroll)
            
                timer = self.font.render(str(100 + self.starting_time - current_time), False, 'purple')
                self.screen.blit(timer, (5, 5))
                if current_time - self.starting_time > 100:
                    self.load_level(0)

            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            self.score -= 1
            
            pygame.display.update()
            
            self.clock.tick(60)


Game().run()