import pygame
import sys
from settings import *
from ui.fight_ui import get_fight_box, draw_fight_box
from ui.menu_ui import load_menu_assets, draw_menu
from ui.common_ui import draw_hp_bar
from player import Player
from attacks import *
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

# Load menu assets
buttons = load_menu_assets()
menu_index = 0

#Megalovania music
pygame.mixer.init()
pygame.mixer.music.load("sounds/megalovania.ogg")
pygame.mixer.music.play(-1)  # Loop forever


# Load Sans assets
sans_assets = load_sans_assets()
current_sans_sprite = sans_assets["normal"]
current_sans_sprite_name = "normal" 

# Create player
dummy_fight_box = get_fight_box() 
player = Player("assets/heart.png", dummy_fight_box.center)

# Fight state assets (initialized on state change)
fight_box = None
bones = []

#attack state variables
attack_state = 1



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
                        # Set the attack
                        if attack_state == 1:
                            current_attack = Sans_Bone_Gap_Low()
                            player.set_blue_mode(True)
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
    draw_sans(screen, current_sans_sprite, current_sans_sprite_name)

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

    # IN THE ITEM STATE
    elif current_state == STATE_ITEM:
        # Load and scale the heart image.
        heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        heart_image = pygame.transform.scale(heart_image, (16, 16))
        draw_item_screen(screen, heart_image, current_state, events, player)
        draw_menu(screen, buttons, menu_index)
        draw_hp_bar(screen, player.hp, MAX_HP)

    # IN THE ATTACK STATE
    elif current_state == STATE_ATTACK:
        # Get input for movement (blue mode physics already in player's handle_movement)
        keys = pygame.key.get_pressed()
        if fight_box:
            inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)
            player.handle_movement(keys, inner_box)

        # Draw the fight box and player
        draw_fight_box(screen, fight_box)
        player.draw(screen)

        # Update and draw the attack
        current_attack.update()  # current_attack is an instance of SansAttack2
        current_attack.draw(screen)

        # Check collision between the player and the attack's bones
        if current_attack.check_collision(player.rect):
            player.take_damage(1)

        # Draw the HP bar (using player's current HP)
        draw_hp_bar(screen, player.hp, MAX_HP)
        
        # If player's HP is 0, trigger game over
        if player.hp <= 0:
            current_state = STATE_GAME_OVER

        # (Optional) Check if the attack is finished, then transition to the next state:
        if current_attack.is_done():
            # For example, go back to the menu or proceed to the next attack
            current_attack = None
            player.set_blue_mode(False)
            current_state = STATE_MENU  # or a different state

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
