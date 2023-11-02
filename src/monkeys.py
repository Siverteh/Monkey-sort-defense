import pygame
from settings import *
import random
import math
from pygame.sprite import collide_mask
class Monkey(pygame.sprite.Sprite):
    """Base class for all monkeys."""

    def __init__(self, image_path, lives, speed):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, MONKEY_SIZE)
        self.rect = self.image.get_rect()

        # Spawn monkey at a random edge
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.rect.x = random.randint(0, SCREEN_WIDTH - MONKEY_SIZE[0])
            self.rect.y = 0 - MONKEY_SIZE[1]
        elif edge == 'bottom':
            self.rect.x = random.randint(0, SCREEN_WIDTH - MONKEY_SIZE[0])
            self.rect.y = SCREEN_HEIGHT
        elif edge == 'left':
            self.rect.x = 0 - MONKEY_SIZE[0]
            self.rect.y = random.randint(0, SCREEN_HEIGHT - MONKEY_SIZE[1])
        else:  # right
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT - MONKEY_SIZE[1])

        self.lives = lives
        self.speed = speed

    def update(self):
        """Move the monkey towards the banana's location."""
        banana_x, banana_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Get the banana's location
        monkey_x, monkey_y = self.rect.center  # Get the current monkey's location

        # Calculate the direction vector from the monkey to the banana
        direction_x = banana_x - monkey_x
        direction_y = banana_y - monkey_y

        # Normalize the direction vector
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if length != 0:
            direction_x /= length
            direction_y /= length

        # Update the monkey's position based on the normalized direction
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

    def clicked(self):
        """Handle a monkey being clicked."""
        self.lives -= 1
        if self.lives <= 0:
            if isinstance(self, Seeker) and self.has_banana:
                self.drop_banana()
            self.kill()  # This removes the sprite from all groups

    def is_dead(self):
        """Check if the monkey is dead."""
        return self.lives <= 0


class Seeker(Monkey):
    def __init__(self, banana):
        super().__init__(IMAGE_PATH + "round_no_detail_monkey.png", random.randint(1, 2), random.randint(4, 8))
        self.banana = banana
        self.has_banana = False

    def drop_banana(self):
        self.has_banana = False
        self.banana.reset()

    def update(self):
        if not self.has_banana:
            # Seeks the banana
            banana_x, banana_y = self.banana.rect.center
            monkey_x, monkey_y = self.rect.center

            # Calculate direction from monkey to banana
            direction_x = banana_x - monkey_x
            direction_y = banana_y - monkey_y

            # Normalize direction
            length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if length != 0:
                direction_x /= length
                direction_y /= length

            # Move monkey based on direction
            self.rect.x += direction_x * self.speed
            self.rect.y += direction_y * self.speed

            # Check for collision with banana
            if pygame.sprite.collide_rect(self, self.banana):
                self.has_banana = True

        else:
            self.speed = random.randint(1, 3)
            # Monkey has the banana and is now trying to escape
            # Here, we'll make the monkey run to the nearest edge. You can adjust this behavior as desired.
            if self.rect.x < SCREEN_WIDTH // 2:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

            if self.rect.y < SCREEN_HEIGHT // 2:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

            self.banana.rect.center = self.rect.center

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
class Mage(Monkey):
    def __init__(self, bananaman):
        super().__init__(IMAGE_PATH + "round_monkey.png", 2, 3)
        self.shoot_timer = 0
        self.bananaman = bananaman
        self.projectiles_group = pygame.sprite.Group()

    def update(self):
        # Stand back a certain distance from the banana
        threshold_distance = 500  # distance from banana where Mage will stop

        # Calculate distances to the edges
        distance_to_left = self.rect.left
        distance_to_right = SCREEN_WIDTH - self.rect.right
        distance_to_top = self.rect.top
        distance_to_bottom = SCREEN_HEIGHT - self.rect.bottom

        # Determine if the monkey is closer to the horizontal or vertical edges
        is_closer_to_horizontal = min(distance_to_top, distance_to_bottom) < min(distance_to_left, distance_to_right)

        if is_closer_to_horizontal:
            # Monkey is closer to the top or bottom
            # Add logic if you want the behavior to change when the monkey is closer to the top or bottom
            pass
        else:
            # Monkey is closer to the left or right
            # Add logic if you want the behavior to change when the monkey is closer to the left or right
            pass

        if distance(self.rect.center, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) > threshold_distance:
            super().update()

        # Shoot projectiles at Bananaman
        self.shoot_timer += 1
        if self.shoot_timer >= random.randint(100, 155):  # shooting frequency
            projectile = Projectile(self.rect.center, self.bananaman.rect.center)
            self.projectiles_group.add(projectile)
            self.shoot_timer = 0

    def handle_projectile_collision(self, bananaman):
        for projectile in self.projectiles_group:
            if pygame.sprite.collide_rect(bananaman, projectile):
                if collide_mask(bananaman, projectile):
                    projectile.kill()
                    if bananaman.stun_timer <= 0 and bananaman.grace_period <= 0:
                        if bananaman.direction == "right":
                            bananaman.current_frames = bananaman.stun_frames_right
                        elif bananaman.direction == "left":
                            bananaman.current_frames = bananaman.stun_frames_left
                        bananaman.stun_timer = 60  # Stun for 1 second (adjust as needed)
                        bananaman.grace_period = 180  # Cooldown for 3 seconds (adjust as needed)




class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()

        self.image = pygame.image.load(IMAGE_PATH + "orb_red.png")  # Replace with your projectile image
        self.rect = self.image.get_rect(center=start_pos)

        direction_x = target_pos[0] - start_pos[0]
        direction_y = target_pos[1] - start_pos[1]

        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if length != 0:
            direction_x /= length
            direction_y /= length

        self.speed = 5  # or any other value
        self.velocity = (direction_x * self.speed, direction_y * self.speed)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

class Tank(Monkey):
    def __init__(self, bananaman):
        super().__init__(IMAGE_PATH + "square_no_detail_monkey.png", random.randint(20, 50), random.randint(1, 2))
        self.bananaman = bananaman
        self.is_mage = False

    def push_back(self, bananaman):
        push_distance = 10  # Adjust this value as needed

        # Calculate direction from tank to Bananaman
        dir_x = (bananaman.x - self.rect.x)
        dir_y = (bananaman.y - self.rect.y)

        # Normalize direction
        length = math.sqrt(dir_x ** 2 + dir_y ** 2)
        if length != 0:
            dir_x /= length
            dir_y /= length

        # Update Bananaman's position based on the direction
        bananaman.x += dir_x * push_distance
        bananaman.y += dir_y * push_distance


    def update(self):
        # Move towards Bananaman instead of the banana
        target_x, target_y = self.bananaman.rect.center

        direction_x = target_x - self.rect.centerx
        direction_y = target_y - self.rect.centery

        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if length != 0:
            direction_x /= length
            direction_y /= length

        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed


class MonkeyType4(Monkey):
    def __init__(self):
        super().__init__(IMAGE_PATH + "square_monkey.png", 6, 1)