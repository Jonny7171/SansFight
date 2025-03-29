# common_ui.py
import pygame
from settings import *

#draw health bar
def draw_hp_bar(screen, current_hp, max_hp):
    bar_width = HP_WIDTH
    bar_height = HP_HEIGHT
    x = HP_X
    y = HP_Y

    # Bar colors
    bg_color = RED
    hp_color = (255, 255, 0)

    # Background of the HP bar
    pygame.draw.rect(screen, bg_color, (x, y, bar_width, bar_height))

    # Fill based on HP ratio
    hp_ratio = max(current_hp, 0) / max_hp
    fill_width = int(bar_width * hp_ratio)
    pygame.draw.rect(screen, hp_color, (x, y, fill_width, bar_height))

    # Fonts for "HP" and numeric value
    font_HP = pygame.font.Font("assets/fonts/8bit_wonder.ttf", 9)
    font_num = pygame.font.Font("assets/fonts/health.ttf", 20)

    # Render "HP"
    hp_label = font_HP.render("HP", False, WHITE)
    # Render "## / 92"
    hp_text = f"{current_hp} / {max_hp}"
    hp_num = font_num.render(hp_text, False, WHITE)

    # Blit them
    screen.blit(hp_label, (x + bar_width + 5, y + 4))
    screen.blit(hp_num, (x + bar_width + 30, y - 2))

#draw sans base sprite
def draw_sans_sprite(screen, x=50, y=50):
    sans_img = pygame.image.load("assets/sans.png").convert_alpha()
    sans_img = pygame.transform.scale(sans_img, (80, 100))
    screen.blit(sans_img, (x, y))
