import pygame
import random
from settings import *
from attacks.blue_movement import handle_blue_mode_movement

class SansSlamAttack:
    def __init__(self, player, fight_box, direction=None, slam_speed=10, slam_duration=3000, slam_accel=0.4, jump_impulse=4, gravity_accel=0.4, attack_area = 40):
        """
        Initialize the slam attack.
        
        Parameters:
          player: The player (heart) object.
          fight_box: pygame.Rect representing the boundaries of the fight area.
          direction: One of "top", "bottom", "left", "right". If None, random.
          slam_speed: Initial speed of the slam.
          slam_duration: Duration of the slam (in milliseconds).
          slam_accel: Acceleration in the slam direction.
          jump_impulse: Impulse applied when countering.
          gravity_accel: Downward acceleration after countering.
        """
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

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        # Counter input detection
        counter_pressed = False
        if(self.direction == "top"):
            handle_blue_mode_movement(self.player, keys, self.fight_box,"up")
        elif(self.direction == "bottom"):
            handle_blue_mode_movement(self.player, keys, self.fight_box,"down")
        elif(self.direction == "left"):
            handle_blue_mode_movement(self.player, keys, self.fight_box,"left")
        elif(self.direction == "right"):
            handle_blue_mode_movement(self.player, keys, self.fight_box,"right")
        
        """
        if counter_pressed and not self.counter_impulse_applied:
            # Apply impulse in the OPPOSITE direction of the slam
            self.velocity = -self.dir_vector * self.jump_impulse
            self.counter_impulse_applied = True

        # Update position
        self.player.rect.x += int(self.velocity.x)
        self.player.rect.y += int(self.velocity.y)
        self.player.rect.clamp_ip(self.fight_box)
        """

        # Attack duration check
        if now - self.start_time >= self.slam_duration:
            self.done = True

        
    def draw(self, screen):
        # Existing fade effect
        effect_radius = 50
        effect_surface = pygame.Surface((effect_radius*2, effect_radius*2), pygame.SRCALPHA)
        elapsed = pygame.time.get_ticks() - self.start_time
        screen.blit(effect_surface, (self.player.rect.centerx - effect_radius, self.player.rect.centery - effect_radius))

        # Red line and bones after delay
        if elapsed > 500:  # 0.5 seconds delay CAN BE CHANGEd
            red = (255, 0, 0)
            line_width = 5
            if self.direction in ["left", "right"]:
                x = (self.fight_box.left + self.attack_area)  if self.direction == "left" else (self.fight_box.right - self.attack_area)
                pygame.draw.line(screen, red, (x, self.fight_box.top), (x, self.fight_box.bottom), line_width)
                # Draw bones vertically
                if elapsed > 700: #CAN BE CHANGED
                    bone_height = self.bone_img.get_height()
                    for y in range(self.fight_box.top, self.fight_box.bottom, bone_height):
                        screen.blit(self.bone_img, (x - self.bone_img.get_width()//2, y))
            else:
                y = (self.fight_box.top + self.attack_area) if self.direction == "top" else (self.fight_box.bottom - self.attack_area)
                pygame.draw.line(screen, red, (self.fight_box.left, y), (self.fight_box.right, y), line_width)
                # Draw bones horizontally
                if elapsed > 700:
                    bone_width = self.bone_img.get_width()
                    for x in range(self.fight_box.left, self.fight_box.right, bone_width):
                        screen.blit(self.bone_img, (x, y - self.bone_img.get_height()//2))

    def is_done(self):
        return self.done

    def check_collision(self, rect):
        return False