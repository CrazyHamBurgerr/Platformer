import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        print("started launching game")
        pygame.init()
        
        print("creating window and variables")
        pygame.display.set_caption("square cubed - level editor")
    
        self.screen = pygame.Surface((320, 240))
        self.display = pygame.display.set_mode((self.screen.get_width() * RENDER_SCALE, self.screen.get_height() * RENDER_SCALE)) 
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
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

        print("editor launched")
        
    def run(self):
        while True:
            self.screen.fill((18, 18, 18))

            self.scroll[0] += (self.movement_x[1] - self.movement_x[0]) * (3 + self.shift * 5)
            self.scroll[1] += (self.movement_y[1] - self.movement_y[0]) * (3 + self.shift * 5)
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.screen.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - render_scroll[0], tile_pos[1] * self.tilemap.tile_size - render_scroll[1]))
            else:
                self.screen.blit(current_tile_img, mouse_pos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = True
                    if event.key == pygame.K_d:
                        self.movement_x[1] = True
                    if event.key == pygame.K_w:
                        self.movement_y[0] = True
                    if event.key == pygame.K_s:
                        self.movement_y[1] = True

                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement_x[0] = False
                    if event.key == pygame.K_d:
                        self.movement_x[1] = False
                    if event.key == pygame.K_w:
                        self.movement_y[0] = False
                    if event.key == pygame.K_s:
                        self.movement_y[1] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            
            self.tilemap.render(self.screen, render_scroll)
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            pygame.display.update()
            
            self.clock.tick(60)


Editor().run()