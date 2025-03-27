import pygame
import sys
from settings import *
from ui import *
from player import Player
from attacks import Bone, test_bones
from death_ui import play_death_animation


pygame.init()

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Time Simulator")
clock = pygame.time.Clock()

# Fight box
fight_box = get_fight_box()

# Player setup
player = Player("assets/heart.png", fight_box.center)
bones = []





# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Handle player movement and keep the heart inside the fight box
    inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)
    player.handle_movement(keys, inner_box)
    #draw fight box and player
    draw_fight_box(screen, fight_box)
    player.draw(screen)



    #Bones test
    test_bones(screen, player, bones)

    #End loop stuff
    draw_hp_bar(screen, player.hp, MAX_HP)
    player.update_invincibility()

    if player.hp <= 0:
        play_death_animation(screen, player.rect)
        running = False  # Or trigger retry/death screen


    #Keep this last
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
