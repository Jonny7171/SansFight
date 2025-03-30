import pygame
import math

class GasterBlaster:
    def __init__(self, start_pos, target_pos, open_delay=400, fire_delay=700, scale=0.5):
        """
        start_pos: where it spawns (off-screen)
        target_pos: the position it will move toward (usually near player)
        open_delay: ms before the mouth opens
        fire_delay: ms before firing the laser
        scale: scale factor for the sprite size
        """
        self.position = pygame.Vector2(start_pos)
        self.move_target = pygame.Vector2(target_pos)  # Where we move to
        self.original_aim = pygame.Vector2(target_pos) # We aim at this for the laser
        self.speed = 5  # Movement speed toward move_target
        self.arrived = False  # Whether we've stopped moving

        self.open_delay = open_delay
        self.fire_delay = fire_delay
        self.spawn_time = pygame.time.get_ticks()
        self.scale = scale

        self.laser_duration = 1000  # Laser visible for 1 second
        self.fade_out_duration = 800  # Fade out over 0.8 seconds

        # Load images
        closed_img = pygame.image.load("assets/gaster_blaster.png").convert_alpha()
        open_img = pygame.image.load("assets/gaster_blaster_open.png").convert_alpha()

        # Scale them
        w_closed = int(closed_img.get_width() * scale)
        h_closed = int(closed_img.get_height() * scale)
        w_open = int(open_img.get_width() * scale)
        h_open = int(open_img.get_height() * scale)

        self.closed_image_raw = pygame.transform.scale(closed_img, (w_closed, h_closed))
        self.open_image_raw = pygame.transform.scale(open_img, (w_open, h_open))

        # Angle from start_pos to move_target (for sprite orientation).
        direction = self.move_target - self.position
        self.angle = math.degrees(math.atan2(direction.y, direction.x))


        # Rotate the images
        self.closed_image = pygame.transform.rotate(self.closed_image_raw, self.angle)
        self.open_image = pygame.transform.rotate(self.open_image_raw, self.angle)
        self.image = self.closed_image

        # Use an alpha channel for fade-out
        self.alpha = 255

        self.rect = self.image.get_rect(center=self.position)
        self.mouth_opened = False
        self.fired = False
        self.laser_beam = None
        self.fire_time = None  # When we actually fired

    def update(self):
        now = pygame.time.get_ticks()

        # 1. Move in until we arrive
        if not self.arrived:
            direction = self.move_target - self.position
            if direction.length() > self.speed:
                direction = direction.normalize() * self.speed
                self.position += direction
            else:
                # We’ve arrived (or very close)
                self.position = self.move_target
                self.arrived = True

        # 2. Open mouth after open_delay
        if not self.mouth_opened and now - self.spawn_time >= self.open_delay:
            self.mouth_opened = True
            self.image = self.open_image

        # 3. Fire laser after fire_delay
        if not self.fired and now - self.spawn_time >= self.fire_delay:
            self.fired = True
            self.fire_time = now
            # Aim at the original_aim
            # Angle for beam is from self.position to self.original_aim
            direction = self.original_aim - self.position
            if direction.length() != 0:
                direction = direction.normalize()
# Extend it, say, 2000 pixels from the blaster, so it crosses the entire screen.
            beam_end = self.position + direction * 2000
            self.laser_beam = (self.position, beam_end)

        # 4. Turn off laser after laser_duration
        if self.fired and now - self.fire_time >= self.laser_duration:
            self.laser_beam = None  # Laser disappears

        # 5. Fade out after laser is gone
        #    We'll start fading once the laser is gone
        if self.fire_time and (now - self.fire_time) > self.laser_duration:
            # Time since laser ended
            fade_time = now - (self.fire_time + self.laser_duration)
            fade_ratio = fade_time / self.fade_out_duration
            if fade_ratio >= 1:
                self.alpha = 0  # fully transparent
            else:
                self.alpha = 255 * (1 - fade_ratio)

        # Update alpha channel on the image
        # Make a copy so we don’t permanently alter the original
        if self.alpha < 255:
            temp_image = self.image.copy()
            temp_image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = temp_image

        # Update rect
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Draw the laser line if it's active
        if self.laser_beam:
            pygame.draw.line(
                screen,
                (255, 0, 0),
                self.laser_beam[0],
                self.laser_beam[1],
                3
            )

    def is_firing(self):
        return self.fired and self.laser_beam is not None

    def is_faded_out(self):
        return self.alpha <= 0
