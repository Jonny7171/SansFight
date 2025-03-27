import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sans Fight - Starter")

# Clock to control FPS
clock = pygame.time.Clock()

# Colors
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

# Heart (soul) position
heart_pos = [WIDTH // 2, HEIGHT // 2]
heart_size = 20
heart_speed = 5

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        heart_pos[0] -= heart_speed
    if keys[pygame.K_RIGHT]:
        heart_pos[0] += heart_speed
    if keys[pygame.K_UP]:
        heart_pos[1] -= heart_speed
    if keys[pygame.K_DOWN]:
        heart_pos[1] += heart_speed

    # Draw heart (placeholder: blue square)
    pygame.draw.rect(screen, BLUE, (heart_pos[0], heart_pos[1], heart_size, heart_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
