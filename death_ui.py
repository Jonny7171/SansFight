import pygame
import time
from settings import WIDTH, HEIGHT, BLACK

def play_death_animation(screen, player_rect):
    # Load images
    heart = pygame.image.load("assets/heart.png").convert_alpha()
    shattered = pygame.image.load("assets/heart_shattered.png").convert_alpha()

    # Scale sprites - tested and working
    heart = pygame.transform.scale(heart, (16, 16))
    shattered = pygame.transform.scale(shattered, (54, 68))
    shattered_rect = shattered.get_rect(center=player_rect.center)

    # Create fullscreen black overlay
    black_overlay = pygame.Surface((WIDTH, HEIGHT))
    black_overlay.fill(BLACK)

    # Fade to black
    for alpha in range(0, 256, 8):
        black_overlay.set_alpha(alpha)
        screen.fill(BLACK)
        screen.blit(heart, player_rect)
        screen.blit(black_overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    # Show shattered heart at the same position as the original
    screen.fill(BLACK)
    screen.blit(shattered, shattered_rect)
    pygame.display.flip()
    pygame.time.delay(1000)

    # Final pause before terminating
    pygame.time.delay(500)