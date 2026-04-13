NEIGHBOUR_OFFSET = []
for i in range(-1, 2, 2):
    for j in range(-1, 2):
        NEIGHBOUR_OFFSET.append((i, j))
NEIGHBOUR_OFFSET.append((0, 1))
NEIGHBOUR_OFFSET.append((0, -1))


print(NEIGHBOUR_OFFSET)

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size=tile_size
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3+i, 10)}
            self.tilemap['10;' + str(5+i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5+i)}
    
    def render(self, surface):
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']] [tile['variant']], [tile['pos']])
            
        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile['type']] [tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
    
    def tiles_around(self, pos):
        tiles = []
        tile_location = ((int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)))
        for offset in NEIGHBOUR_OFFSET:
            check_loc = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles