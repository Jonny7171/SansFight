import pygame
from settings import *

class Player:
    @staticmethod
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
        self.hp = MAX_HP
        self.invincible = False
        self.invincibility_timer = INVINCIBILITY_DURATION
        self.pause_at_peak = False
        self.peak_pause_start = 0
        self.peak_pause_duration = 70  # milliseconds

        # Blue mode properties
        self.blue_mode = False
        self.vel_y = 0
        self.on_ground = True  # assume starting on ground

    def handle_movement(self, keys, bounds_rect):
        if not self.blue_mode:
            # Red heart: free movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= HEART_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += HEART_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= HEART_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += HEART_SPEED
        else:
            # Blue heart: horizontal movement and jumping with gravity.
            # Horizontal movement:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= HEART_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += HEART_SPEED

            # Jump
            if self.on_ground and (keys[pygame.K_UP] or keys[pygame.K_w]):
                self.jump_start_time = pygame.time.get_ticks()  # Record the time jump started
                self.vel_y = -4  # Initial jump strength
                self.on_ground = False
                jumped_flag = True

            # Check if the jump key is still being held and adjust velocity.
            if not self.on_ground and (keys[pygame.K_UP] or keys[pygame.K_w]):
                jump_duration = pygame.time.get_ticks() - self.jump_start_time
                if jump_duration < 200:  # Allow stronger jump for up to 200ms
                    self.vel_y -= 0.7  # Incremental boost, not set on it yet

            if not self.on_ground and self.vel_y <= 0 and self.vel_y >= -0.5 and not self.pause_at_peak:
                    self.pause_at_peak = True
                    self.peak_pause_start = pygame.time.get_ticks()

            
            if self.pause_at_peak:
                now = pygame.time.get_ticks()
                if now - self.peak_pause_start >= self.peak_pause_duration:
                    self.pause_at_peak = False  # end the pause
                else:
                    return  # skip gravity update this frame
            # gravity effect
            if not self.pause_at_peak:
                self.vel_y += 0.5  # gravity constan, can be adjusted for feel
                self.rect.y += int(self.vel_y)

            # Check if landed
            if self.rect.bottom > bounds_rect.bottom:
                self.rect.bottom = bounds_rect.bottom
                self.vel_y = 0
                self.on_ground = True

        # Clamp the player inside fight area
        self.rect.clamp_ip(bounds_rect)

    def take_damage(self, amount):
        if not self.invincible:
            self.hp -= amount
            self.invincible = False
            self.invincibility_timer = INVINCIBILITY_DURATION
            #print(f"Player took {amount} damage! HP: {self.hp}")

    def update_invincibility(self):
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_color_blue(self):
        self.image = self.blue_image

    def set_color_red(self):
        self.image = self.red_image

    def set_blue_mode(self, mode):
        """
        Turn blue mode on or off.
        When enabled, the player uses blue-mode physics (gravity and jumping).
        Also, switch the sprite to the blue variant.
        """
        self.blue_mode = mode
        if mode:
            self.set_color_blue()
            self.vel_y = 0
            self.on_ground = True
        else:
            self.set_color_red()