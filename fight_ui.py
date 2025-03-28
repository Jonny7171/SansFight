# fight_ui.py
import pygame
from settings import WIDTH, HEIGHT, WHITE

def get_fight_box(box_width=150, box_height=150):
    """
    A smaller box for the actual fight/dodge phase.
    Adjust size or position as you like.
    """
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    return pygame.Rect(box_x, box_y, box_width, box_height)

def draw_fight_box(screen, fight_box):
    pygame.draw.rect(screen, WHITE, fight_box, width=5)