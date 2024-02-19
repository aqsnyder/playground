import numpy as np
import pygame
import sys
from numba import jit

# Initialize Pygame
pygame.init()

# Screen dimensions and full-screen mode
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Particle settings
num_particles = 1000
# Adjust initial positions to be within the channel
channel_start_x, channel_start_y = 100, 150
channel_end_x, channel_end_y = 700, 450  # Adjust for a longer and skinnier channel
positions = np.random.rand(num_particles, 2) * np.array([channel_end_x - channel_start_x, channel_end_y - channel_start_y]) + np.array([channel_start_x, channel_start_y])
velocities = np.random.rand(num_particles, 2) * 2 - 1  # Random velocities
particle_radius = 2
interaction_radius = 25  # Radius within which particles will interact

# Define the channel walls (fully enclosed) and an obstruction
channel_walls = [
    pygame.Rect(channel_start_x, channel_start_y, channel_end_x - channel_start_x, 10),  # Top wall
    pygame.Rect(channel_start_x, channel_end_y, channel_end_x - channel_start_x, 10),  # Bottom wall
    pygame.Rect(channel_start_x, channel_start_y, 10, channel_end_y - channel_start_y),  # Left wall
    pygame.Rect(channel_end_x, channel_start_y, 10, channel_end_y - channel_start_y),  # Right wall
]

# Adjust obstruction in the middle of the channel
obstructions = [
    pygame.Rect(350, 250, 50, 100),  # Middle obstruction, adjusted for skinnier channel
]

@jit(nopython=True)
def particle_interaction(positions, velocities, num_particles, interaction_radius):
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            dx = positions[i, 0] - positions[j, 0]
            dy = positions[i, 1] - positions[j, 1]
            distance = np.sqrt(dx * dx + dy * dy)
            if distance < interaction_radius:
                direction = np.array([dx, dy]) / distance
                velocities[i] -= direction * 0.1
                velocities[j] += direction * 0.1
    return velocities

def update_positions():
    global positions, velocities
    positions += velocities
    # Boundary conditions for the screen edges
    mask_x = (positions[:, 0] <= particle_radius) | (positions[:, 0] >= width - particle_radius)
    mask_y = (positions[:, 1] <= particle_radius) | (positions[:, 1] >= height - particle_radius)
    velocities[mask_x, 0] *= -1
    velocities[mask_y, 1] *= -1

def apply_forces():
    global positions, velocities
    velocities[:, 0] += 0.05  # Apply a force in the x-direction to simulate flow

def channel_and_obstruction_interaction():
    global positions, velocities
    for wall in channel_walls:
        for i, pos in enumerate(positions):
            if wall.collidepoint(pos[0], pos[1]):
                velocities[i] *= -1
    for obstruction in obstructions:
        for i, pos in enumerate(positions):
            if obstruction.collidepoint(pos[0], pos[1]):
                velocities[i] *= -1

def render():
    screen.fill(BLACK)
    for pos in positions:
        pygame.draw.circle(screen, BLUE, pos.astype(int), particle_radius)
    for wall in channel_walls:
        pygame.draw.rect(screen, WHITE, wall)
    for obstruction in obstructions:
        pygame.draw.rect(screen, WHITE, obstruction)
    pygame.display.flip()

def main_loop():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Exit on 'x'
                    pygame.quit()
                    sys.exit()

        global velocities
        velocities = particle_interaction(positions, velocities, num_particles, interaction_radius)
        update_positions()
        apply_forces()
        channel_and_obstruction_interaction()
        render()

        clock.tick(60)

if __name__ == "__main__":
    main_loop()
