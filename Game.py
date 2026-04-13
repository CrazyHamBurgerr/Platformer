import sys
import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption("square cubed")
        self.display = pygame.display.set_mode((640, 480)) 
        self.screen = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone')
        } #loads assets

        
        self.player = PhysicsEntity(self, 'player', (50, 50), (15, 15))
        
        self.tilemap = Tilemap(self, 16)
        
    def run(self):
        while True:
            self.screen.fill("purple")
            self.tilemap.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.screen)
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            
            pygame.display.update()
            
            self.clock.tick(60)


Game().run()