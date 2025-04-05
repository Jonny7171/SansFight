import pygame
import random
from settings import *
from attacks.sansSlamAttack import SansSlamAttack
from attacks.blue_movement import handle_blue_mode_movement

"""
Chain SansSlamAttack together multiple times to replicate the attack from Undertale
"""
class SansSlamMultiple:
    def __init__(self, player, fight_box, num_attacks=5, direction=None, slam_speed=10, slam_duration=1500, slam_accel=0.4, jump_impulse=4, gravity_accel=0.4, attack_area=40, sans_sprite_manager=None):
        """
        Initializes a chain of SansSlamAttack instances.
        
        Parameters:
            player: The player object.
            fight_box: The fighting area.
            num_attacks (int): How many attacks to chain
        """
        self.player = player
        self.fight_box = fight_box
        self.num_attacks = num_attacks
        self.current_attack_index = 0
        self.direction = direction
        self.slam_speed = slam_speed
        self.slam_duration = slam_duration
        self.slam_accel = slam_accel
        self.jump_impulse = jump_impulse
        self.gravity_accel = gravity_accel
        self.attack_area = attack_area
        self.sans_sprite_manager = sans_sprite_manager

        # Start the first attack.
        self.current_attack = SansSlamAttack(player, fight_box, self.direction, self.slam_speed, self.slam_duration, self.slam_accel, self.jump_impulse, self.gravity_accel, self.attack_area, self.sans_sprite_manager)
        self.done = False

    def update(self):
        """
        Update the current attack. If the current attack is done,
        start the next one until the chain is complete.
        """
        # Update the current attack.
        self.current_attack.update()
        
        # If the current attack finished, move to the next.
        if self.current_attack.is_done():
            self.current_attack_index += 1
            if self.current_attack_index < self.num_attacks:
                # Start a new attack.
                self.current_attack = SansSlamAttack(self.player, self.fight_box, self.direction, self.slam_speed, self.slam_duration, self.slam_accel, self.jump_impulse, self.gravity_accel, self.attack_area, self.sans_sprite_manager)
            else:
                self.done = True

    def draw(self, screen):
        self.current_attack.draw(screen)
    
    def check_collision(self, rect):
        return self.current_attack.check_collision(rect)

    def is_done(self):
        return self.done