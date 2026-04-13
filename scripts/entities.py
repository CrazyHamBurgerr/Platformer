import pygame

class PhysicsEntity:
    def __init__(self,game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        self.velocity = [0, 2]

    def update(self, movement=(0,0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity [1])
        
        self.velocity[1] = min(1, self.velocity[1]+0.1)
        
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surface):
        pygame.draw.rect(surface, (100, 200, 0), pygame.Rect(*self.pos, *self.size))