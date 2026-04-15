import pygame

class PhysicsEntity:
    def __init__(self,game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        self.velocity = [0, 0]

        self.grounded_grace = 0
        self.jump_grace = 0
        self.dash = False

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

        ################################################
        if self.velocity[0] * movement[0] < 0:
            self.velocity[0] += movement[0]*0.8
        elif self.velocity[0] < 1.5 and self.velocity[0] > -1.5:
            self.velocity[0] += movement[0]*0.5

        if self.velocity[0] * movement[0] <= 0 or self.grounded_grace > 0: #slows entity if on the ground not holding movement direction for player
            if self.velocity[0] > 0.2:
                self.velocity[0] -= 0.2
            if self.velocity[0] < -0.2:
                self.velocity[0] += 0.2
            if -0.2 <= self.velocity[0] <= 0.2:
                self.velocity[0] = 0
        
        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = 0
        
        self.velocity[1] = min(6, self.velocity[1]+0.2)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        if self.collisions['down']:
            self.grounded_grace = 7
        
        if self.jump_grace > 0 and self.grounded_grace > 0:
            self.velocity[1] = -5
            self.jump_grace = 0
            self.grounded_grace = 0
        else:
            self.jump_grace -= 1
            self.grounded_grace -= 1

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
        
        