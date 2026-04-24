import pygame
import sys

def game_event_handler(game, event):
    if event.type == pygame.QUIT:
                game.score_board.save()
                pygame.quit()
                sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            game.movement_x[0] = True
        if event.key == pygame.K_RIGHT:
            game.movement_x[1] = True
        if event.key == pygame.K_UP:
            game.movement_y[0] = True
        if event.key == pygame.K_DOWN:
            game.player.velocity[1] += 0.3
            game.player.maximum_fall_velocity = 9
            game.movement_y[1] = True
        if event.key == pygame.K_z:
            game.player.jump_grace = 5
        if event.key == pygame.K_r:
            game.player.dead = 1
        if event.key == pygame.K_p:
            game.score_board.sort()
            game.score_board.print()
        if event.key == pygame.K_x:
            game.player.dash(game.movement_x[1] - game.movement_x[0], 
                             game.movement_y[1] - game.movement_y[0])
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            game.movement_x[0] = False
        if event.key == pygame.K_RIGHT:
            game.movement_x[1] = False
        if event.key == pygame.K_UP:
            game.movement_y[0] = False
        if event.key == pygame.K_DOWN:
            game.movement_y[1] = False
            game.player.maximum_fall_velocity = 6
        if event.key == pygame.K_z and game.player.velocity[1] < -1 and game.player.can_dash:
             game.player.velocity[1] = -1

def editor_event_handler(editor, event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            editor.clicking = True
            editor.place_once = True
        if event.button == 3:
            editor.right_clicking = True
        if editor.shift:
            if event.button == 4:
                editor.tile_variant = (editor.tile_variant - 1) % len(editor.assets[editor.tile_list[editor.tile_group]])
            if event.button == 5:
                editor.tile_variant = (editor.tile_variant + 1) % len(editor.assets[editor.tile_list[editor.tile_group]])
        else:
            if event.button == 4:
                editor.tile_group = (editor.tile_group - 1) % len(editor.tile_list)
                editor.tile_variant = 0
            if event.button == 5:
                editor.tile_group = (editor.tile_group + 1) % len(editor.tile_list)
                editor.tile_variant = 0

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            editor.clicking = False
        if event.button == 3:
            editor.right_clicking = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            editor.movement_x[0] = True
        if event.key == pygame.K_d:
            editor.movement_x[1] = True
        if event.key == pygame.K_w:
            editor.movement_y[0] = True
        if event.key == pygame.K_s:
            editor.movement_y[1] = True

        if event.key == pygame.K_g:
            editor.ongrid = not editor.ongrid
        if event.key == pygame.K_LSHIFT:
            editor.shift = True
        if event.key == pygame.K_o:
            editor.save_level(0)
        if event.key == pygame.K_t:
            editor.tilemap.autotile()

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            editor.movement_x[0] = False
        if event.key == pygame.K_d:
            editor.movement_x[1] = False
        if event.key == pygame.K_w:
            editor.movement_y[0] = False
        if event.key == pygame.K_s:
            editor.movement_y[1] = False
        if event.key == pygame.K_LSHIFT:
            editor.shift = False

def editor_placement_handler(editor, tile_pos = (0,0), mouse_pos = (0,0)):
    if editor.clicking and editor.ongrid:
        editor.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
            'type': editor.tile_list[editor.tile_group], 'variant': editor.tile_variant, 'pos': tile_pos}
    elif editor.clicking and editor.place_once and not editor.ongrid:
        editor.tilemap.offgrid_tiles.append({'type': editor.tile_list[editor.tile_group], 
            'variant': editor.tile_variant, 
            'pos': (mouse_pos[0] + editor.scroll[0], mouse_pos[1] + editor.scroll[1])})
        editor.place_once = False
    
    if editor.right_clicking:
        tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
        if tile_loc in editor.tilemap.tilemap:
            del editor.tilemap.tilemap[tile_loc]
        for tile in editor.tilemap.offgrid_tiles.copy():
            tile_img = editor.assets[tile['type']][tile['variant']]
            tile_r = pygame.Rect(tile['pos'][0] - editor.scroll[0], tile['pos'][1] 
                - editor.scroll[1], tile_img.get_width(), tile_img.get_height())
            if tile_r.collidepoint(mouse_pos):
                editor.tilemap.offgrid_tiles.remove(tile)