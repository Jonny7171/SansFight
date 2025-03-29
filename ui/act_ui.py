import pygame
from settings import *



def draw_act_screen(screen, heart_image, current_state):
    heart_x = HEART_X
    heart_y = HEART_Y
    # Load your font (adjust the path/size as needed)
    font = pygame.font.Font("assets/fonts/health.ttf", 27)
    
    # Draw the heart at a fixed position
    screen.blit(heart_image, (heart_x, heart_y))
    
    # Allow text for check to be reset each time sans is checked
    if not hasattr(draw_act_screen, 'last_state'):
        draw_act_screen.last_state = None

    if current_state == STATE_ACT_RESPONSE and draw_act_screen.last_state != STATE_ACT_RESPONSE:
        draw_act_screen.start_time = pygame.time.get_ticks()

    draw_act_screen.last_state = current_state

    if current_state == STATE_ACT:
        act_text = "* Sans"
        text_surface = font.render(act_text, False, WHITE)
        text_x = heart_x + heart_image.get_width() + 10
        text_y = DIALOGUE_Y
        screen.blit(text_surface, (text_x, text_y))
    elif current_state == STATE_ACT_SANS:
        text_surface = font.render("* Check", False, WHITE)
        screen.blit(text_surface, (heart_x + 26, heart_y - 7))
    
    #unique- I want text to appear over time
    elif current_state == STATE_ACT_RESPONSE:
    # Initialize persistent start time for typewriter effect
        if not hasattr(draw_act_screen, 'start_time'):
            draw_act_screen.start_time = pygame.time.get_ticks()
        elapsed = (pygame.time.get_ticks() - draw_act_screen.start_time) / 1000.0
        letters_per_second = 20  # Adjust speed as needed
        total_chars = int(elapsed * letters_per_second)
        line1 = "* SANS 1 ATK 1 DEF"
        line2 = "* The easiest enemy."
        line3 = "* Can only deal 1 damage."
        lines = [line1, line2, line3]

        # Build the rendered lines by revealing letters continuously
        rendered_lines = []
        remaining = total_chars
        for line in lines:
            if remaining >= len(line):
                rendered_lines.append(line)
                remaining -= len(line)
            elif remaining > 0:
                rendered_lines.append(line[:remaining])
                remaining = 0
            else:
                rendered_lines.append("")

        # Render each line
        text_surface = font.render(rendered_lines[0], False, WHITE)
        screen.blit(text_surface, (heart_x + 26, heart_y - 7))

        text_surface = font.render(rendered_lines[1], False, WHITE)
        screen.blit(text_surface, (heart_x + 26, heart_y + 20))

        text_surface = font.render(rendered_lines[2], False, WHITE)
        screen.blit(text_surface, (heart_x + 26, heart_y + 47))
