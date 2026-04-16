import pygame

NEIGHBOUR_OFFSET = []
for i in range(-1, 2):
    for j in range(-1, 2):
        NEIGHBOUR_OFFSET.append((i, j))

PHYSICS_TILES = {'grass', 'stone'} #apparently a set, like a dictionary without values


# print(NEIGHBOUR_OFFSET) #check for all tiles near position

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size=tile_size
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap['10;' + str(7+i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 7+i)}
            self.tilemap['18;' + str(5+i)] = {'type': 'stone', 'variant': 1, 'pos': (18, 5+i)}

        for i in range(20):
            self.tilemap[str(i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (i, 10)} # dictionary of grass blocks
            self.tilemap['0;' + str(-5+i)] = {'type': 'stone', 'variant': 1, 'pos': (0, -5+i)} # dictionary of stone blocks
    
    def tiles_around(self, pos):
        tiles = []
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOUR_OFFSET:
            check_loc = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surface, offset = (0, 0)): #matches tilemap to assets and overrites them on the surface, so the screen
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size+1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size+1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(self.game.assets[tile['type']] [tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']] [tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
