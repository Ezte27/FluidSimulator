import pygame, math
import numpy as np

# Variables

G = pygame.math.Vector2((0, 9.8)) # m/s^2

SIMULATION_SPEED = 9 # The speed of the simulation. 0 = stop, 1 = 1x, 2 = 2x, ...

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_CAPTION = "Fluid Simulation"
FPS = 60        # Frames per second
dt = (1 * SIMULATION_SPEED) / FPS    # Delta time
running = True # True if running simulation, False otherwise

BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
LIGHT_BLUE = (5, 145, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (5, 255, 145)

PARTICLE_RAD   = 10
PARTICLE_COLOR = LIGHT_BLUE

NUM_PARTICLES       = 9
PARTICLE_SPACING    = 10
particles = []

BOUNDS_SIZE = pygame.math.Vector2((800, 600))
BOUNDS_POS  = pygame.math.Vector2(((SCREEN_WIDTH - BOUNDS_SIZE.x)/2, (SCREEN_HEIGHT - BOUNDS_SIZE.y)/2))
collisionDamping = 0.8 # Damping between 0 and 1

# Initialize Pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_CAPTION)
clock = pygame.time.Clock()

#TODO: Im thinking of adding a panel to the current screen or add a new screen with a panel similar to what unity has in order to modify certain variables on the go.
# I think it should be a panel at the top right of the screen before the simulation starts and has a button to start and pause the simulation

class Particle():
    def __init__(self, position) -> None:
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2((0, 0))

def draw_particles(screen, color, particle, radius):
    for particle in particles:
        pygame.draw.circle(screen, color, particle.position, radius)

def apply_gravity(particle):
    particle.velocity.x += G.x * dt
    particle.velocity.y += G.y * dt

def update_position(particle):
    particle.position.x += particle.velocity.x * dt
    particle.position.y += particle.velocity.y * dt

def resolveCollision(particle):
    reducedBoundSize = pygame.math.Vector2((BOUNDS_SIZE.x - PARTICLE_RAD*2, BOUNDS_SIZE.y - PARTICLE_RAD*2))
    reducedBoundPos = pygame.math.Vector2((BOUNDS_POS.x + PARTICLE_RAD, BOUNDS_POS.y + PARTICLE_RAD)) # Bound size reduced to compensate for particle radius

    # Check left bound
    if (particle.position.x < reducedBoundPos.x):                    
        particle.position.x = reducedBoundPos.x
        particle.velocity.x *= -1 * collisionDamping
    # Check right bound
    elif (particle.position.x > reducedBoundPos.x + reducedBoundSize.x):
        particle.position.x = reducedBoundPos.x + reducedBoundSize.x
        particle.velocity.x *= -1 * collisionDamping

    # Check top bound
    if (particle.position.y < reducedBoundPos.y):                    
        particle.position.y = reducedBoundPos.y
        particle.velocity.y *= -1 * collisionDamping
    # Check bottom bound
    elif (particle.position.y > reducedBoundPos.y + reducedBoundSize.y):  
        particle.position.y = reducedBoundPos.y + reducedBoundSize.y
        particle.velocity.y *= -1 * collisionDamping

def draw_bounds():
    pygame.draw.rect(screen, GREEN, (BOUNDS_POS.x, BOUNDS_POS.y, BOUNDS_SIZE.x, BOUNDS_SIZE.y), 3)

# Place particles in a grid formation

particlesPerRow = int(math.sqrt(NUM_PARTICLES))
particlesPerCol = (NUM_PARTICLES) / particlesPerRow
spacing         = PARTICLE_RAD * 2 + PARTICLE_SPACING

for i in range(0, NUM_PARTICLES):
    x = ((i % particlesPerRow - particlesPerRow / 2 + 0.5) * spacing) + SCREEN_WIDTH/2
    y = ((i // particlesPerRow - particlesPerCol / 2 + 0.5) * spacing) + SCREEN_HEIGHT/2
    particles.append(Particle((x, y)))

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Panel HERE

    screen.fill(BLACK)

    # Start simulation code
    
    # Particle loop
    for particle in particles:
        apply_gravity(particle)
        update_position(particle)
        resolveCollision(particle)
        draw_particles(screen, PARTICLE_COLOR, particle, PARTICLE_RAD)
        draw_bounds()
    # End simulation code

    clock.tick(FPS)
    pygame.display.update()