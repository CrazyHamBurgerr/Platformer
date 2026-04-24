import sys
import pygame

from scripts.eventhandler import editor_event_handler, editor_placement_handler
from scripts.tilemap import Tilemap
from scripts.utils import load_images

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        print("started launching editor")
        pygame.init()
        
        print("creating window and variables")
        pygame.display.set_caption("square cubed - level editor")
    
        self.screen = pygame.Surface((320, 240))
        self.display = pygame.display.set_mode((self.screen.get_width() * RENDER_SCALE, 
                                                self.screen.get_height() * RENDER_SCALE)) 
        self.clock = pygame.time.Clock()

        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.scroll = [0, 0]

        print("loading assets")
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
        } #loads assets
        
        self.tilemap = Tilemap(self, 16)
        self.load_level(0)

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.place_once = False
        self.shift = False
        self.ongrid = True

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 15)

        print("editor launched")
    
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

    def save_level(self, map_id):
        self.tilemap.save('data/maps/' + str(map_id) + '.json')

    def tile_preview(self, tile_pos, mouse_pos, render_scroll):
        current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        current_tile_img.set_alpha(100)
        self.screen.blit(current_tile_img, (5, 5))

        if self.ongrid:
                self.screen.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - render_scroll[0], 
                                                    tile_pos[1] * self.tilemap.tile_size - render_scroll[1]))
        else:
            self.screen.blit(current_tile_img, mouse_pos)

    def run(self):
        while True:
            self.screen.fill((18, 18, 18))

            self.scroll[0] += (self.movement_x[1] - self.movement_x[0]) * (3 + self.shift * 5)
            self.scroll[1] += (self.movement_y[1] - self.movement_y[0]) * (3 + self.shift * 5)
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), 
                        int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))

            self.tilemap.render(self.screen, render_scroll)
            self.tile_preview(tile_pos, mouse_pos, render_scroll)


            tile_pos_render = self.font.render(str(tile_pos[0]) + ";" + str(tile_pos[1]), False, 'purple')
            self.screen.blit(tile_pos_render, (5, 215))

            editor_placement_handler(self, tile_pos, mouse_pos)

            for event in pygame.event.get():
                editor_event_handler(self, event)
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            pygame.display.update()
            
            self.clock.tick(60)


Editor().run()