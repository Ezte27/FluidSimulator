import pygame

class Particle():
    def __init__(self, position, radius) -> None:
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2((0, 0))

        self.radius = radius