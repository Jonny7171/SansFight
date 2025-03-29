import pygame
from settings import *
from player import Player

#Bone class
class Bone:
    def __init__(self, x, y, speed=-4, image_path="assets/bone.webp", desired_height=48, desired_width = 30, rotation=90):
        # Load the bone image
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Get original size and compute scale factor based on the desired height.
        orig_width, orig_height = self.image.get_size()
        scale_factor = desired_height / orig_height
        #desired_width = int(orig_width * scale_factor)
        
        # Scale proportionally
        self.image = pygame.transform.scale(self.image, (desired_width, desired_height))
        
        # Optionally rotate the image. If rotation is None, skip rotating.
        if rotation is not None:
            self.image = pygame.transform.rotate(self.image, rotation)
        
        # Position & speed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_width):
        return self.rect.right < 0 or self.rect.left > screen_width





def test_bones(screen, player, bones):
    # Spawn a bone if needed
    if len(bones) < 1:
        new_bone = Bone(WIDTH, player.rect.centery)
        bones.append(new_bone)
        
    # For each bone, update, draw, and check collisions
    for bone in bones[:]:
        bone.update()
        bone.draw(screen)
        # Calculate an adjusted collision rectangle for this bone
        adjusted_rect = bone.rect.inflate(-5, -10)  # shrink width by 5 and height by 10 pixels
        if player.rect.colliderect(adjusted_rect):
            player.take_damage(1)
            print("Collision detected!")
        # Remove the bone if it's off screen
        if bone.is_off_screen(WIDTH):
            bones.remove(bone)


class Sans_Bone_Gap_Low:
    def __init__(self):
        self.bones = []
        self.timer = 0
        self.spawn_columns()

    def spawn_columns(self):
        columns_x = [500, 600, 700]  # x positions for each column
        gap_y = 200                  # top of the gap
        gap_height = 60             # vertical size of the gap
        speed = -4                  # bone travel speed

        for x in columns_x:
            y = 0
            while y < gap_y:
                bone = Bone(x, y, speed=speed, image_path="assets/bone.webp")
                self.bones.append(bone)
                y += bone.rect.height  # stack next bone below
                y2 = gap_y + gap_height
            while y2 < 400:
                bone = Bone(x, y2, speed=speed, image_path="assets/bone.webp")
                self.bones.append(bone)
                y2 += bone.rect.height

    def update(self):
        self.timer += 1
        # Move all bones, remove if off-screen
        for bone in self.bones[:]:
            bone.update()
            if bone.is_off_screen(WIDTH):
                self.bones.remove(bone)

    def draw(self, screen):
        for bone in self.bones:
            bone.draw(screen)

    def check_collision(self, player_rect):
        """
        For each bone, see if we collide with the player's rect.
        We can shrink the bone rect if needed to avoid bounding box issues.
        """
        for bone in self.bones:
            shrunk_rect = bone.rect.inflate(-10, -10)  # tweak as needed
            if shrunk_rect.colliderect(player_rect):
                return True
        return False

    def is_done(self):
        return self.timer > 300
