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

    def update(self, tilemap, movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        
        frame_movement = ((movement[0] + self.velocity[0])*1.1, movement[1] + self.velocity [1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = 0
        
        self.velocity[1] = min(6, self.velocity[1]+0.2)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        
        self.air_time = 0
        self.jump_grace = 0
        self.wall_jump_grace = 0
        self.right_wall= False # is the character on the right wall
        self.can_dash = False
    
    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement)

        if self.velocity[0] * movement[0] < 0:
            self.velocity[0] += movement[0]*0.2
        elif self.velocity[0] < 1.5 and self.velocity[0] > -1.5:
            self.velocity[0] += movement[0]*0.5

        if self.velocity[0] * movement[0] <= 0 or self.air_time < 4 or abs(self.velocity[0]) > 2: #slows entity if on the ground not holding movement direction for player
            friction = 0.2
            if self.velocity[0] > friction:
                self.velocity[0] -= friction
            elif self.velocity[0] < -friction:
                self.velocity[0] += friction
            else:
                self.velocity[0] = 0
        
        self.wall_jump_grace -=1
        self.wall_slide = False
        if self.collisions['right'] or self.collisions['left']:
            self.wall_jump_grace = 10
            self.velocity[1] = min(1.5, self.velocity[1])
            if self.collisions['right']:
                self.right_wall= True
            else:
                self.right_wall= False
       
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.can_dash = True
        
        if self.jump_grace > 0: #determines if player character should jump and if it's a normal or a wall jump
            self.jump_grace -= 1
            if self.air_time < 7:
                self.jump()
            elif self.wall_jump_grace > 0:
                self.wall_jump_grace = 0
                self.velocity[1] = -4.2
                if self.right_wall:
                    self.velocity[0] = -4
                else:
                    self.velocity[0] = 4

    def jump(self):
        self.velocity[1] = -5
        self.jump_grace = 0
        self.air_time = 7
    
    def dash(self):
        pass

    def render(self, surface, offset = (0, 0)):
        if abs(self.velocity[1]) > 0.61:
            scale_y = 1+abs(self.velocity[1])/40
        else:
            scale_y = 1

        scale_x = 1+abs(self.velocity[0])/15

        scale = scale_y / scale_x 
        offset_x = (self.size[0] - int(self.size[0]*scale)) / 2
        offset_y = self.size[1] - int(self.size[1]/scale)

        pygame.draw.rect(surface, (100, 200, 0), pygame.Rect(self.pos[0] + offset_x - offset[0], self.pos[1] + offset_y - offset[1], self.size[0] * scale, self.size[1] / scale))
        