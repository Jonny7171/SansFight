import pygame
from settings import *

# ACT state variables:
act_substate = "MAIN"   # starts as "MAIN" (displaying "* Sans")
act_done = False        # becomes True when user confirms "CHECK"

def update_act_state(events):
    global act_substate, act_done
    for event in events:
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            if act_substate == "MAIN":
                act_substate = "CHECK"
            elif act_substate == "CHECK":
                act_done = True

def draw_act_screen(screen, heart_image, current_state):
    heart_x = 75
    heart_y = 155
    # Load your font (adjust the path/size as needed)
    font = pygame.font.Font("assets/fonts/health.ttf", 27)
    
    # Draw the heart at a fixed position
    screen.blit(heart_image, (heart_x, heart_y))
    
    if current_state == STATE_ACT:
        act_text = "* Sans"
        text_surface = font.render(act_text, False, WHITE)
        text_x = heart_x + heart_image.get_width() + 10
        text_y = heart_y - 7
        screen.blit(text_surface, (text_x, text_y))
    elif current_state == STATE_ACT_SANS:
        text_surface = font.render("* Check", False, WHITE)
        screen.blit(text_surface, (heart_x + 26, heart_y - 7))