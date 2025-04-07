import pygame
from settings import *
from ui.fight_ui import draw_fight_box, get_fight_box
from ui.common_ui import draw_hp_bar

attack_anim_timer = 0
sans_x_offset = 0
animation_done = False

def reset_player_attack_animation():
    global attack_anim_timer, sans_x_offset, animation_done
    attack_anim_timer = 0
    sans_x_offset = 0
    animation_done = False

def play_player_attack_animation(screen, player, sans_sprite_manager, fight_box):
    global attack_anim_timer, sans_x_offset, animation_done
    slash_image = pygame.image.load("assets/slash.png").convert_alpha()
    slash_image = pygame.transform.rotate(slash_image, 90)
    base_width, base_height = slash_image.get_size()
    SLIDE_OUT_DURATION = 15
    SLASH_DURATION = 15
    MISS_DURATION = 50
    SLIDE_IN_DURATION = 30
    SLASH_OVERLAP = 5
    phase1_end = SLIDE_OUT_DURATION - SLASH_OVERLAP         
    phase2_end = phase1_end + SLASH_DURATION                  
    phase3_end = phase2_end + MISS_DURATION                   
    phase4_end = phase3_end + SLIDE_IN_DURATION               
    TOTAL_DURATION = phase4_end
    SANS_OFF_OFFSET = -60
    attack_anim_timer += 1
    origin_x, origin_y = (340, 80)
    draw_fight_box(screen, fight_box)
    draw_hp_bar(screen, player.hp, MAX_HP)
    #player.draw(screen)

    # 1- Slide Out Sans
    if attack_anim_timer <= phase1_end:
        sans_x_offset = - (attack_anim_timer / phase1_end) * abs(SANS_OFF_OFFSET)
    # 2- Slash Animation starts
    elif attack_anim_timer <= phase2_end:
        sans_x_offset = SANS_OFF_OFFSET
        slash_progress = (attack_anim_timer - phase1_end) / SLASH_DURATION
        scaled_width = int(base_width * slash_progress)
        scaled_height = int(base_height * slash_progress)
        if scaled_width <= 0: scaled_width = 1
        if scaled_height <= 0: scaled_height = 1
        scaled_slash = pygame.transform.scale(slash_image, (scaled_width, scaled_height))

        slash_x = origin_x - 60 - ((phase1_end / attack_anim_timer) * 30)
        slash_y = origin_y - 20
        screen.blit(scaled_slash, (slash_x, slash_y))
    # 3- MISS text appears
    elif attack_anim_timer <= phase3_end:
        sans_x_offset = SANS_OFF_OFFSET
        font = pygame.font.SysFont("comicsans", 24)
        miss_text = font.render("MISS", True, WHITE)
        text_pos = (270, origin_y - miss_text.get_height() - 20)
        screen.blit(miss_text, text_pos)
    # 4- Slide In Sans
    elif attack_anim_timer <= phase4_end:
        time_into_slide_in = attack_anim_timer - phase3_end
        sans_x_offset = SANS_OFF_OFFSET * (1 - (time_into_slide_in / SLIDE_IN_DURATION))
    else:
        animation_done = True
        return False
    sans_sprite_manager.draw(screen, offset_x=sans_x_offset)
    return True
