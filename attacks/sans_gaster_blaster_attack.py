import pygame
import random
import math
from Gaster_class import GasterBlaster
from settings import *

class sans_gaster_blaster_attack:
    def __init__(self, player):
        self.blaster_list = []
        self.timer = 0
        self.player = player
        self.spawn_next = 0

    def update(self):
        now = pygame.time.get_ticks()
        self.timer += 1

        # Spawn new blaster every  2 seconds (not perfected yet)
        if now > self.spawn_next:
            self.spawn_next = now + 1000
            self.spawn_blaster()


        for blaster in self.blaster_list[:]:
            blaster.update()

            # Remove if fully faded
            if blaster.is_faded_out():
                self.blaster_list.remove(blaster)

    def draw(self, screen):
        for blaster in self.blaster_list:
            blaster.draw(screen)

    def spawn_blaster(self):
        # Player center
        player_x = self.player.rect.centerx
        player_y = self.player.rect.centery

        # Fight box boundaries (I think, make var's when confirmed)
        fight_box_left = 125
        fight_box_top = 150
        fight_box_right = 475
        fight_box_bottom = 300

        # Expanded fight box boundaries
        margin = FIGHT_BOX_MARGIN
        exp_left = fight_box_left - margin   # 75
        exp_top = fight_box_top - margin     # 100
        exp_right = fight_box_right + margin # 525
        exp_bottom = fight_box_bottom + margin  # 350

        # Choose a random angle (in degrees) and convert to radians
        angle = random.uniform(0, 360)
        radians = math.radians(angle)
        dir_x = math.cos(radians)
        dir_y = -math.sin(radians)

        # Compute t-values for the intersection of the ray from the player.
        t_candidates = []
        if dir_x < 0:
            t_left = (exp_left - player_x) / dir_x
            if t_left > 0:
                t_candidates.append(t_left)
        if dir_x > 0:
            t_right = (exp_right - player_x) / dir_x
            if t_right > 0:
                t_candidates.append(t_right)
        if dir_y < 0:
            t_top = (exp_top - player_y) / dir_y
            if t_top > 0:
                t_candidates.append(t_top)
        if dir_y > 0:
            t_bottom = (exp_bottom - player_y) / dir_y
            if t_bottom > 0:
                t_candidates.append(t_bottom)

        if t_candidates:
            t = min(t_candidates)
        else:
            t = 180  # Fallback

        approach_target = (player_x + dir_x * t, player_y + dir_y * t)

        # Spawn position. Start 500 away
        spawn_distance = GASTER_BLASTER_SPWAN
        spawn_pos = (player_x + dir_x * spawn_distance, player_y + dir_y * spawn_distance)

        # Calculate the angle for the blaster's "mouth" to face the player.
        dx = player_x - spawn_pos[0]
        dy = player_y - spawn_pos[1]
        raw_angle = math.degrees(math.atan2(-dy, dx)) #Needs to be negative dy for some reason
        orientation_degrees = raw_angle  

        # Create and add the blaster
        blaster = GasterBlaster(
            start_pos=spawn_pos,
            target_pos=approach_target,
            open_delay=1200,
            fire_delay=1200,
            scale=0.2, #Looks good
            orientation=orientation_degrees
        )
        self.blaster_list.append(blaster)




#Math
    def distance_point_to_segment(self, px, py, ax, ay, bx, by):
        # Vector AP = P - A, AB = B - A
        ABx, ABy = (bx - ax), (by - ay)
        APx, APy = (px - ax), (py - ay)

        # Length squared of AB
        ab_len_sq = ABx * ABx + ABy * ABy
        if ab_len_sq == 0:
            # A and B are the same point
            return math.hypot(px - ax, py - ay)

        # Project AP onto AB
        t = (APx * ABx + APy * ABy) / ab_len_sq
        t = max(0, min(1, t))

        # Closest point on AB to P is A + t*AB
        closest_x = ax + t * ABx
        closest_y = ay + t * ABy

        # Return distance from P to that closest point
        return math.hypot(px - closest_x, py - closest_y)


#Collision logic
    def check_collision(self, player_rect):
        player_center = player_rect.center
        player_radius = player_rect.width // 2

        for blaster in self.blaster_list:
            if blaster.laser_beam:
                start_vec, end_vec = blaster.laser_beam
                ax, ay = start_vec.x, start_vec.y
                bx, by = end_vec.x, end_vec.y
                px, py = player_center

                dist = self.distance_point_to_segment(px, py, ax, ay, bx, by)

                if dist < player_radius:
                    return True

        return False

    def is_done(self):
        return self.timer > 600
