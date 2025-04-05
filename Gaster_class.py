import pygame
import math
from settings import *

class GasterBlaster:
    def __init__(self, start_pos, target_pos, open_delay=1000, fire_delay=1000, scale=0.5,
                 orientation=None):
        self.position = pygame.Vector2(start_pos)
        self.move_target = pygame.Vector2(target_pos)
        self.original_aim = pygame.Vector2(target_pos)
        self.speed = 7
        self.arrived = False
        self.open_delay = open_delay
        self.fire_delay = fire_delay
        self.spawn_time = pygame.time.get_ticks()
        self.scale = scale
        self.sound_effect = pygame.mixer.Sound("sounds/gaster_blaster.wav")
        # Set a delay (in ms) before playing the sound
        self.sound_delay = 150

        self.laser_duration = 1000
        self.fade_out_duration = 600

        # Load images
        closed_img = pygame.image.load("assets/gaster_blaster.png").convert_alpha()
        open_img = pygame.image.load("assets/gaster_blaster_open.png").convert_alpha()

        # Scale images
        w_closed = int(closed_img.get_width() * scale)
        h_closed = int(closed_img.get_height() * scale)
        w_open = int(open_img.get_width() * scale)
        h_open = int(open_img.get_height() * scale)

        self.closed_image_raw = pygame.transform.scale(closed_img, (w_closed, h_closed))
        self.open_image_raw = pygame.transform.scale(open_img, (w_open, h_open))

        # Calculate initial direction for laser
        initial_direction = self.move_target - self.position
        if initial_direction.length() == 0:
            self.initial_direction = pygame.Vector2(1, 0)
        else:
            self.initial_direction = initial_direction.normalize()

        # Set initial orientation
        if orientation is None:
            direction = self.move_target - self.position
            self.angle = math.degrees(math.atan2(-direction.y, direction.x))
        else:
            self.angle = orientation + 90

        # Rotate images using the corrected angle
        self.closed_image = pygame.transform.rotate(self.closed_image_raw, self.angle)
        self.open_image = pygame.transform.rotate(self.open_image_raw, self.angle)
        self.image = self.closed_image

        self.alpha = 255
        self.rect = self.image.get_rect(center=self.position)
        self.mouth_opened = False
        self.fired = False
        self.laser_beam = None
        self.fire_time = None

    def update(self):
        now = pygame.time.get_ticks()

        # 1. Move toward the target
        if not self.arrived:
            direction = self.move_target - self.position
            # Only play the sound after the sound delay has passed
            if (not self.arrived and not hasattr(self, 'sound_played') 
                    and now - self.spawn_time >= self.sound_delay):
                self.sound_effect.play()
                self.sound_played = True
            if direction.length() > self.speed:
                direction = direction.normalize() * self.speed
                self.position += direction
            else:
                self.position = self.move_target
                self.arrived = True

        # 2. Open mouth after delay
        if not self.mouth_opened and now - self.spawn_time >= self.open_delay:
            self.mouth_opened = True

        # 3. Fire laser after delay using initial direction
        if not self.fired and now - self.spawn_time >= self.fire_delay:
            self.fired = True
            self.fire_time = now
            beam_end = self.position + self.initial_direction * 2000
            self.laser_beam = (self.position, beam_end)

        # 4. Handle laser duration and fade out
        if self.fired:
            elapsed_since_fire = now - self.fire_time
            if elapsed_since_fire > self.laser_duration:
                fade_time = elapsed_since_fire - self.laser_duration
                fade_ratio = fade_time / self.fade_out_duration
                self.alpha = max(0, 255 * (1 - fade_ratio))
                if fade_ratio >= 1:
                    self.laser_beam = None

        # Update sprite image
        base_image = self.open_image_raw if self.mouth_opened else self.closed_image_raw
        rotated_image = pygame.transform.rotate(base_image, self.angle)
        self.rect = rotated_image.get_rect(center=self.position)
        
        if self.alpha < 255:
            rotated_image = rotated_image.copy()
            rotated_image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.image = rotated_image

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.laser_beam:
            laser_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            laser_color = (255, 255, 255, self.alpha)
            pygame.draw.line(laser_surface, laser_color, self.laser_beam[0], self.laser_beam[1], 10)
            screen.blit(laser_surface, (0, 0))

    def is_firing(self):
        return self.fired and self.laser_beam is not None

    def is_faded_out(self):
        return self.alpha <= 0