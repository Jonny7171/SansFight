import pygame
import sys
from settings import *
from ui.fight_ui import get_fight_box, draw_fight_box
from ui.menu_ui import load_menu_assets, draw_menu
from ui.common_ui import draw_hp_bar
from player import Player
from attacks import test_bones
from ui.death_ui import play_death_animation
from ui.act_ui import draw_act_screen
from ui.item_ui import draw_item_screen
from ui.mercy_ui import draw_mercy_screen
from ui.sans_ui import load_sans_assets, draw_sans





pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bad Time Simulator")
clock = pygame.time.Clock()

current_state = STATE_MENU
running = True

# Load menu assets (buttons with both color versions)
buttons = load_menu_assets()
menu_index = 0

# Load Sans assets
sans_assets = load_sans_assets()
current_sans_sprite = sans_assets["normal"]  # set an initial sprite

# Create player
dummy_fight_box = get_fight_box() 
player = Player("assets/heart.png", dummy_fight_box.center)

# Fight state assets (initialized on state change)
fight_box = None
bones = []

# When switching to ACT, we use this flag to ignore leftover key events on the first frame.
skip_act_update = False

while running:
    screen.fill(BLACK)
    events = pygame.event.get()  # Get events once per frame

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        #this can definitely be improved, but works for now to keep track of the last state for act
        if (hasattr(draw_item_screen, 'last_state') and current_state != STATE_ITEM):
            draw_item_screen.last_state = None
    
        if current_state != STATE_MENU:
    # Clear typewriter attributes so they won't persist.
            if hasattr(draw_menu, 'last_letter_time'):
                del draw_menu.last_letter_time
            if hasattr(draw_menu, 'dialogue_index'):
                del draw_menu.dialogue_index
            if hasattr(draw_menu, 'dialogue_full'):
                del draw_menu.dialogue_full
        # MENU state event handling:
        if current_state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    menu_index = (menu_index - 1) % 4
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    menu_index = (menu_index + 1) % 4
                if event.key == pygame.K_RETURN:
                    if menu_index == 0:  # FIGHT
                        current_state = STATE_ATTACK
                        fight_box = get_fight_box()
                        player.rect.center = fight_box.center
                        bones = []
                    elif menu_index == 1:  # ACT
                        current_state = STATE_ACT
                    elif menu_index == 2:  # ITEM
                        current_state = STATE_ITEM
                    elif menu_index == 3:  # MERCY
                        current_state = STATE_SPARE

        #ACT STARTS HERE
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
                    current_state = STATE_ACT_RESPONSE
        
        elif current_state == STATE_ACT_RESPONSE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_state = STATE_MENU
        #ACT ENDS HERE

        #ITEM STARTS HERE
        # ITEM state event handling:
        elif current_state == STATE_ITEM:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                    current_state = STATE_MENU


        # ATTACK state event handling:
        elif current_state == STATE_ATTACK:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                    current_state = STATE_MENU

        # Mercy state event handling:
        elif current_state == STATE_SPARE:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT, pygame.K_RETURN]:
                    current_state = STATE_MENU

    # =========================
    # RENDER LOGIC PER STATE
    # =========================
    draw_sans(screen, current_sans_sprite)

    if current_state == STATE_MENU:
        draw_menu(screen, buttons, menu_index, True)
        draw_hp_bar(screen, player.hp, MAX_HP)

    #IN THE ACT STATE
    elif current_state == STATE_ACT or current_state == STATE_ACT_SANS or current_state == STATE_ACT_RESPONSE:
        # Load and scale the heart image.
        heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (16, 16))
        draw_act_screen(screen, heart_image, current_state)
        draw_menu(screen, buttons, menu_index)
        draw_hp_bar(screen, player.hp, MAX_HP)

    #IN THE ITEM STATE
    elif current_state == STATE_ITEM:
        # Load and scale the heart image.
        heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (16, 16))
        draw_item_screen(screen, heart_image, current_state, events, player)
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
    
    elif current_state == STATE_SPARE:
        # Load and scale the heart image.
        heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (16, 16))
        draw_mercy_screen(screen, heart_image, current_state)
        draw_menu(screen, buttons, menu_index)
        draw_hp_bar(screen, player.hp, MAX_HP)

    elif current_state == STATE_GAME_OVER:
        play_death_animation(screen, player.rect)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()