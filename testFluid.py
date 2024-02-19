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

# Obstacle settings
obstacle = pygame.Rect(width // 2 - 50, height // 2 - 50, 100, 100)

@jit(nopython=True)
def particle_interaction(positions, velocities, num_particles, interaction_radius):
    for i in range(num_particles):
        for j in range(i + 1, num_particles):  # Avoid double checking pairs
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
    velocities[:, 1] += 0.05  # Simple gravity

def obstacle_interaction():
    global positions, velocities
    for i, pos in enumerate(positions):
        if obstacle.collidepoint(pos):
            if obstacle.left < pos[0] < obstacle.right:
                velocities[i][1] *= -1
            if obstacle.top < pos[1] < obstacle.bottom:
                velocities[i][0] *= -1

def render():
    screen.fill(BLACK)
    for pos in positions:
        pygame.draw.circle(screen, BLUE, pos.astype(int), particle_radius)
    pygame.draw.rect(screen, WHITE, obstacle)
    pygame.display.flip()

def main_loop():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Check if 'x' key is pressed
                    pygame.quit()
                    sys.exit()

        global velocities
        velocities = particle_interaction(positions, velocities, num_particles, interaction_radius)
        update_positions()
        apply_forces()
        obstacle_interaction()
        render()

        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main_loop()
