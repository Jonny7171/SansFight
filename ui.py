import pygame
from settings import *

# Get the position and size of the fight box
def get_fight_box(box_width=150, box_height=150):
    box_x = (WIDTH - box_width) // 2
    box_y = ((HEIGHT - box_height) // 2) + 50
    return pygame.Rect(box_x, box_y, box_width, box_height)

# Draw the fight box
def draw_fight_box(screen, fight_box):
    pygame.draw.rect(screen, WHITE, fight_box, width=5)

# Draw the HP bar
def draw_hp_bar(screen, current_hp, max_hp):
    # Position and size
    bar_width = 200
    bar_height = 20
    x = 200
    y = HEIGHT - 50  # Near the bottom of the screen

    # Colors
    bg_color = RED
    hp_color = (255, 255, 0)

    # Draw background
    pygame.draw.rect(screen, bg_color, (x, y, bar_width, bar_height))

    # Calculate and draw HP fill
    hp_ratio = max(current_hp, 0) / MAX_HP
    fill_width = int(bar_width * hp_ratio)
    pygame.draw.rect(screen, hp_color, (x, y, fill_width, bar_height))

    # Load fonts (ensure these file names match your files)
    font_HP = pygame.font.Font("assets/fonts/8bit_wonder.ttf", 9)
    font_num = pygame.font.Font("assets/fonts/health.ttf", 20)
    #font_num.set_bold(True)

    # Render "HP" label using 8-Bit Wonder font
    hp_label = font_HP.render("HP", False, WHITE)

    # Render the numeric HP using the health font
    hp_text = f"{current_hp} / {max_hp}"
    hp_num = font_num.render(hp_text, False, WHITE)

    # Blit the text surfaces to the screen with some spacing
    screen.blit(hp_label, (x + bar_width + 5, y + 4))
    screen.blit(hp_num, (x + bar_width + 30, y - 2))

    