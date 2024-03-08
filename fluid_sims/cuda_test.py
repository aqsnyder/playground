import numpy as np
import pygame
import sys
from numba import cuda
import math

# Pygame initialization
pygame.init()

# Screen dimensions
screen_width = 800  # Use a fixed size for simplicity
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Particle settings
num_particles = 10000  # Reduced for demonstration purposes
positions = np.random.rand(num_particles, 2) * np.array([screen_width, screen_height]).astype(np.float32)
velocities = (np.random.rand(num_particles, 2) * 2 - 1).astype(np.float32)  # Random velocities
particle_radius = 2
interaction_radius = 2.0  # Increased for visibility

# CUDA kernel for particle interaction
@cuda.jit
def particle_interaction_cuda(positions, velocities, interaction_radius, num_particles):
    i = cuda.grid(1)
    if i >= num_particles: return  # Prevent out-of-bounds access

    for j in range(num_particles):
        if i != j:
            dx = positions[i, 0] - positions[j, 0]
            dy = positions[i, 1] - positions[j, 1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < interaction_radius and distance > 0:  # Ensure distance is not zero
                # Adjust velocities directly, avoiding np.array
                inv_distance = 1.0 / distance  # Inverse of distance for normalization
                velocities[i, 0] -= dx * inv_distance * 0.1
                velocities[i, 1] -= dy * inv_distance * 0.1
                # Note: Adjustments to velocities[j] are omitted to prevent race conditions

def apply_particle_interaction(positions, velocities):
    num_particles = positions.shape[0]
    threads_per_block = 256
    blocks_per_grid = (num_particles + (threads_per_block - 1)) // threads_per_block
    particle_interaction_cuda[blocks_per_grid, threads_per_block](positions, velocities, interaction_radius, num_particles)

def update_positions(positions, velocities):
    positions += velocities
    # Boundary conditions
    np.clip(positions[:, 0], particle_radius, screen_width - particle_radius, out=positions[:, 0])
    np.clip(positions[:, 1], particle_radius, screen_height - particle_radius, out=positions[:, 1])

def render(screen, positions):
    screen.fill(BLACK)
    for pos in positions:
        pygame.draw.circle(screen, BLUE, pos.astype(int), particle_radius)
    pygame.display.flip()

def main_loop():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        apply_particle_interaction(positions, velocities)
        update_positions(positions, velocities)
        render(screen, positions)

        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main_loop()
