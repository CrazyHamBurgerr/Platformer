import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        print("started launching game")
        pygame.init()
        
        print("creating game window and variables")
        pygame.display.set_caption("square cubed")
        self.display = pygame.display.set_mode((640, 480)) 
        self.screen = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.scroll = [0, 0]

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
        self.player = PhysicsEntity(self, 'player', (50, 50), (15, 15))

        print("creating clouds")
        self.clouds = Clouds(self.assets['clouds'], 16)
        
        self.tilemap = Tilemap(self, 16)
        print("game launched")
        
    def run(self):
        while True:

            self.scroll[0] += (self.player.rect().centerx - self.screen.get_width()/2 - self.scroll[0])/15
            self.scroll[1] += (self.player.rect().centery - self.screen.get_height()/2 - self.scroll[1])/15
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.screen.blit(self.assets['background'])

            self.clouds.update()
            self.clouds.render(self.screen, render_scroll)

            self.tilemap.render(self.screen, render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if (event.key == pygame.K_z or event.key == pygame.K_UP):
                        self.player.jump_grace = 5
                        self.player.velocity[1] = -5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if (event.key == pygame.K_z or event.key == pygame.K_UP)  and self.player.velocity[1] < -1:
                         self.player.velocity[1] = -1

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.screen, render_scroll)
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            
            pygame.display.update()
            
            self.clock.tick(60)


Game().run()