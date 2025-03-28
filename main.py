import pygame
import sys
from settings import *
from fight_ui import get_fight_box, draw_fight_box
from menu_ui import load_menu_assets, draw_menu
from common_ui import draw_hp_bar
from player import Player
from attacks import test_bones
from death_ui import play_death_animation

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Time Simulator")
clock = pygame.time.Clock()

current_state = STATE_MENU
running = True

# menu assets
buttons = load_menu_assets()
#track where in menu we are
menu_index = 0

# create player
dummy_fight_box = get_fight_box() 
player = Player("assets/heart.png", dummy_fight_box.center)

# We'll create actual fight_box, bones, etc. once we go to ATTACK
fight_box = None
bones = []

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#STATE SWITCHING
        if current_state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                # Move selection left or right
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    menu_index = (menu_index - 1) % 4
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    menu_index = (menu_index + 1) % 4
                # If user presses Z/ENTER to confirm, switch to ATTACK or do something
                if event.key == pygame.K_RETURN:
                    # ATTACK
                    if menu_index == 0:
                        current_state = STATE_ATTACK
                        fight_box = get_fight_box()
                        player.rect.center = fight_box.center
                        bones = []
                    # ACT
                    elif menu_index == 1:
                        # ACT logic here
                        pass
                    # ITEM
                    elif menu_index == 2:
                        # ITEM logic here
                        pass
                    # MERCY
                    elif menu_index == 3:
                        # MERCY logic here
                        pass
                    # If they choose ACT (1), ITEM (2), MERCY (3) you can do something else. Add here!

        elif current_state == STATE_ATTACK:
            if event.type == pygame.KEYDOWN:
                # Maybe ESC or something returns to MENU
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_MENU

    # =========================
    # RENDER LOGIC PER STATE
    # =========================
    if current_state == STATE_MENU:
        # drae menu
        draw_menu(screen, buttons, menu_index)
        # draw hp bar
        draw_hp_bar(screen, player.hp, MAX_HP)

    elif current_state == STATE_ATTACK:
        # Move the player
        keys = pygame.key.get_pressed()
        if fight_box:
            inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)
            player.handle_movement(keys, inner_box)
            # Draw fight box
            draw_fight_box(screen, fight_box)
            # Draw player
            player.draw(screen)
            # Bones test
            test_bones(screen, player, bones)
            # HP bar
            draw_hp_bar(screen, player.hp, MAX_HP)
            # Check invincibility + death
            player.update_invincibility()
            if player.hp <= 0:
                play_death_animation(screen, player.rect)
                current_state = STATE_GAME_OVER

    elif current_state == STATE_GAME_OVER:
        play_death_animation(screen, player.rect)
        #end game for now
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()