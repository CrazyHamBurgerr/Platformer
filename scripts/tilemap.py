import pygame
import json

NEIGHBOR_OFFSET = []
for i in range(-1, 2):
    for j in range(-1, 2):
        NEIGHBOR_OFFSET.append((i, j))

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0, # top left tile
    tuple(sorted([(1, 0), (-1, 0), (0, 1)])): 1, # top tile
    tuple(sorted([(-1, 0), (0, 1)])): 2, # top right tile
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3, # middle right tile
    tuple(sorted([(-1, 0), (0, -1)])): 4, # bottom right tile
    tuple(sorted([(1, 0), (-1, 0), (0, -1)])): 5, # bottom tile
    tuple(sorted([(1, 0), (0, -1)])): 6, # bottom left tile
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7, # middle left tile
    tuple(sorted([(1, 0), (-1, 0), (0, -1), (0, 1)])): 8  # middle tile
}

PHYSICS_TILES = {'grass', 'stone'} #apparently a set, like a dictionary without values
AUTOTILE_TYPES = {'grass', 'stone'}

# print(NEIGHBOR_OFFSET) #check for all tiles near position

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size=tile_size
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []
    
    def tiles_around(self, pos):
        tiles = []
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def deadly_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] == 'decor' and tile['variant'] == 4:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, 
                                         tile['pos'][1] * self.tile_size, 
                                         self.tile_size, self.tile_size))
        return rects

    def goal_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] == 'decor' and tile['variant'] == 5:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, 
                                         tile['pos'][1] * self.tile_size, 
                                         self.tile_size, self.tile_size))
        return rects

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, 
                                         tile['pos'][1] * self.tile_size, 
                                         self.tile_size, self.tile_size))
        return rects

    def render(self, surface, offset = (0, 0)): #matches tilemap to assets and overrites them on the surface, so the screen
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']] [tile['variant']], 
                         (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size+1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size+1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(self.game.assets[tile['type']] [tile['variant']], 
                                (tile['pos'][0] * self.tile_size - offset[0], 
                                 tile['pos'][1] * self.tile_size - offset[1]))

    def save(self, path):
        file = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, file)
        file.close()

    def load(self, path):
        try:
            file = open(path, 'r')
            map_data = json.load(file)
            file.close()

            self.tilemap = map_data['tilemap']
            self.tile_size = map_data['tile_size']
            self.offgrid_tiles = map_data['offgrid']
        except FileNotFoundError:
            pass

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neightbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ";" + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neightbors.add(shift)
            neightbors = tuple(sorted(neightbors))
            if tile['type'] in AUTOTILE_TYPES and neightbors in AUTOTILE_MAP:
                tile['variant'] = AUTOTILE_MAP[neightbors]