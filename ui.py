import pygame
from settings import WIDTH, HEIGHT, WHITE

# Get the position and size of the fight box
def get_fight_box():
    box_width = 300
    box_height = 200
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    return pygame.Rect(box_x, box_y, box_width, box_height)

# Draw the fight box
def draw_fight_box(screen, fight_box):
    pygame.draw.rect(screen, WHITE, fight_box, width=2)