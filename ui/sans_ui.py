import pygame
from settings import *

def load_sans_assets():
    """Load Sans sprites and return them in a dictionary."""
    sans_normal = pygame.image.load("assets/sans.png").convert_alpha()
    #sans_angry  = pygame.image.load("assets/sans_angry.png").convert_alpha()
    
    # Optionally, scale the sprites if needed:
    sans_normal = pygame.transform.scale(sans_normal, (100, 100))
    #sans_angry  = pygame.transform.scale(sans_angry, (100, 100))
    
    return {
        "normal": sans_normal,
        #"angry": sans_angry,
    }

def draw_sans(screen, sans_sprite, fight_box=None):
    x = WIDTH // 2 - sans_sprite.get_width() // 2
    y = 25
    screen.blit(sans_sprite, (x, y))