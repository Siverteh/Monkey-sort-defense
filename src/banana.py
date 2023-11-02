import pygame
from settings import *
import math
class Banana(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))

        self.is_returning = False
        self.target_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 3  # Adjust as needed

    def update(self):
        if self.is_returning:
            # Calculate the direction vector from the banana to the target position
            direction_x = self.target_position[0] - self.rect.centerx
            direction_y = self.target_position[1] - self.rect.centery

            # Normalize the direction vector
            length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if length != 0:
                direction_x /= length
                direction_y /= length

            # Move the banana based on the normalized direction
            self.rect.x += direction_x * self.speed
            self.rect.y += direction_y * self.speed

            # Check if the banana has reached its target position
            if abs(self.rect.centerx - self.target_position[0]) < self.speed and \
                    abs(self.rect.centery - self.target_position[1]) < self.speed:
                self.rect.center = self.target_position
                self.is_returning = False

    def reset(self):
        self.is_returning = True