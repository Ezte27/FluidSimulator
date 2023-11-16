import pygame, math
import numpy as np
from particle import Particle
from utilities import apply_gravity, update_position, resolveCollision, draw_bounds, draw_particles
from config import *

#TODO: Im thinking of adding a panel to the current screen or add a new screen with a panel similar to what unity has in order to modify certain variables on the go.
# I think it should be a panel at the top right of the screen before the simulation starts and has a button to start and pause the simulation

# Place particles in a grid formation

particlesPerRow = int(math.sqrt(NUM_PARTICLES))
particlesPerCol = (NUM_PARTICLES) / particlesPerRow
spacing         = PARTICLE_RAD * 2 + PARTICLE_SPACING

for i in range(0, NUM_PARTICLES):
    x = ((i % particlesPerRow - particlesPerRow / 2 + 0.5) * spacing) + SCREEN_WIDTH/2
    y = ((i // particlesPerRow - particlesPerCol / 2 + 0.5) * spacing) + SCREEN_HEIGHT/2
    particles.append(Particle((x, y), PARTICLE_RAD))

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
        apply_gravity(particle, G, dt)
        update_position(particle, dt)
        resolveCollision(particle, BOUNDS_POS, BOUNDS_SIZE, COLLISION_DAMPING)
        draw_particles(screen, PARTICLE_COLOR, particle)
        draw_bounds(screen, GREEN, BOUNDS_POS, BOUNDS_SIZE, 3)
    # End simulation code

    clock.tick(FPS)
    pygame.display.update()