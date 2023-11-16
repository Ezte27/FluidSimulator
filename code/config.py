import pygame

# Colors
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
LIGHT_BLUE = (5, 145, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (5, 255, 145)

# Window variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_CAPTION = "Fluid Simulation"

# Initializing Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_CAPTION)
clock = pygame.time.Clock()

# PANEL variables
G                   = pygame.math.Vector2((0, 9.8)) # m/s^2
SIMULATION_SPEED    = 9 # The speed of the simulation. 0 = stop, 1 = 1x, 2 = 2x, ...
FPS                 = 60 # Frames per second
dt                  = (1 * SIMULATION_SPEED) / FPS # Delta time
BOUNDS_SIZE         = pygame.math.Vector2((800, 600))
BOUNDS_POS          = pygame.math.Vector2(((SCREEN_WIDTH - BOUNDS_SIZE.x)/2, (SCREEN_HEIGHT - BOUNDS_SIZE.y)/2))
COLLISION_DAMPING   = 0.8 # Damping between 0 and 1
PARTICLE_RAD        = 10
PARTICLE_COLOR      = LIGHT_BLUE
NUM_PARTICLES       = 9
PARTICLE_SPACING    = 10

# Main loop variables
running = True # True if running simulation, False otherwise

# Other variables
particles = []