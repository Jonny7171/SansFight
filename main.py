import pygame
import sys
from settings import *
from ui import get_fight_box, draw_fight_box
from player import Player


pygame.init()

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Time Simulator")
clock = pygame.time.Clock()

# Fight box
fight_box = get_fight_box()

# Player setup
player = Player("assets/heart.png", fight_box.center)





# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Handle player movement and keep the heart inside the fight box
    player.handle_movement(keys, fight_box)
    #draw fight box and player
    draw_fight_box(screen, fight_box)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
