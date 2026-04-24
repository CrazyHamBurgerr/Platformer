import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        self.velocity = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0,0), fall_velocity = 6):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.friction(movement)
        frame_movement = (round((movement[0] + self.velocity[0]), 2), round(movement[1] + self.velocity [1], 2))

        self.pos[1] += frame_movement[1]
        self.entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.pos):
            if self.entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self.entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    self.entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = self.entity_rect.y

        self.pos[0] += frame_movement[0]
        self.entity_rect = self.rect()
        
        for rect in tilemap.physics_rects_around(self.pos):
            if self.entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    self.entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = self.entity_rect.x

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = 0
        
        self.velocity[1] = min(fall_velocity, self.velocity[1] + 0.2)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def determine_friction(self, movement = (0, 0)):
        if abs(self.velocity[0]) > 20:
            return 0.5 * abs(self.velocity[0]) / 10
        if movement[0] == 0: 
            return 0.05

    def friction(self, movement = (0, 0)): #slows entity if on the ground not holding movement direction
        friction = self.determine_friction(movement)
        if friction == None:
            friction = 0
        if self.velocity[0] > friction:
            self.velocity[0] -= friction
        elif self.velocity[0] < -friction:
            self.velocity[0] += friction
        else:
            self.velocity[0] = 0
    
    def render(self, surface, offset = (0, 0)):
        colour = (150, 0, 150)
        pygame.draw.rect(surface, colour, pygame.Rect(self.pos[0] - offset[0], 
                                                      self.pos[1] - offset[1], 
                                                      self.size[0], self.size[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        
        self.air_time = 0
        self.friction_time = 0
        self.jump_grace = 0
        self.wall_jump_grace = 0
        self.right_wall= False # is the character on the right wall
        self.can_dash = False
        self.maximum_fall_velocity = 6
        self.dead = 0
    
    def update(self, tilemap, movement=(0,0)):
        self.force_restart_check(tilemap)

        self.velocity_change(movement)
        super().update(tilemap, movement, self.maximum_fall_velocity)
        
        self.wall_jump_check()
        self.jump(movement)

        self.air_time += 1
        if self.collisions['down']: # checks if player is grounded and resets air time (important for jump forgiveness) and the ability to dash
            self.air_time = 0
            self.can_dash = True

        return self.goal_check(tilemap)

    def determine_friction(self, movement = (0, 0)):
            if self.air_time < 4:
                self.friction_time = max(0, self.friction_time - 1)
            if round(abs(self.velocity[0]), 2) == 2.05:
                return 0.05
            if self.air_time < 4 and self.friction_time == 0:
                return 0.2
            return super().determine_friction(movement)

    def velocity_change(self, movement = (0, 0)):
        if self.velocity[0] * movement[0] < 0:
            self.velocity[0] += movement[0] * 0.8
        elif self.velocity[0] < 2.05 and self.velocity[0] > -2.05:
            if movement[0] == 1:
                self.velocity[0] = min(self.velocity[0] + movement[0] * 0.5, 2.05)
            elif movement[0] == -1:
                self.velocity[0] = max(self.velocity[0] + movement[0] * 0.5, -2.05)
            

    # movement abilities
    def jump(self, movement): # determines if player character should jump and if it's a normal or a wall jump
        if self.jump_grace > 0:
            self.jump_grace = max (0, self.jump_grace - 1)
            if self.air_time < 7:
                self.velocity[1] = -4.5
                self.jump_grace = 0
                self.air_time = 7
            elif self.wall_jump_grace > 0:
                self.wall_jump_grace = 0
                self.velocity[1] = -4.2
                if self.right_wall:
                    if movement[0] == 1:
                        self.velocity[0] = -4
                else:
                    if movement[0] == -1:
                        self.velocity[0] = 4
    
    def wall_jump_check(self): # checks if player can wall jump
        self.wall_jump_grace = max(0, self.wall_jump_grace - 1)
        if self.collisions['right'] or self.collisions['left']:
            self.wall_jump_grace = 7
            self.velocity[1] = min(1.5, self.velocity[1])
            if self.collisions['right']:
                self.right_wall= True
            else:
                self.right_wall= False

    def dash(self, move_x, move_y):
        if self.can_dash and (move_x != 0 or move_y != 0):
            if move_y * self.velocity[1] > 0 and abs(self.velocity[1]) > 2 and move_x == 0:
                self.velocity[1] += move_y * 3
            else:
                self.velocity[1] = move_y * 5
            self.velocity[0] += move_x * 3
            self.can_dash = False
            self.friction_time = 7

    # player rendering
    def render(self, surface, offset = (0, 0)):
        if abs(self.velocity[1]) > 0.61:
            scale_y = 1+abs(self.velocity[1])/40
        else:
            scale_y = 1

        scale_x = 1+abs(self.velocity[0])/15

        scale = scale_y / scale_x 
        offset_x = (self.size[0] - int(self.size[0]*scale)) / 2
        offset_y = self.size[1] - int(self.size[1]/scale)

        colour = (100, 200, 0)
        if self.can_dash == False:
            colour = (70, 140, 0)
        pygame.draw.rect(surface, colour, pygame.Rect(self.pos[0] + offset_x - offset[0], 
                                                      self.pos[1] + offset_y - offset[1], 
                                                      self.size[0] * scale, self.size[1] / scale))

    # collision check with special tiles
    def force_restart_check(self, tilemap):
        for rect in tilemap.deadly_rects_around(self.pos):
            if self.entity_rect.colliderect(rect):
                self.dead = 1
    
    def goal_check(self, tilemap):
        for rect in tilemap.goal_rects_around(self.pos):
            if self.entity_rect.colliderect(rect):
                return True
            else:
                return False
        else:
            return False