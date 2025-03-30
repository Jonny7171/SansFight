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



