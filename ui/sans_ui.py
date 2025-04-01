import pygame
from settings import *

def load_sans_assets():

    sans_normal = pygame.image.load("assets/sans.png").convert_alpha()
    sans_blue_eye = pygame.image.load("assets/sans_blue_eye.png").convert_alpha()
    sans_cut = pygame.image.load("assets/sans_cut.png").convert_alpha()
    sans_hand_out = pygame.image.load("assets/sans_hand_out.png").convert_alpha()
    sans_sweat = pygame.image.load("assets/sans_sweat.png").convert_alpha()
    sans_wink = pygame.image.load("assets/sans_wink.png").convert_alpha()

    sans_normal = pygame.transform.scale(sans_normal, (110, 200))
    sans_blue_eye = pygame.transform.scale(sans_blue_eye, (110, 200))
    sans_cut = pygame.transform.scale(sans_cut, (110, 200))
    sans_hand_out = pygame.transform.scale(sans_hand_out, (110, 200))
    sans_sweat = pygame.transform.scale(sans_sweat, (110, 200))
    sans_wink = pygame.transform.scale(sans_wink, (110, 200))
    
    return {
        "normal": sans_normal,
        "blue_eye": sans_blue_eye,
        "cut": sans_cut,
        "hand_out": sans_hand_out,
        "sweat": sans_sweat,
        "wink": sans_wink,
    }

def draw_sans(screen, sans_sprite, current_sans_sprite_name, fight_box=None, sans_visible = True):
    if not sans_visible:
        return
    if current_sans_sprite_name == "normal":
        x = WIDTH // 2 - sans_sprite.get_width() // 2
        y = SANS_NORMAL_Y
        screen.blit(sans_sprite, (x, y))
    elif current_sans_sprite_name == "blue_eye":
        x = WIDTH // 2 - sans_sprite.get_width() // 2
        y = SANS_BLUR_EYE_Y
        screen.blit(sans_sprite, (x, y))
    elif current_sans_sprite_name == "cut":
        x = WIDTH // 2 - sans_sprite.get_width() // 2
        y = SANS_CUT_Y
        screen.blit(sans_sprite, (x, y))
    elif current_sans_sprite_name == "hand_out":
        x = WIDTH // 2 - sans_sprite.get_width() // 2
        y = SANS_HAND_OUT_Y
        screen.blit(sans_sprite, (x, y))
    elif current_sans_sprite_name == "sweat":
        x = WIDTH // 2 - sans_sprite.get_width() // 2
        y = SANS_SWEAT_Y
        screen.blit(sans_sprite, (x, y))
    elif current_sans_sprite_name == "wink":
        x = WIDTH // 2 - sans_sprite.get_width() // 2
        y = SANS_WINK_Y
        screen.blit(sans_sprite, (x, y))

    
