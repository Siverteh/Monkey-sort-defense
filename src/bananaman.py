import pygame
from settings import *
from pygame.sprite import collide_mask
class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            # Use convert_alpha() to preserve transparency
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image
    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Bananaman(pygame.sprite.Sprite):
    FRAME_UPDATE_DELAY = 10
    ATTACK_FRAME_UPDATE_DELAY = 10
    def __init__(self, x, y, spritesheet_filename):
        pygame.sprite.Sprite.__init__(self)
        self.a_key_pressed = False
        self.x = x
        self.y = y
        self.spritesheet = SpriteSheet(spritesheet_filename)
        self.stun_timer = 0
        self.grace_period = 0

        self.width = 32
        self.height = 32

        #Victory frames:
        self.victory_frames = self.scale_frames(
            self.spritesheet.load_strip((0, 6 * self.height, self.width, self.height), 4))

        #Stunned frames:
        self.stun_frames_right = self.scale_frames(
            self.spritesheet.load_strip((0, 4 * self.height, self.width, self.height), 4))
        self.stun_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.stun_frames_right]

        #Idle frames:
        self.idle_frames_right = self.scale_frames(
            self.spritesheet.load_strip((0, 0 * self.height, self.width, self.height), 4))  # Sample strip
        self.idle_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.idle_frames_right]

        # Load attack frames
        self.attack_frames_right = self.scale_frames(
            self.spritesheet.load_strip((0, 5 * self.height, self.width, self.height), 4))
        self.attack_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames_right]
        self.attacking = False

        # Load walking frames for each direction
        self.walking_frames_right = self.scale_frames(self.spritesheet.load_strip((0, self.height, self.width, self.height), 4))
        self.walking_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.walking_frames_right]
        self.walking_frames_down = self.scale_frames(
            self.spritesheet.load_strip((0, self.height, self.width, self.height), 4))
        self.walking_frames_up = self.scale_frames(
            self.spritesheet.load_strip((0, self.height, self.width, self.height), 4))
        self.frame_update_counter = 0

        self.current_frames = self.walking_frames_right  # Initial direction
        self.current_frame = 0
        self.image = self.current_frames[self.current_frame]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.speed = 6
        self.walking = False
        self.direction = 'right'  # Initial direction

    monkeys_group = pygame.sprite.Group()
    @classmethod
    def set_monkeys_group(cls, group):
        cls.monkeys_group = group

    def scale_frames(self, frames):
        SCALE_FACTOR = 5
        return [pygame.transform.scale(frame, (self.width * SCALE_FACTOR, self.height * SCALE_FACTOR)) for frame in
                frames]

    def idle(self):
        self.walking = False
        if self.direction == 'right':
            self.current_frames = self.idle_frames_right
        elif self.direction == 'left':
            self.current_frames = self.idle_frames_left
        self.current_frame = 0

    def walk(self, direction):
        self.walking = True
        if direction == 'right':
            self.x += self.speed
            self.current_frames = self.walking_frames_right
            self.direction = 'right'
        elif direction == 'left':
            self.x -= self.speed
            self.current_frames = self.walking_frames_left
            self.direction = 'left'
        elif direction == 'up':
            self.y -= self.speed
            # Check if the character is currently moving left
            if self.direction == 'left':
                self.current_frames = [pygame.transform.flip(frame, True, False) for frame in self.walking_frames_up]
            else:
                self.current_frames = self.walking_frames_up
        elif direction == 'down':
            self.y += self.speed
            # Check if the character is currently moving left
            if self.direction == 'left':
                self.current_frames = [pygame.transform.flip(frame, True, False) for frame in self.walking_frames_down]
            else:
                self.current_frames = self.walking_frames_down

        self.frame_update_counter += 1
        if self.frame_update_counter >= self.FRAME_UPDATE_DELAY:
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.frame_update_counter = 0  # Reset the counter

        self.image = self.current_frames[self.current_frame]
        self.rect.topleft = (self.x, self.y)

    def stop_walking(self):
        self.walking = False
        self.idle()

    def victory(self):
        self.current_frames = self.victory_frames


    def attack(self, monkeys):
        ATTACK_RANGE = 10
        ATTACK_WIDTH = 70
        self.attacking = True
        monkeys_killed = 0
        if self.current_frame + 1 >= len(self.current_frames):
            if not self.a_key_pressed:
                self.attacking = False
                self.idle()
            self.current_frame = 0
        else:
            if self.direction == 'right':
                self.current_frames = self.attack_frames_right
                attack_rect = pygame.Rect(self.rect.right, self.rect.centery - ATTACK_WIDTH // 2, ATTACK_RANGE,
                                          ATTACK_WIDTH)
            elif self.direction == 'left':
                self.current_frames = self.attack_frames_left
                attack_rect = pygame.Rect(self.rect.left - ATTACK_RANGE, self.rect.centery - ATTACK_WIDTH // 2,
                                          ATTACK_RANGE, ATTACK_WIDTH)
            # Assuming you have up and down directions for Bananaman as well
            elif self.direction == 'up':
                attack_rect = pygame.Rect(self.rect.centerx - ATTACK_WIDTH // 2, self.rect.top - ATTACK_RANGE,
                                          ATTACK_WIDTH, ATTACK_RANGE)
            elif self.direction == 'down':
                attack_rect = pygame.Rect(self.rect.centerx - ATTACK_WIDTH // 2, self.rect.bottom, ATTACK_WIDTH,
                                          ATTACK_RANGE)
            else:
                return monkeys_killed  # Return early if Bananaman isn't facing a valid direction

            # Check collision with monkeys using the attack hitbox
            hit_monkeys = [monkey for monkey in monkeys if attack_rect.colliderect(monkey.rect)]
            for monkey in hit_monkeys:
                monkey.clicked()
                if monkey.is_dead():  # Check if the monkey is dead after being clicked.
                    monkeys_killed += 1

            self.frame_update_counter += 1
            if self.frame_update_counter >= self.ATTACK_FRAME_UPDATE_DELAY:
                self.current_frame += 1
                self.frame_update_counter = 0
        return monkeys_killed

    def update(self):
        if self.stun_timer > 0:
            self.stun_timer -= 1
        if self.grace_period > 0:
            self.grace_period -= 1
        if self.attacking:
            self.frame_update_counter += 1
            if self.frame_update_counter >= self.ATTACK_FRAME_UPDATE_DELAY:
                if self.current_frame + 1 < len(self.current_frames):
                    self.current_frame += 1
                else:
                    if not self.a_key_pressed:  # If 'A' key is not pressed
                        self.attacking = False
                        self.idle()  # Switch to idle state
                    else:
                        self.current_frame = 0  # Reset to start of attack animation
                self.frame_update_counter = 0

        else:  # This is for the regular movement animation
            self.frame_update_counter += 1
            if self.frame_update_counter >= self.FRAME_UPDATE_DELAY:
                self.current_frame = (self.current_frame + 1) % len(self.current_frames)
                self.frame_update_counter = 0  # Reset the counter

        self.image = self.current_frames[self.current_frame]
        self.rect.topleft = (self.x, self.y)

    def handle_tank_collision(self, bananaman, tank):
        if pygame.sprite.collide_rect(self, tank):
            if collide_mask(bananaman, tank):
                tank.push_back(self)
