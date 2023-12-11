import pygame, math, random, time
from cmd_colors import CmdColors

# Constants
CELL_OFFSETS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

def apply_gravity(particle, g, dt):
    particle.velocity.x += g.x * dt
    particle.velocity.y += g.y * dt

def update_position(particle, dt):
    particle.position.x += particle.velocity.x * dt
    particle.position.y += particle.velocity.y * dt

def resolveCollision(particle, bound_pos, bounds_size, collisionDamping):
    reducedBoundSize = pygame.math.Vector2((bounds_size.x - particle.radius*2, bounds_size.y - particle.radius*2))
    reducedBoundPos = pygame.math.Vector2((bound_pos.x + particle.radius, bound_pos.y + particle.radius)) # Bound size reduced to compensate for particle radius

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

def smoothingKernel(radius, distance):
    if (distance >= radius):
        return 0
    
    volume = (math.pi * radius**4) / 6
    return (radius - distance) * (radius - distance) / volume

def smoothingKernelDerivative(dst, radius):
    if (dst >= radius):
        return 0
    
    scale = 12 / (radius**4 * math.pi)
    return (dst - radius) * scale

# def calculateDensity(samplePoint, particles, mass, smoothingRadius):
#     density = 0

#     for particle in particles:
#         dst = _get_dst(particle.position, samplePoint)
#         influence = smoothingKernel(smoothingRadius, dst)
#         density += mass * influence
#     return density

def calculateDensity(sample_particle, mass, smoothing_radius, spatial_lookup, cell_keys, num_cols, num_rows):
    density = 0

    # Get list of particles in 3 x 3 grid near the sample_particle
    neighboors = getNeighboors(sample_particle, spatial_lookup, cell_keys, num_cols, num_rows, smoothing_radius)

    # Loop over all particles in neighboors list
    for particle in neighboors:
        dst = _get_dst(particle.position, sample_particle.predictedPosition) # Using predicted position for better collision handling
        influence = smoothingKernel(smoothing_radius, dst)
        density += mass * influence
    return density

def convertDensityToPressure(density, targetDensity, pressureMultiplier):
    densityError = density - targetDensity
    pressure = densityError * pressureMultiplier
    return pressure

def calculateSharedPressure(densityA, densityB, targetDensity, pressureMultiplier):
    pressureA = convertDensityToPressure(densityA, targetDensity, pressureMultiplier)
    pressureB = convertDensityToPressure(densityB, targetDensity, pressureMultiplier)
    return (pressureA + pressureB) / 2

# # Space partitioning
# def updateSpatialLookup(spatial_lookup, particles, cell_keys, smoothing_radius):
#     for particle in particles:
#         cell_coord = posToCellCoord(particle.position, smoothing_radius)
#         cell_key = cell_keys.get(cell_coord)
#         spatial_lookup[cell_key].append(particle)
#     return spatial_lookup

# Space partitioning
def updateSpatialLookup(spatial_lookup, particle, cell_keys, smoothing_radius):
    cell_coord = posToCellCoord(particle.position, smoothing_radius)
    cell_key = cell_keys.get(cell_coord)
    spatial_lookup[cell_key].append(particle)
    return spatial_lookup

def calculatePressureForceForEachPointWithinRadius(sample_particle, smoothing_radius, spatial_lookup, mass, targetDensity, pressureMultiplier, cell_keys, num_cols, num_rows):

    # Define pressure force
    pressureForce = pygame.math.Vector2((0, 0))

    # Get list of particles in 3 x 3 grid near the sample_particle
    neighboors = getNeighboors(sample_particle, spatial_lookup, cell_keys, num_cols, num_rows, smoothing_radius)

    # Loop over all particles in the neighboors list
    for particle in neighboors:
      
        if sample_particle == particle:
            continue

        dst = _get_dst(particle.position, sample_particle.predictedPosition)

        try:
            direction = pygame.math.Vector2(((particle.predictedPosition.x - sample_particle.predictedPosition.x) / dst, (particle.predictedPosition.y - sample_particle.predictedPosition.y) / dst))
        except: # If dst == 0, get random direction
            direction = pygame.math.Vector2((_get_random_dir()))

        slope = smoothingKernelDerivative(dst, smoothing_radius)
        density = particle.density
        sharedPressure = calculateSharedPressure(density, sample_particle.density, targetDensity, pressureMultiplier)
        pressureForce += -sharedPressure * direction * slope * mass / density
    return pressureForce

# Helper functions for Spatial Lookup

# Return particles in the 3 x 3 grid around the sample particle
def getNeighboors(sample_particle, spatial_lookup:list, cell_keys:dict, num_cols, num_rows, smoothing_radius) -> list:

    neighboors = []
    cell_coord = posToCellCoord(sample_particle.position, smoothing_radius) # The coordinates for the cell that the sample particle is on
    cell_offsets = set(CELL_OFFSETS)  # Create a set of CELL_OFFSETS
    invalid_offsets = set()

    # Check cols
    if (0 >= cell_coord[0]):
        invalid_offsets.update([(-1, -1), (-1, 0), (-1, 1)])
    elif (cell_coord[0] >= num_cols):
        invalid_offsets.update([(1, -1), (1, 0), (1, 1)])

    # Check rows
    if (0 >= cell_coord[1]):
        invalid_offsets.update([(-1, -1), (0, -1), (1, -1)])
    elif (cell_coord[1] >= num_rows):
        invalid_offsets.update([(-1, 1), (0, 1), (1, 1)])

    cell_offsets -= invalid_offsets  # Use set difference to filter out invalid_offsets

    # Iterate over all offsets and append particles to the neighboors list
    for offsetX, offsetY in cell_offsets:
        neighboor_cell_coord = (cell_coord[0] + offsetX,  cell_coord[1] + offsetY)
        cell_key = cell_keys.get(neighboor_cell_coord) # The key of the neighboor cell
        for particle in spatial_lookup[cell_key]:
            neighboors.append(particle)
    
    return neighboors

# Get the cell in which the sample point is on 
def posToCellCoord(samplePoint, smoothingRad):
    cellX = samplePoint[0] // smoothingRad
    cellY = samplePoint[1] // smoothingRad

    return (cellX, cellY)

# End of Helper Functions

# Debug problems with the particles by using a particle as a reference
def debugFromParticle(particle, particles, id, screen, color, smoothingRadius):
    if particle == particles[id]:
        print(f"----- Particle -----")
        print(f"Position: {particle.position}")
        print(f"Velocity: {particle.velocity}")
        print(f"Density: {particle.density}")
        print(f"Predicted position: {particle.predictedPosition}")
        drawSmoothingRadius(screen, color, particle, smoothingRadius)
        pygame.draw.circle(screen, (255, 10, 10), particle.position, particle.radius*1.8)

# Debug pressure force related problems by printing the force that a sample particle is experiencing
def debugPressureForce(sampleParticleId, particle, particles, force):
    '''
    sampleParticleId: is the id for the specific particle that the pressure force it experiences is being observed
    particle: is the current particle in the main particle loop (found in main.py)
    force: the pressure force calculated in the main particle loop
    '''
    if particle == particles[sampleParticleId]:
        print(f"----- Particle {sampleParticleId} -----")
        print(f"Experienced pressure force: {force}")

# This function takes a particle and highlights the cell it is on
def debugSampleParticleAndCell(sampleParticleIdx, particles, smoothingRadius, screen):
    sampleParticle = particles[sampleParticleIdx]
    cellCoord = posToCellCoord(sampleParticle.position, smoothingRadius)

    # Highlight cell
    pygame.draw.rect(screen, (10, 20, 250), ((cellCoord[0] * smoothingRadius, cellCoord[1] * smoothingRadius), (smoothingRadius, smoothingRadius)), 3)

    # Highlight sample particle
    pygame.draw.circle(screen, (255, 50, 50), sampleParticle.position, sampleParticle.radius*1.8)

# Highlight sample particle
def highlightSampleParticle(sampleParticleId, particle, particles, screen, smoothingRadius):
    if particle == particles[sampleParticleId]:
        drawSmoothingRadius(screen, (20, 250, 50), particle, smoothingRadius)
        pygame.draw.circle(screen, (255, 50, 50), particle.position, particle.radius*1.8)

def highlightParticlesInCell(sampleCell:tuple | list, particles, cellKeys, startIndices, spatialLookup, screen, smoothingRadius):
    # Highlight cell
    pygame.draw.rect(screen, (10, 20, 250), ((sampleCell[0] * smoothingRadius, sampleCell[1] * smoothingRadius), (smoothingRadius, smoothingRadius)), 3)

    # spatialLookupV2 = []
    # for particle in particles:
    #     cellCoord = posToCellCoord(particle.predictedPosition, smoothingRadius)
    #     cellKey = cellKeys[cellCoord]
    #     spatialLookupV2.append(cellKey)
    
    # print(spatialLookupV2)

    # Get key of current cell, then loop over all points that share that key
    key = cellKeys[(sampleCell[0], sampleCell[1])]
    cellStartIndex = startIndices[key]

    # Check to for inf value, inf means the square is empty
    if cellStartIndex == math.inf:
        # print("Sample Cell is empty")
        return

    for i in range(cellStartIndex, len(spatialLookup)):

        # Exit loop if we are no longer looking at the correct cell
        if (spatialLookup[i][1] != key):
            break

        particle = particles[spatialLookup[i][0]]
            
        # Highlight particle
        # drawSmoothingRadius(screen, (20, 250, 50), particle, smoothingRadius)
        pygame.draw.circle(screen, (255, 50, 50), particle.position, particle.radius*1.8)

def sleep_code(secs:int, num_of_msgs):

    print("Code started sleeping ...")
    print(f"Waking up in {secs} seconds")

    # Sleep time divided into number of messages
    divided_time = secs / num_of_msgs
    secs_left = secs

    for _ in range(num_of_msgs):
        time.sleep(divided_time)
        secs_left -= divided_time
        print(f"Waking up in {secs_left} seconds{'!!!' if secs_left <= 10 else '!!' if secs_left <= 30 else '!' if secs_left <= 60 else ''}")

# Label each cell in the grid inside of the screen
def getCellKeys(screen_width, screen_height, smoothing_radius) -> dict:
    
    # Dictionary to store cell coordinates and key
    cellKeys = {}

    # Calculate the number of cells in x and y axis
    cellsX = screen_width // smoothing_radius
    cellsY = screen_height // smoothing_radius

    # Loop over all cells inside the screen
    for row in range(cellsY):
        for col in range(cellsX):
            cellKeys[(col, row)] = col + (cellsX * row)
    
    return cellKeys

# Rendering functions
def draw_bounds(screen, color, bound_pos, bound_size, width):
    pygame.draw.rect(screen, color, (bound_pos.x, bound_pos.y, bound_size.x, bound_size.y), width)
def draw_particles(screen, color, particle):
    pygame.draw.circle(screen, color, particle.position, particle.radius)
def drawSmoothingRadius(screen, color, particle, smoothingRadius):
    pygame.draw.circle(screen, color, particle.position, smoothingRadius, 2)
def drawGrid(screen:pygame.Surface, color:tuple, cellKeys:dict, smoothing_radius:int, edgeWidth:int):
    # Loop over all cells inside the screen
    for cellCoord in cellKeys.keys():
        pygame.draw.rect(screen, color, ((cellCoord[0] * smoothing_radius, cellCoord[1] * smoothing_radius), (smoothing_radius, smoothing_radius)), edgeWidth)

def user_warning(msg):
    print(f"{CmdColors.WARNING}USER WARNING{CmdColors.ENDC} - {CmdColors.WARNING}{msg}{CmdColors.ENDC}")
def _get_dst(particle1, particle2):
    return math.sqrt((particle2.x - particle1.x)**2 + (particle2.y - particle1.y)**2)
def _get_random_dir():
    return (-1 if random.random() > 0.5 else 1, -1 if random.random() > 0.5 else 1)
def _get_max_col(cell_keys:dict):
    return max(list(zip(*list(cell_keys.keys())))[0])
def _get_max_row(cell_keys:dict):
    return max(list(zip(*list(cell_keys.keys())))[1])