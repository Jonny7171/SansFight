import pygame
from settings import *



def draw_item_screen(screen, heart_image, current_state, events, player):
    # Load your font (adjust the path/size as needed)
    font = pygame.font.Font("assets/fonts/health.ttf", 27)
    
    # Keep track of our last state for potential logic if needed
    if not hasattr(draw_item_screen, 'last_state'):
        draw_item_screen.last_state = None

    # When switching into the ITEM state, reset the timestamp
    if current_state == STATE_ITEM and draw_item_screen.last_state != STATE_ITEM:
        draw_item_screen.time_entered_item = pygame.time.get_ticks()
        print("Entered ITEM state")
        draw_item_screen.selected_index = 0

    # Update last_state for next frame
    draw_item_screen.last_state = current_state

    now = pygame.time.get_ticks()
    ignore_threshold = 250

    # If we are in the ITEM state, handle the menu logic
    if current_state == STATE_ITEM:
        if not hasattr(draw_item_screen, 'options'):
            draw_item_screen.options = ["Pie", "I. Noodels", "Pancakes:P", "L. Hero"]
        if not hasattr(draw_item_screen, 'selected_index'):
            draw_item_screen.selected_index = 0

        # Convenience reference
        options = draw_item_screen.options

        # Menu navigation and selection
        for event in events:
            # Ignore events if within the debounce threshold
            if now - draw_item_screen.time_entered_item < ignore_threshold:
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    draw_item_screen.selected_index = (draw_item_screen.selected_index - 2) % len(options)
                elif event.key == pygame.K_s:
                    draw_item_screen.selected_index = (draw_item_screen.selected_index + 2) % len(options)
                elif event.key == pygame.K_a:
                    draw_item_screen.selected_index = (draw_item_screen.selected_index - 1) % len(options)
                elif event.key == pygame.K_d:
                    draw_item_screen.selected_index = (draw_item_screen.selected_index + 1) % len(options)
                # Consume food and remove the selected option
                elif event.key == pygame.K_RETURN:
                    if len(options) > 0:
                        selected_option = options[draw_item_screen.selected_index]
                        if selected_option == "Pie":
                            player.hp = min(player.hp + 90, MAX_HP)
                            print("Pie consumed!")
                        elif selected_option == "I. Noodels":
                            player.hp = min(player.hp + 90, MAX_HP)
                            print("Instant Noodles consumed!")
                        elif selected_option == "Pancakes:P":
                            player.hp = min(player.hp + 60, MAX_HP)
                            print("Pancakes consumed!")
                        elif selected_option == "L. Hero":
                            player.hp = min(player.hp + 50, MAX_HP)
                        options.pop(draw_item_screen.selected_index)
                        draw_item_screen.selected_index = min(
                            draw_item_screen.selected_index, 
                            len(options) - 1
                        )
                        if len(options) == 0:
                            draw_item_screen.selected_index = 0

        # Coordinates for the top-left (index 0) option
        option1_x = 101
        option1_y = 148

        heart_x = 0
        heart_y = 0

        # Only draw if we still have options
        if len(options) > 0:
            for i, option in enumerate(options):
                # 2x2 grid layout:
                x = option1_x + (i % 2) * 240
                y = option1_y + (i // 2) * 65

                if i == draw_item_screen.selected_index:
                    heart_x = x - 26
                    heart_y = y + 2

                option_text = font.render(option, True, WHITE)
                screen.blit(option_text, (x, y))

            screen.blit(heart_image, (heart_x, heart_y))
        else:
            no_items_text = font.render("No more items!", True, WHITE)
            screen.blit(no_items_text, (option1_x, option1_y))