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
positions = np.random.rand(num_particles, 2) * np.array([width, height])
velocities = np.random.rand(num_particles, 2) * 2 - 1  # Random velocities
particle_radius = 5
interaction_radius = 25  # Radius within which particles will interact

# Define the channel walls (fully enclosed) and an obstruction
channel_walls = [
    pygame.Rect(100, 100, 600, 10),  # Top wall
    pygame.Rect(100, 500, 600, 10),  # Bottom wall
    pygame.Rect(100, 100, 10, 400),  # Left wall
    pygame.Rect(690, 100, 10, 400),  # Right wall
]

# Add an obstruction in the middle of the channel
obstructions = [
    pygame.Rect(350, 250, 100, 100),  # Middle obstruction
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
    # Apply a force in the x-direction to simulate flow, no gravity
    velocities[:, 0] += 0.05

def channel_and_obstruction_interaction():
    global positions, velocities
    # Handle interactions with the channel walls
    for wall in channel_walls:
        for i, pos in enumerate(positions):
            if wall.collidepoint(pos[0], pos[1]):
                velocities[i] *= -1
    # Handle interactions with the obstructions
    for obstruction in obstructions:
        for i, pos in enumerate(positions):
            if obstruction.collidepoint(pos[0], pos[1]):
                velocities[i] *= -1

def render():
    screen.fill(BLACK)
    for pos in positions:
        pygame.draw.circle(screen, BLUE, pos.astype(int), particle_radius)
    # Draw channel walls
    for wall in channel_walls:
        pygame.draw.rect(screen, WHITE, wall)
    # Draw obstructions
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
