import pygame, math, random
import numpy as np
from particle import Particle
from utilities import   (apply_gravity, update_position, resolveCollision, draw_bounds, draw_particles, drawSmoothingRadius, 
                         calculateDensity, updateSpatialLookup, calculatePressureForceForEachPointWithinRadius, getCellKeys, 
                         drawGrid, sleep_code, debugFromParticle, debugPressureForce, highlightSampleParticle, 
                         highlightParticlesInCell, debugSampleParticleAndCell, _get_max_col, _get_max_row,)
from settings import *

# Smoothing particle hydrodynamics

PARTICLE_GENERATION_MODES = ['grid', 'random']

#TODO: Im thinking of adding a panel to the current screen or add a new screen with a panel similar to what unity has in order to modify certain variables on the go.
# I think it should be a panel at the top right of the screen before the simulation starts and has a button to start and pause the simulation

def createParticlesRandomly(num_particles, particle_rad, particles):

    # Creating particles in random positions
    for _ in range(0, num_particles):

        # Calculating position for each particle
        x = random.random() * SCREEN_WIDTH * 1
        y = random.random() * SCREEN_HEIGHT * 1

        particles.append(Particle((x, y), particle_rad))

    
    return particles 

def createParticlesInGrid(num_particles, particle_rad, particle_spacing, particles):
    # Place particles in a grid formation
    particlesPerRow = int(math.sqrt(num_particles))
    particlesPerCol = (num_particles) / particlesPerRow
    spacing         = particle_rad * 2 + particle_spacing

    # Creating particles in an grid formation
    for i in range(0, num_particles):

        # Calculating position for each particle
        x = ((i % particlesPerRow - particlesPerRow / 2 + 0.5) * spacing) + SCREEN_WIDTH / 2
        y = ((i // particlesPerRow - particlesPerCol / 2 + 0.5) * spacing) + SCREEN_HEIGHT / 2
        
        particles.append(Particle((x, y), particle_rad))
    
    return particles

def initializeSimulation(num_particles, particle_rad, particle_spacing, smoothing_rad, mass, particle_generation_mode):
    particles = []

    cell_keys = getCellKeys(SCREEN_WIDTH, SCREEN_HEIGHT, smoothing_rad)
    num_cols = _get_max_col(cell_keys)
    num_rows = _get_max_row(cell_keys)

    # Filling up the spatialLookup list with padding
    spatial_lookup = [] 
    for _ in range(0, len(cell_keys)):
        spatial_lookup.append([])

    if particle_generation_mode == 'grid':
        particles  = createParticlesInGrid(num_particles, particle_rad, particle_spacing, particles)
    
    elif particle_generation_mode == 'random':
        particles = createParticlesRandomly(num_particles, particle_rad, particles)
    
    else:
        print(f"The particle generation mode provided is not supported by this simulator. Supported modes are {PARTICLE_GENERATION_MODES}") # ("¯\_(ツ)_/¯")

    # Calculate the density in each particle after they are created
    for particle in particles:
        particle.density = calculateDensity(particle.position, particles, mass, smoothing_rad)

    # Simulation variables

    return particles, spatial_lookup, cell_keys, num_cols, num_rows

# Initialize simulation
particles, spatial_lookup, cell_keys, num_cols, num_rows = initializeSimulation(NUM_PARTICLES, PARTICLE_RAD, PARTICLE_SPACING, SMOOTHING_RAD, MASS, 'grid')

dt = 0.01

# Main loop variables
running = True # True = main loop is running, False = main loop is not running
simulation_paused = True # True = simulation loop is not running, False = the other possibility
move_frame = False # If True, move one frame into the simulation

# Variables to calculate iteration time (used to measure the performance or efficiency of the loop)
start_time = 0 # Start of iteration
num_iter = 0 # Number of iterations since start of simulation
mean_time  = 0 # Average computing time per frame

# Main loop
while running:
    # Get computing time for each iteration or step
    start_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Pressed Keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start / Pause
                simulation_paused = not simulation_paused
            
            if event.key == pygame.K_PERIOD:
                # Move frame by frame
                if simulation_paused:
                    move_frame = True
            
            if event.key == pygame.K_r:
                # Reset simulation
                particles, spatial_lookup, cell_keys, num_cols, num_rows = initializeSimulation(NUM_PARTICLES, PARTICLE_RAD, PARTICLE_SPACING, SMOOTHING_RAD, MASS, 'random')

                start_time = -1
                num_iter = 0
                mean_time = 0

    screen.fill(BLACK)

    t1 = pygame.time.get_ticks()

    if not simulation_paused or move_frame:
        move_frame = False

        # Start simulation code

        # Particle loop
        for particle in particles:

            # Apply gravity and predict next positions
            apply_gravity(particle, G, dt)
            particle.predictedPosition.x = particle.position.x + particle.velocity.x * dt
            particle.predictedPosition.y = particle.position.y + particle.velocity.y * dt

            # update spatial lookup
            updateSpatialLookup(spatial_lookup, particle, cell_keys, SMOOTHING_RAD)

            # Calculate density
            particle.density = calculateDensity(particle, MASS, SMOOTHING_RAD, spatial_lookup, cell_keys, num_cols, num_rows) #calculateDensity(particle.predictedPosition, particles, MASS, SMOOTHING_RAD)
            if 0 >= particle.density:
                particle.density = 0.0001

            # Calculate and apply pressure force
            pressureForce = calculatePressureForceForEachPointWithinRadius(particle, SMOOTHING_RAD, spatial_lookup, MASS, TARGET_DENSITY, PRESSURE_MULTIPLIER, cell_keys, num_cols, num_rows)
            pressureAcceleration = pressureForce / particle.density
            
            particle.velocity.x += pressureAcceleration.x * dt
            particle.velocity.y += pressureAcceleration.y * dt

            # Update positions and resolve collisions
            update_position(particle, dt)
            resolveCollision(particle, BOUNDS_POS, BOUNDS_SIZE, COLLISION_DAMPING)   

        # End simulation code

    t2 = pygame.time.get_ticks()
    dt = (t2 - t1) / 1000

    # Rendering
    draw_bounds(screen, GREEN, BOUNDS_POS, BOUNDS_SIZE, 3)
    drawGrid(screen, LIGHT_GREEN, cell_keys, SMOOTHING_RAD, 1)

    for particle in particles:
        draw_particles(screen, PARTICLE_COLOR, particle)

    pygame.display.update()

    # Calculate iteration time
    if not(simulation_paused) and start_time >= 0:
        iter_time = pygame.time.get_ticks() - start_time
        num_iter += 1
        mean_time = ((mean_time * (num_iter - 1)) + (iter_time)) / num_iter

print(f"Simulation finished!")
print(f"Average iteration time: {round(mean_time, 2)} ms")
print(f"Average frames per second: {round(((1000 - mean_time) / mean_time), 1)} fps")