import pygame

def draw_particles(screen, color, particle):
    pygame.draw.circle(screen, color, particle.position, particle.radius)

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

def draw_bounds(screen, color, bound_pos, bound_size, width):
    pygame.draw.rect(screen, color, (bound_pos.x, bound_pos.y, bound_size.x, bound_size.y), width)
