import pygame
from settings import *
from player import Player

#Bone class
class Bone:
    def __init__(self, x, y, speed=-4, image_path="assets/bone.webp", desired_height=48, desired_width = 30, rotation=90):
        # Load the bone image
        self.image = pygame.image.load(image_path).convert_alpha()
        
        
        # Scale proportionally
        self.image = pygame.transform.scale(self.image, (desired_height, desired_width))
        
        # Optionally rotate the image. 
        if rotation is not None:
            self.image = pygame.transform.rotate(self.image, rotation)
        
        # Position & speed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self, direction="left"):
        if direction == "left":
            self.rect.x += self.speed
        elif direction == "right":
            self.rect.x -= self.speed
        elif direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_width, buffer=50):
        if self.speed < 0:  # Moving left
            return self.rect.right < -buffer  # fully off left side
        elif self.speed > 0:  # Moving right
            return self.rect.left > screen_width + buffer  # fully off right side
        return False  # Not moving? Don't remove





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



class Sans_Bone_Gap_Low:
    def __init__(self):
        self.bones = []
        self.timer = 0
        self.spawn_columns()

    def spawn_columns(self):
        columns_x = [500, 700, 900, 1100, 1300, 1500, 1700]  # x positions for each column
        speed = -2

        # Fight box boundaries:
        box_top = 150
        box_bottom = 300

        top_bone_height = 110
        bottom_bone_height = 35
        
        # For a thin bone, reduce the width. For a thicker bone, increase it.
        bone_width = 30

        for x in columns_x:
            # ---- TOP bone ----
            top_bone_y = box_top  # spawn exactly at the top of the box
            top_bone = Bone(
                x, 
                top_bone_y-8, 
                speed=speed, 
                image_path="assets/bone.webp",
                desired_height=top_bone_height, 
                desired_width=bone_width, 
                rotation=90  # rotate 90 if the original bone is horizontal
            )
            self.bones.append(top_bone)

            # ---- BOTTOM bone ----
            # Position it so it sits at the bottom of the box
            bottom_bone_y = box_bottom - bottom_bone_height
            bottom_bone = Bone(
                x, 
                bottom_bone_y, 
                speed=speed, 
                image_path="assets/bone.webp",
                desired_height=bottom_bone_height, 
                desired_width=bone_width, 
                rotation=90
            )
            self.bones.append(bottom_bone)

        # Add mirrored bones coming from left to right
        mirrored_columns_x = [100, -100, -300, -500, -700, -900, -1100]  # x positions for mirrored columns
        mirrored_speed = 2

        for x in mirrored_columns_x:
            # ---- TOP mirrored bone ----
            top_bone_y = box_top  # spawn exactly at the top of the box
            top_bone = Bone(
                x, 
                top_bone_y-8, 
                speed=mirrored_speed, 
                image_path="assets/bone.webp",
                desired_height=top_bone_height, 
                desired_width=bone_width, 
                rotation=90  # rotate 90 if the original bone is horizontal
            )
            self.bones.append(top_bone)

            # ---- BOTTOM mirrored bone ----
            # Position it so it sits at the bottom of the box
            bottom_bone_y = box_bottom - bottom_bone_height
            bottom_bone = Bone(
                x, 
                bottom_bone_y, 
                speed=mirrored_speed, 
                image_path="assets/bone.webp",
                desired_height=bottom_bone_height, 
                desired_width=bone_width, 
                rotation=90
            )
            self.bones.append(bottom_bone)


    def update(self):
        self.timer += 1
        for bone in self.bones[:]:
            bone.update()
            if bone.is_off_screen(WIDTH):
                self.bones.remove(bone)

    def draw(self, screen):
        FIGHT_BOX_RECT = pygame.Rect(175, 150, 250, 150)
        for bone in self.bones:
            bone.update()
            if FIGHT_BOX_RECT is None or bone.rect.colliderect(FIGHT_BOX_RECT):
                bone.draw(screen)

    def check_collision(self, player_rect):
        """
        For each bone, see if we collide with the player's rect.
        We can shrink the bone rect if needed to avoid bounding box issues.
        """
        for bone in self.bones:
            shrunk_rect = bone.rect.inflate(-15, -30)  # NOT PERFECT YET
            if shrunk_rect.colliderect(player_rect):
                return True
        return False

    def is_done(self):
        return self.timer > 450
