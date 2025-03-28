import pygame
import sys
from settings import *
from ui.fight_ui import get_fight_box, draw_fight_box
from ui.menu_ui import load_menu_assets, draw_menu
from ui.common_ui import draw_hp_bar
from player import Player
from attacks import test_bones
from ui.death_ui import play_death_animation
from ui.act_ui import update_act_state, draw_act_screen, act_substate

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Time Simulator")
clock = pygame.time.Clock()

current_state = STATE_MENU
running = True

# Load menu assets (buttons with both color versions)
buttons = load_menu_assets()
menu_index = 0

# Create player
dummy_fight_box = get_fight_box() 
player = Player("assets/heart.png", dummy_fight_box.center)

# Fight state assets (initialized on state change)
fight_box = None
bones = []

# Flags to ensure one key press triggers one action
enter_processed = False
# When switching to ACT, we use this flag to ignore leftover key events on the first frame.
skip_act_update = False

while running:
    screen.fill(BLACK)
    events = pygame.event.get()  # Get events once per frame

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # MENU state event handling:
        if current_state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    menu_index = (menu_index - 1) % 4
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    menu_index = (menu_index + 1) % 4
                if event.key == pygame.K_RETURN and not enter_processed:
                    enter_processed = True
                    if menu_index == 0:  # FIGHT
                        current_state = STATE_ATTACK
                        fight_box = get_fight_box()
                        player.rect.center = fight_box.center
                        bones = []
                    elif menu_index == 1:  # ACT
                        current_state = STATE_ACT
                        # Set flag to skip any ACT update on the first frame
                        skip_act_update = True
                    elif menu_index == 2:  # ITEM
                        # ITEM logic here
                        pass
                    elif menu_index == 3:  # MERCY
                        # MERCY logic here
                        pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    enter_processed = False

        # ACT state event handling:
        elif current_state == STATE_ACT:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                    current_state = STATE_MENU
                elif event.key == pygame.K_RETURN:
                    current_state = STATE_ACT_SANS
        
        elif current_state == STATE_ACT_SANS:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                    current_state = STATE_ACT
                elif event.key == pygame.K_RETURN:
                    current_state = STATE_MENU

        # ATTACK state event handling:
        elif current_state == STATE_ATTACK:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                    current_state = STATE_MENU

    # =========================
    # RENDER LOGIC PER STATE
    # =========================
    if current_state == STATE_MENU:
        draw_menu(screen, buttons, menu_index)
        draw_hp_bar(screen, player.hp, MAX_HP)

    #IN THE ACT STATE
    elif current_state == STATE_ACT or current_state == STATE_ACT_SANS:
        # Load and scale the heart image.
        heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (16, 16))
        draw_act_screen(screen, heart_image, current_state)
        draw_menu(screen, buttons, menu_index)
        draw_hp_bar(screen, player.hp, MAX_HP)

    elif current_state == STATE_ATTACK:
        keys = pygame.key.get_pressed()
        if fight_box:
            inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)
            player.handle_movement(keys, inner_box)
            draw_fight_box(screen, fight_box)
            player.draw(screen)
            test_bones(screen, player, bones)
            draw_hp_bar(screen, player.hp, MAX_HP)
            player.update_invincibility()
            if player.hp <= 0:
                play_death_animation(screen, player.rect)
                current_state = STATE_GAME_OVER

    elif current_state == STATE_GAME_OVER:
        play_death_animation(screen, player.rect)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()