import pygame
from settings import *

def handle_blue_mode_movement(self, keys, bounds_rect, gravity_direction="down"):
    # Note: This function only handles blue_mode logic.
    if gravity_direction == "down":
        # Horizontal movement stays on the x-axis.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= HEART_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += HEART_SPEED

        # Jump is triggered by UP.
        if self.on_ground and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.jump_start_time = pygame.time.get_ticks()
            self.vel_y = -4  # jump upward
            self.on_ground = False
            jumped_flag = True

        if not self.on_ground and (keys[pygame.K_UP] or keys[pygame.K_w]):
            jump_duration = pygame.time.get_ticks() - self.jump_start_time
            if jump_duration < 200:
                self.vel_y -= 0.7

        if not self.on_ground and self.vel_y <= 0 and self.vel_y >= -0.5 and not self.pause_at_peak:
            self.pause_at_peak = True
            self.peak_pause_start = pygame.time.get_ticks()

        if self.pause_at_peak:
            now = pygame.time.get_ticks()
            if now - self.peak_pause_start >= self.peak_pause_duration:
                self.pause_at_peak = False
            else:
                return

        # Gravity effect (accelerates downward).
        self.vel_y += 0.5
        self.rect.y += int(self.vel_y)

        # Landing check.
        if self.rect.bottom > bounds_rect.bottom:
            self.rect.bottom = bounds_rect.bottom
            self.vel_y = 0
            self.on_ground = True

    elif gravity_direction == "up":
        print(gravity_direction, "Here")
        # Horizontal movement still on the x-axis.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= HEART_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += HEART_SPEED

        # Jump is now triggered by DOWN (.
        if self.on_ground and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.jump_start_time = pygame.time.get_ticks()
            self.vel_y = 4  # jump downward (opposite to upward gravity)
            self.on_ground = False
            jumped_flag = True

        if not self.on_ground and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            jump_duration = pygame.time.get_ticks() - self.jump_start_time
            if jump_duration < 200:
                self.vel_y += 0.7

        if not self.on_ground and self.vel_y >= 0 and self.vel_y <= 0.5 and not self.pause_at_peak:
            self.pause_at_peak = True
            self.peak_pause_start = pygame.time.get_ticks()

        if self.pause_at_peak:
            now = pygame.time.get_ticks()
            if now - self.peak_pause_start >= self.peak_pause_duration:
                self.pause_at_peak = False
            else:
                return

        # Gravity effect (accelerates upward, so subtract from vel_y).
        self.vel_y += -0.5
        self.rect.y += int(self.vel_y)

        # Landing check for upward gravity.
        if self.rect.top < bounds_rect.top:
            self.rect.top = bounds_rect.top
            self.vel_y = 0
            self.on_ground = True

    elif gravity_direction == "left":
        # For left gravity, movement is along the vertical axis.
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= HEART_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += HEART_SPEED

        # Jump is now triggered by RIGHT (jumping opposite to leftward gravity).
        if self.on_ground and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.jump_start_time = pygame.time.get_ticks()
            self.vel_x = 4  # jump to the right
            self.on_ground = False
            jumped_flag = True

        if not self.on_ground and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            jump_duration = pygame.time.get_ticks() - self.jump_start_time
            if jump_duration < 200:
                self.vel_x += 0.7

        if not self.on_ground and self.vel_x >= 0 and self.vel_x <= 0.5 and not self.pause_at_peak:
            self.pause_at_peak = True
            self.peak_pause_start = pygame.time.get_ticks()

        if self.pause_at_peak:
            now = pygame.time.get_ticks()
            if now - self.peak_pause_start >= self.peak_pause_duration:
                self.pause_at_peak = False
            else:
                return

        # Gravity effect (accelerates leftward).
        self.vel_x += -0.5
        self.rect.x += int(self.vel_x)

        # Landing check.
        if self.rect.left < bounds_rect.left:
            self.rect.left = bounds_rect.left
            self.vel_x = 0
            self.on_ground = True

    elif gravity_direction == "right":
        # For right gravity, movement is along the vertical axis.
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= HEART_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += HEART_SPEED

        # Jump is triggered by LEFT (jumping opposite to rightward gravity).
        if self.on_ground and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.jump_start_time = pygame.time.get_ticks()
            self.vel_x = -4  # jump to the left
            self.on_ground = False
            jumped_flag = True

        if not self.on_ground and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            jump_duration = pygame.time.get_ticks() - self.jump_start_time
            if jump_duration < 200:
                self.vel_x -= 0.7

        if not self.on_ground and self.vel_x <= 0 and self.vel_x >= -0.5 and not self.pause_at_peak:
            self.pause_at_peak = True
            self.peak_pause_start = pygame.time.get_ticks()

        if self.pause_at_peak:
            now = pygame.time.get_ticks()
            if now - self.peak_pause_start >= self.peak_pause_duration:
                self.pause_at_peak = False
            else:
                return

        # Gravity effect (accelerates rightward).
        self.vel_x += 0.5
        self.rect.x += int(self.vel_x)

        # Landing check.
        if self.rect.right > bounds_rect.right:
            self.rect.right = bounds_rect.right
            self.vel_x = 0
            self.on_ground = True

    # Finally, ensure the heart stays within the fight area.
    self.rect.clamp_ip(bounds_rect)

