import pygame
import random
import math
from Gaster_class import GasterBlaster

class sans_gaster_blaster_attack:
    def __init__(self, player):
        self.blaster_list = []
        self.timer = 0
        self.player = player
        self.spawn_next = 0

    def update(self):
        now = pygame.time.get_ticks()
        self.timer += 1

        # Spawn new blaster every second
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
        angle = random.uniform(0, 360)
        distance = 500
        radians = math.radians(angle)

        # Spawn circle around player
        x = self.player.rect.centerx + math.cos(radians) * distance
        y = self.player.rect.centery - math.sin(radians) * distance

        spawn_pos = (x, y)
        # We move to 100 px away from player so we appear on screen
        # or maybe directly to the box boundary. Tweak to taste.
        approach_distance = 100  
        approach_x = self.player.rect.centerx + math.cos(radians) * approach_distance
        approach_y = self.player.rect.centery - math.sin(radians) * approach_distance
        move_target = (approach_x, approach_y)

        blaster = GasterBlaster(
            start_pos=spawn_pos,
            target_pos=move_target,   # We'll move here
            open_delay=400,
            fire_delay=700,
            scale=0.2
        )
        self.blaster_list.append(blaster)

    def distance_point_to_segment(self, px, py, ax, ay, bx, by):
        """
        Returns the shortest distance from point P(px, py)
        to the line segment AB(ax, ay) -> (bx, by).
        """
        # Vector AP = P - A, AB = B - A
        ABx, ABy = (bx - ax), (by - ay)
        APx, APy = (px - ax), (py - ay)

        # Length squared of AB
        ab_len_sq = ABx * ABx + ABy * ABy
        if ab_len_sq == 0:
            # A and B are the same point
            return math.hypot(px - ax, py - ay)

        # Project AP onto AB, clamped to [0, 1] to stay within segment
        t = (APx * ABx + APy * ABy) / ab_len_sq
        t = max(0, min(1, t))

        # Closest point on AB to P is A + t*AB
        closest_x = ax + t * ABx
        closest_y = ay + t * ABy

        # Return distance from P to that closest point
        return math.hypot(px - closest_x, py - closest_y)

    def check_collision(self, player_rect):
        player_center = player_rect.center
        # Example radius if you want a small circle around the heart
        # You can tweak or base it on player_rect width/height.
        player_radius = player_rect.width // 2

        for blaster in self.blaster_list:
            if blaster.laser_beam:
                start_vec, end_vec = blaster.laser_beam
                # Convert from Vector2 to simple x,y floats
                ax, ay = start_vec.x, start_vec.y
                bx, by = end_vec.x, end_vec.y
                px, py = player_center

                dist = self.distance_point_to_segment(px, py, ax, ay, bx, by)

                # If the distance from the player's center to the laser
                # is less than the player's radius => collision
                if dist < player_radius:
                    return True

        return False

    def is_done(self):
        return self.timer > 4500
