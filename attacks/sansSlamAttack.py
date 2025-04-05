import pygame
import random
from settings import *
from attacks.blue_movement import handle_blue_mode_movement
from ui.sans_ui import SansSpriteManager

'''
SansSlamAttack: Slam in a random direction one time, producing a gravity and slam effect.
Jump to escape the attack.
Meant to be used in an attack multiple times.
'''

class SansSlamAttack:
    def __init__(self, player, fight_box, direction=None, slam_speed=10, slam_duration=1500, 
                 slam_accel=0.4, jump_impulse=4, gravity_accel=0.6, attack_area=40, 
                 sans_sprite_manager=None):
        self.player = player
        self.fight_box = fight_box
        self.direction = direction if direction else random.choice(["left", "top", "bottom", "right"])
        self.slam_speed = slam_speed
        self.slam_duration = slam_duration  # Overall duration remains 1200 ms
        self.slam_accel = slam_accel
        self.jump_impulse = jump_impulse
        self.gravity_accel = gravity_accel
        self.on_ground = True
        self.pause_at_peak = False
        self.attack_area = attack_area
        self.inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)

        self.sans_sprite_manager = sans_sprite_manager
        # Flash duration is 25% of slam_duration
        self.flash_duration = int(0.25 * self.slam_duration)
        self.flashing = True

        self.start_time = pygame.time.get_ticks()
        self.done = False
        self.counter_impulse_applied = False

        self.direction_vectors = {
            "top": pygame.Vector2(0, -1),
            "bottom": pygame.Vector2(0, 1),
            "left": pygame.Vector2(-1, 0),
            "right": pygame.Vector2(1, 0)
        }
        self.dir_vector = self.direction_vectors[self.direction]

        if self.sans_sprite_manager:
            self.sans_sprite_manager.set("blue_eye")

        self.bone_img = pygame.image.load("assets/bone.webp").convert_alpha()
        self.bone_img = pygame.transform.scale(self.bone_img, (20, 10))
        if self.direction in ["top", "bottom"]:
            self.bone_img = pygame.transform.rotate(self.bone_img, 90)


        # Red line phase: from 15% to 35% of slam_duration, think thats good
        self.red_line_start = int(0.15 * self.slam_duration)
        self.red_line_end = int(0.35 * self.slam_duration)
        # Add a 300ms delay after the red line before the bones start animating, possibly shorten for harder attack?
        self.bone_delay = 300
        # Bone animation phase: 85% of slam_duration.
        self.bone_phase_start = self.red_line_end + self.bone_delay
        self.bone_phase_end = int(0.85 * self.slam_duration)
        
        # Divide the bone phase into in, hold, and out phases
        bone_phase_total = self.bone_phase_end - self.bone_phase_start 
        self.in_phase_duration = int(0.25 * bone_phase_total)   
        self.hold_phase_duration = int(0.5 * bone_phase_total)   
        self.out_phase_duration = bone_phase_total - (self.in_phase_duration + self.hold_phase_duration)  

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.flashing and self.sans_sprite_manager and now - self.start_time >= self.flash_duration:
            self.sans_sprite_manager.set("normal")
            self.flashing = False

        if self.direction == "top":
            handle_blue_mode_movement(self.player, keys, self.inner_box, "up")
        elif self.direction == "bottom":
            handle_blue_mode_movement(self.player, keys, self.inner_box, "down")
        elif self.direction == "left":
            handle_blue_mode_movement(self.player, keys, self.inner_box, "left")
        elif self.direction == "right":
            handle_blue_mode_movement(self.player, keys, self.inner_box, "right")

        if now - self.start_time >= self.slam_duration:
            self.done = True

    def draw(self, screen):
        elapsed = pygame.time.get_ticks() - self.start_time

        # Draw red line between red_line_start and red_line_end
        if elapsed > self.red_line_start:
            line_width = 5
            if self.direction in ["left", "right"]:
                x = (self.fight_box.left + self.attack_area) if self.direction == "left" else (self.fight_box.right - self.attack_area)
                if elapsed < self.red_line_end:
                    pygame.draw.line(screen, RED, (x, self.fight_box.top), (x, self.fight_box.bottom), line_width)
            else:
                y = (self.fight_box.top + self.attack_area) if self.direction == "top" else (self.fight_box.bottom - self.attack_area)
                if elapsed < self.red_line_end:
                    pygame.draw.line(screen, RED, (self.fight_box.left, y), (self.fight_box.right, y), line_width)

        # Draw the animated bones
        for bone_rect in self.get_active_bone_rects():
            screen.blit(self.bone_img, bone_rect)

    def get_active_bone_rects(self, sans_slam_margin=SANS_SLAM_MARGIN):
        elapsed = pygame.time.get_ticks() - self.start_time
        # Only animate bones during the bone phase.
        if elapsed < self.bone_phase_start or elapsed > self.bone_phase_end:
            return []

        bone_width = self.bone_img.get_width()
        bone_height = self.bone_img.get_height()
        anim_elapsed = elapsed - self.bone_phase_start

        # Determine progress based on the current phase.
        if anim_elapsed <= self.in_phase_duration:
            progress = anim_elapsed / self.in_phase_duration
        elif anim_elapsed <= (self.in_phase_duration + self.hold_phase_duration):
            progress = 1
        elif anim_elapsed <= (self.in_phase_duration + self.hold_phase_duration + self.out_phase_duration):
            progress = 1 - (anim_elapsed - self.in_phase_duration - self.hold_phase_duration) / self.out_phase_duration
        else:
            return []

        rects = []
        if self.direction in ["left", "right"]:
            x = (self.fight_box.left + self.attack_area) if self.direction == "left" else (self.fight_box.right - self.attack_area)
            if self.direction == "left":
                for fill_x in range(self.fight_box.left, x - sans_slam_margin, bone_width):
                    for fill_y in range(self.fight_box.top, self.fight_box.bottom, bone_height):
                        pos_x = self.fight_box.left + progress * (fill_x - self.fight_box.left) + sans_slam_margin
                        rects.append(pygame.Rect(int(pos_x) - bone_width // 2, fill_y, bone_width, bone_height))
            else:
                for fill_x in range(x + sans_slam_margin, self.fight_box.right, bone_width):
                    for fill_y in range(self.fight_box.top, self.fight_box.bottom, bone_height):
                        pos_x = self.fight_box.right + progress * (fill_x - self.fight_box.right)
                        rects.append(pygame.Rect(int(pos_x) - bone_width // 2, fill_y, bone_width, bone_height))
        else:
            y = (self.fight_box.top + self.attack_area) if self.direction == "top" else (self.fight_box.bottom - self.attack_area)
            if self.direction == "top":
                for fill_y in range(self.fight_box.top, y - sans_slam_margin, bone_height):
                    for fill_x in range(self.fight_box.left, self.fight_box.right, bone_width):
                        pos_y = self.fight_box.top + progress * (fill_y - self.fight_box.top) + sans_slam_margin
                        rects.append(pygame.Rect(fill_x, int(pos_y) - bone_height // 2, bone_width, bone_height))
            else:
                for fill_y in range(y, self.fight_box.bottom, bone_height):
                    for fill_x in range(self.fight_box.left, self.fight_box.right, bone_width):
                        pos_y = self.fight_box.bottom + progress * (fill_y - self.fight_box.bottom)
                        rects.append(pygame.Rect(fill_x, int(pos_y) - bone_height // 2, bone_width, bone_height))
        return rects

    def get_damage_rect(self):
        """
        Returns a rectangle representing the damage area.
        This area is defined by the edge of the fight box and the red line (attack_area)
        and is not drawn on the screen.
        """
        if self.direction == "left":
            return pygame.Rect(self.fight_box.left, self.fight_box.top, self.attack_area, self.fight_box.height)
        elif self.direction == "right":
            return pygame.Rect(self.fight_box.right - self.attack_area, self.fight_box.top, self.attack_area, self.fight_box.height)
        elif self.direction == "top":
            return pygame.Rect(self.fight_box.left, self.fight_box.top, self.fight_box.width, self.attack_area)
        elif self.direction == "bottom":
            return pygame.Rect(self.fight_box.left, self.fight_box.bottom - self.attack_area, self.fight_box.width, self.attack_area)

    def check_collision(self, rect):
        """
        Returns True if the player's rect collides with the damage area.
        The damage area is only active during the bone's active phase.
        """
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed < self.bone_phase_start or elapsed > self.bone_phase_end:
            return False
        damage_rect = self.get_damage_rect()
        return rect.colliderect(damage_rect)

    def is_done(self):
        return self.done
