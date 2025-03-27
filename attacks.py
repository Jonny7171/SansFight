import pygame
from settings import *
from player import Player

#Bone class
class Bone:
    def __init__(self, x, y, speed=-4, image_path="assets/bone.webp"):
        # Load the bone image
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Get original size
        orig_width, orig_height = self.image.get_size()
        desired_height = 48
        scale_factor = desired_height / orig_height
        desired_width = int(orig_width * scale_factor)
        
        # Scale proportionally
        self.image = pygame.transform.scale(self.image, (desired_width, desired_height))
        
        # Optionally rotate the image (uncomment if needed)
        # self.image = pygame.transform.rotate(self.image, 90)
        
        # Position & speed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_width):
        return self.rect.right < 0 or self.rect.left > screen_width




#Bones Test
def test_bones(screen, player, bones):
    #have 1 bone travel from right to left
    if len(bones) < 1:
        # Create a new bone and add it to the list
        new_bone = Bone(WIDTH, player.rect.centery)
        bones.append(new_bone)
    # Update and draw bones
    for bone in bones[:]:
        bone.update()
        bone.draw(screen)
    #damage detection
    if player.rect.colliderect(bone.rect):
        player.take_damage(1)
        # Remove bones that are off screen
    if bone.is_off_screen(WIDTH):
        bones.remove(bone)
    # Check for collisions with the player
    for bone in bones:
        if player.rect.colliderect(bone.rect):
            # Handle collision (e.g., reduce health, end game, etc.)
            print("Collision detected!")