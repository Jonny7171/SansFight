import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sans Fight - Heart Sprite")

# Clock
clock = pygame.time.Clock()

# Load heart image
heart_image = pygame.image.load("heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (16, 16))
heart_rect = heart_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
heart_speed = 5

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        heart_rect.x -= heart_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        heart_rect.x += heart_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        heart_rect.y -= heart_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        heart_rect.y += heart_speed

    # Draw heart
    screen.blit(heart_image, heart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()