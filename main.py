import pygame
import sys
from settings import *
from ui.fight_ui import get_fight_box, draw_fight_box
from ui.menu_ui import load_menu_assets, draw_menu
from ui.common_ui import draw_hp_bar
from player import Player
from Bone_Class import *
from ui.death_ui import play_death_animation
from ui.act_ui import draw_act_screen
from ui.item_ui import draw_item_screen
from ui.mercy_ui import draw_mercy_screen
from ui.sans_ui import load_sans_assets, draw_sans, SansSpriteManager
from attacks.Sans_bones_attack_low import Sans_Bone_Gap_Low
from attacks.sans_gaster_blaster_attack import sans_gaster_blaster_attack
from attacks.sansSlamAttack import SansSlamAttack
from attacks.Sans_slam_multiple import SansSlamMultiple

def main():
    global current_state, current_attack, attack_state, fight_box, sans_visible, bones, player

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bad Time Simulator")
    clock = pygame.time.Clock()
    current_state = STATE_MENU
    running = True

    buttons = load_menu_assets()
    menu_index = 0

    pygame.mixer.init()
    pygame.mixer.music.load("sounds/megalovania.ogg")
    pygame.mixer.music.play(-1)

    sans_sprite_manager = SansSpriteManager()
    sans_visible = True

    dummy_fight_box = get_fight_box()
    player = Player("assets/heart.png", dummy_fight_box.center)

    fight_box = None
    bones = []

    attack_state = 1
    current_attack = None

    def begin_attack():
        global current_state, current_attack, attack_state, fight_box, sans_visible, bones, player
        if attack_state == 1:
            fight_box = get_fight_box(250)  # First create fight_box
            current_attack = Sans_Bone_Gap_Low()
            player.set_blue_mode(True)
        elif attack_state == 2:
            fight_box = get_fight_box(350)  # First create fight_box
            current_attack = sans_gaster_blaster_attack(player)
            sans_visible = False
            player.set_blue_mode(False)
        elif attack_state == 3:
            fight_box = get_fight_box(150)  # Create fight_box FIRST
            current_attack = SansSlamMultiple(player, fight_box, direction=None, sans_sprite_manager=sans_sprite_manager)
            player.set_blue_mode(True)
            
        current_state = STATE_ATTACK
        player.rect.center = fight_box.center
        bones = []

    while running:
        screen.fill(BLACK)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if hasattr(draw_item_screen, 'last_state') and current_state != STATE_ITEM:
                draw_item_screen.last_state = None

            if current_state != STATE_MENU:
                if hasattr(draw_menu, 'last_letter_time'):
                    del draw_menu.last_letter_time
                if hasattr(draw_menu, 'dialogue_index'):
                    del draw_menu.dialogue_index
                if hasattr(draw_menu, 'dialogue_full'):
                    del draw_menu.dialogue_full

        #MENU
            if current_state == STATE_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        menu_index = (menu_index - 1) % 4
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        menu_index = (menu_index + 1) % 4
                    if event.key == pygame.K_RETURN:
                        if menu_index == 0:
                            begin_attack()
                        elif menu_index == 1:
                            current_state = STATE_ACT
                        elif menu_index == 2:
                            current_state = STATE_ITEM
                        elif menu_index == 3:
                            current_state = STATE_SPARE

            #ACT
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
                        begin_attack()


        #ITEM
            elif current_state == STATE_ITEM:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                        current_state = STATE_MENU
                    #elif event.key == pygame.K_RETURN:
                     #   begin_attack()

        #ATTACK
            elif current_state == STATE_ATTACK:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                        current_state = STATE_MENU

        #SPARE
            elif current_state == STATE_SPARE:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_RSHIFT]:
                        current_state = STATE_MENU
                    elif event.key == pygame.K_RETURN:
                        begin_attack()

        sans_sprite_manager.draw(screen)

        if current_state == STATE_MENU:
            draw_menu(screen, buttons, menu_index, True)
            draw_hp_bar(screen, player.hp, MAX_HP)

        elif current_state in [STATE_ACT, STATE_ACT_SANS, STATE_ACT_RESPONSE]:
            heart_image = pygame.image.load("assets/heart.png").convert_alpha()
            heart_image = pygame.transform.scale(heart_image, (16, 16))
            draw_act_screen(screen, heart_image, current_state)
            draw_menu(screen, buttons, menu_index)
            draw_hp_bar(screen, player.hp, MAX_HP)

        elif current_state == STATE_ITEM:
            heart_image = pygame.image.load("assets/heart.png").convert_alpha()
            heart_image = pygame.transform.scale(heart_image, (16, 16))
            eaten_flag = draw_item_screen(screen, heart_image, current_state, events, player)
            if eaten_flag:
                current_state = STATE_ATTACK
                begin_attack()
            draw_menu(screen, buttons, menu_index)
            draw_hp_bar(screen, player.hp, MAX_HP)

        elif current_state == STATE_ATTACK:
            keys = pygame.key.get_pressed()
            inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)
            if fight_box and not isinstance(current_attack, SansSlamMultiple):
                
                player.handle_movement(keys, inner_box)

            draw_fight_box(screen, fight_box)
            player.draw(screen)
            current_attack.update()
            current_attack.draw(screen)

            if current_attack.check_collision(player.rect):
                player.take_damage(1)

            draw_hp_bar(screen, player.hp, MAX_HP)

            if player.hp <= 0:
                current_state = STATE_GAME_OVER

            if current_attack.is_done():
                attack_state += 1
                current_attack = None
                player.set_blue_mode(False)
                sans_visible = True
                current_state = STATE_MENU
                player.velocity = pygame.Vector2(0, 0)

        elif current_state == STATE_SPARE:
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

if __name__ == "__main__":
    main()
