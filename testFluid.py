import numpy as np
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Particle settings
num_particles = 100
positions = np.random.rand(num_particles, 2) * np.array([width, height])
velocities = np.random.rand(num_particles, 2) * 2 - 1  # Random velocities
particle_radius = 5

# Obstacle settings
obstacle = pygame.Rect(width // 2 - 50, height // 2 - 50, 100, 100)

def update_positions():
    global positions, velocities
    positions += velocities
    # Boundary conditions for the screen edges
    mask_x = (positions[:, 0] <= particle_radius) | (positions[:, 0] >= width - particle_radius)
    mask_y = (positions[:, 1] <= particle_radius) | (positions[:, 1] >= height - particle_radius)
    velocities[mask_x, 0] *= -1
    velocities[mask_y, 1] *= -1

def apply_forces():
    global velocities
    velocities[:, 1] += 0.05  # Simple gravity

def obstacle_interaction():
    global positions, velocities
    # Check if any particle is within the obstacle and bounce it off
    for i, pos in enumerate(positions):
        if obstacle.collidepoint(pos):
            # Simple reflection based on position inside the obstacle
            if obstacle.left < pos[0] < obstacle.right:
                velocities[i][1] *= -1
            if obstacle.top < pos[1] < obstacle.bottom:
                velocities[i][0] *= -1

def render():
    screen.fill(BLACK)
    # Draw particles
    for pos in positions:
        pygame.draw.circle(screen, BLUE, pos.astype(int), particle_radius)
    # Draw obstacle
    pygame.draw.rect(screen, WHITE, obstacle)
    pygame.display.flip()

def main_loop():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update_positions()
        apply_forces()
        obstacle_interaction()
        render()

        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main_loop()
