import pygame
from settings import HEART_SPEED

class Player:
    @staticmethod
    # Create a blue variant of the heart image for certain attacks
    def create_blue_variant(surface):
        new_surface = surface.copy()
        new_surface.fill((0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
        new_surface.fill((0, 0, 150, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return new_surface

    def __init__(self, image_path, start_pos):
        # Load heart image and scale it to 16x16
        base_image = pygame.image.load(image_path).convert_alpha()
        base_image = pygame.transform.scale(base_image, (16, 16))
        self.red_image = base_image
        # Create the blue variant
        self.blue_image = self.create_blue_variant(base_image)
        self.image = self.red_image
        self.rect = self.image.get_rect(center=start_pos)

    def handle_movement(self, keys, bounds_rect):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= HEART_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += HEART_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= HEART_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += HEART_SPEED

        # Keep the heart inside the fight box
        self.rect.clamp_ip(bounds_rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_color_blue(self):
        self.image = self.blue_image

    def set_color_red(self):
        self.image = self.red_image