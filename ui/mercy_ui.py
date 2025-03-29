import pygame
from settings import *



def draw_mercy_screen(screen, heart_image, current_state):
    heart_x = 75
    heart_y = 155
    # Load your font (adjust the path/size as needed)
    font = pygame.font.Font("assets/fonts/health.ttf", 27)
    
    # Draw the heart at a fixed position
    screen.blit(heart_image, (heart_x, heart_y))
    
    # Allow text for check to be reset each time sans is checked
    if not hasattr(draw_mercy_screen, 'last_state'):
        draw_mercy_screen.last_state = None

    if current_state == STATE_SPARE:
        mercy_text = "* Spare"
        text_surface = font.render(mercy_text, False, WHITE)
        text_x = heart_x + heart_image.get_width() + 10
        text_y = heart_y - 7
        screen.blit(text_surface, (text_x, text_y))
