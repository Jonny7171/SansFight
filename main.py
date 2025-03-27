import pygame
import sys
from settings import *
from ui import get_fight_box, draw_fight_box

pygame.init()


#SETUP
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Time Simulator")
clock = pygame.time.Clock()

#set fight box
fight_box = get_fight_box()

# Load Images
heart_image = pygame.image.load("assets/heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (16, 16))
heart_rect = heart_image.get_rect(center=fight_box.center)
heart_speed = 5







running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move heart
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        heart_rect.x -= heart_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        heart_rect.x += heart_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        heart_rect.y -= heart_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        heart_rect.y += heart_speed

    # Keep the heart in the box
    heart_rect.clamp_ip(fight_box)

    # Draw everything
    draw_fight_box(screen, fight_box)
    screen.blit(heart_image, heart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
