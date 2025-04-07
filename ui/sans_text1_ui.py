import pygame
from settings import *
from ui.fight_ui import draw_fight_box, get_fight_box
from ui.sans_ui import SansSpriteManager

# Globals to track the typing state and dialogue pagination
typing_index = 0        # how many characters are currently revealed
last_update_time = 0    # last time (in ms) we added a character
typing_speed = 50       # how many ms between characters (the smaller, the faster)
current_page = 0        # current dialogue page index

def reset_dialogue():
    """
    Call this whenever you want to restart the typing effect 
    from the beginning for a new line of text or dialogue page.
    """
    global typing_index, last_update_time
    typing_index = 0
    last_update_time = 0

def draw_sans_dialogue(screen, full_text, current_page=0, sans_sprite_manager=None):
    """
    Draws the Sans dialogue bubble with a typewriter effect and word-wrapping.
    The text is not repositioned; it will be drawn at the same location you have set.
    If full_text is a list, it will display the current page based on current_page.
    :param screen: The pygame display surface
    :param full_text: The full text (string or list of strings) to be typed out
    """
    global typing_index, last_update_time

    # If full_text is a list, use the text from the current page.
    if isinstance(full_text, list):
        page_text = full_text[current_page]
        if page_text == 'it was a "slice" try':
            if sans_sprite_manager:
                sans_sprite_manager.set("wink")
    else:
        page_text = full_text

    # 1) Load the bubble image
    bubble_img = pygame.image.load("assets/textbox.png").convert_alpha()
    bubble_img = pygame.transform.scale(bubble_img, (300, 120))
    bubble_rect = bubble_img.get_rect()
    bubble_rect.topleft = (320, 30)

    # 2) Blit the bubble image
    screen.blit(bubble_img, bubble_rect)

    # 3) Update the typing_index if enough time has passed
    current_time = pygame.time.get_ticks()
    if typing_index < len(page_text):
        if current_time - last_update_time >= typing_speed:
            typing_index += 1
            last_update_time = current_time

    # 4) Prepare the substring that should be shown so far
    displayed_text = page_text[:typing_index]

    # 5) Word-wrap the displayed_text without splitting words
    font = pygame.font.SysFont("comicsans", 16)
    max_width = 180  # Maximum pixel width allowed per line inside the bubble

    # Split the typed substring into words
    words = displayed_text.split()

    lines = []
    current_line = ""

    for word in words:
        test_line = (current_line + " " + word).strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # 6) Render each line inside the bubble at the specified text location.
    text_x = bubble_rect.x + 60
    text_y = bubble_rect.y + 20
    line_height = font.get_height() + 2

    for line in lines:
        line_surface = font.render(line, True, (0, 0, 0))
        screen.blit(line_surface, (text_x, text_y))
        text_y += line_height
