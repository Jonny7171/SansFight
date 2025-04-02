import pygame
import random
from settings import *
from attacks.blue_movement import handle_blue_mode_movement

class SansSlamAttack:
    def __init__(self, player, fight_box, direction=None, slam_speed=10, slam_duration=3000, slam_accel=0.4, jump_impulse=4, gravity_accel=0.4, attack_area=40):
        self.player = player
        self.fight_box = fight_box
        self.direction = direction if direction else random.choice(["left", "top", "bottom", "right"])
        self.slam_speed = slam_speed
        self.slam_duration = slam_duration
        self.slam_accel = slam_accel
        self.jump_impulse = jump_impulse
        self.gravity_accel = gravity_accel
        self.on_ground = True
        self.pause_at_peak = False
        self.attack_area = attack_area
        self.inner_box = fight_box.inflate(-MARGIN * 2, -MARGIN * 2)

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

        self.bone_img = pygame.image.load("assets/bone.webp").convert_alpha()
        self.bone_img = pygame.transform.scale(self.bone_img, (20, 10))
        
        if self.direction in ["top", "bottom"]:
            self.bone_img = pygame.transform.rotate(self.bone_img, 90)

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
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
        
        # Red line appears after 300ms
        if elapsed > 300:
            line_width = 5
            
            if self.direction in ["left", "right"]:
                x = (self.fight_box.left + self.attack_area) if self.direction == "left" else (self.fight_box.right - self.attack_area)
                if elapsed < 700:  # Show red line for 400ms (300ms + 400ms = 700ms)
                    pygame.draw.line(screen, RED, (x, self.fight_box.top), (x, self.fight_box.bottom), line_width)
                
                # Bones start 400ms after red line (700ms total)
                if 700 < elapsed <= 1500:  # Total animation duration 800ms (700-1500)
                    bone_width = self.bone_img.get_width()
                    bone_height = self.bone_img.get_height()
                    anim_elapsed = elapsed - 700
                    
                    # Animation phases:
                    # 200ms in (0-200)
                    # 400ms hold (200-600)
                    # 200ms out (600-800)
                    if anim_elapsed <= 200:
                        progress = anim_elapsed / 200
                    elif anim_elapsed <= 600:  # 400ms hold (reduced by 50ms)
                        progress = 1
                    elif anim_elapsed <= 800:
                        progress = 1 - (anim_elapsed - 600) / 200
                    else:
                        return
                    
                    if self.direction == "left":
                        for fill_x in range(self.fight_box.left, x - SANS_SLAM_MARGIN, bone_width):
                            for fill_y in range(self.fight_box.top, self.fight_box.bottom, bone_height):
                                pos_x = self.fight_box.left + progress * (fill_x - self.fight_box.left) + SANS_SLAM_MARGIN
                                screen.blit(self.bone_img, (int(pos_x) - bone_width // 2, fill_y))
                    else:  # right
                        for fill_x in range(x + SANS_SLAM_MARGIN, self.fight_box.right, bone_width):
                            for fill_y in range(self.fight_box.top, self.fight_box.bottom, bone_height):
                                pos_x = self.fight_box.right + progress * (fill_x - self.fight_box.right)
                                screen.blit(self.bone_img, (int(pos_x) - bone_width // 2, fill_y))
            
            else:  # top or bottom
                y = (self.fight_box.top + self.attack_area) if self.direction == "top" else (self.fight_box.bottom - self.attack_area)
                if elapsed < 700:  # Show red line for 400ms
                    pygame.draw.line(screen, RED, (self.fight_box.left, y), (self.fight_box.right, y), line_width)
                
                # Bones animation starts 400ms after red line (700ms total)
                if 700 < elapsed <= 1500:
                    bone_width = self.bone_img.get_width()
                    bone_height = self.bone_img.get_height()
                    anim_elapsed = elapsed - 700
                    
                    if anim_elapsed <= 200:
                        progress = anim_elapsed / 200
                    elif anim_elapsed <= 600:
                        progress = 1
                    elif anim_elapsed <= 800:
                        progress = 1 - (anim_elapsed - 600) / 200
                    else:
                        return
                    
                    if self.direction == "top":
                        for fill_y in range(self.fight_box.top, y - SANS_SLAM_MARGIN, bone_height):
                            for fill_x in range(self.fight_box.left, self.fight_box.right, bone_width):
                                pos_y = self.fight_box.top + progress * (fill_y - self.fight_box.top) + SANS_SLAM_MARGIN
                                screen.blit(self.bone_img, (fill_x, int(pos_y) - bone_height // 2))
                    else:  # bottom
                        for fill_y in range(y, self.fight_box.bottom, bone_height):
                            for fill_x in range(self.fight_box.left, self.fight_box.right, bone_width):
                                pos_y = self.fight_box.bottom + progress * (fill_y - self.fight_box.bottom) + SANS_SLAM_MARGIN
                                screen.blit(self.bone_img, (fill_x, int(pos_y) - bone_height // 2))

    def is_done(self):
        return self.done

    def check_collision(self, rect):
        return False