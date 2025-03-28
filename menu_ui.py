# menu_ui.py
import pygame
from settings import *

def load_menu_assets():
    """Load orange + yellow versions for each button, scale, and return them in a list."""
    fight_orange = pygame.image.load("assets/fight_orange.png").convert_alpha()
    fight_yellow = pygame.image.load("assets/fight_yellow.png").convert_alpha()

    act_orange   = pygame.image.load("assets/act_orange.png").convert_alpha()
    act_yellow   = pygame.image.load("assets/act_yellow.png").convert_alpha()

    item_orange  = pygame.image.load("assets/item_orange.png").convert_alpha()
    item_yellow  = pygame.image.load("assets/item_yellow.png").convert_alpha()

    mercy_orange = pygame.image.load("assets/mercy_orange.png").convert_alpha()
    mercy_yellow = pygame.image.load("assets/mercy_yellow.png").convert_alpha()

    # Scale them to your desired size
    def scale_btn(img):
        return pygame.transform.scale(img, (120, 48))

    fight_orange = scale_btn(fight_orange)
    fight_yellow = scale_btn(fight_yellow)
    act_orange   = scale_btn(act_orange)
    act_yellow   = scale_btn(act_yellow)
    item_orange  = scale_btn(item_orange)
    item_yellow  = scale_btn(item_yellow)
    mercy_orange = scale_btn(mercy_orange)
    mercy_yellow = scale_btn(mercy_yellow)

    # Return a list of (orange, yellow) pairs, in the order FIGHT=0, ACT=1, ITEM=2, MERCY=3
    buttons = [
        (fight_orange, fight_yellow),
        (act_orange,   act_yellow),
        (item_orange,  item_yellow),
        (mercy_orange, mercy_yellow),
    ]
    return buttons


def draw_menu(screen, buttons, menu_index):
    """
    Draw the 4 menu buttons (FIGHT, ACT, ITEM, MERCY) along the bottom,
    highlighting the one at 'menu_index' with the yellow version.
    """
    #draw box
    box_width = 500
    box_height = 150
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    menu_box = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, WHITE, menu_box, width=5)
    margin = 10
    menu_y = screen.get_height() - buttons[0][0].get_height() - margin

    gap = 20
    # Each button pair has the same size, so let's get the width of the orange one:
    btn_width  = buttons[0][0].get_width()
    btn_height = buttons[0][0].get_height()

    total_buttons_width = btn_width * len(buttons)
    total_gaps_width    = gap * (len(buttons) - 1)
    total_width         = total_buttons_width + total_gaps_width

    start_x = (screen.get_width() - total_width) // 2

    x = start_x
    for i, (orange_img, yellow_img) in enumerate(buttons):
        # If i == menu_index, draw the yellow version; else draw the orange
        if i == menu_index:
            screen.blit(yellow_img, (x, menu_y))
        else:
            screen.blit(orange_img, (x, menu_y))
        x += btn_width + gap
