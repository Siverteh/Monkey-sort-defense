import pygame
import random
from settings import *
from monkeys import Seeker, Tank, Mage
from utils import randomsort
import time
from bananaman import *
from game_functions import *
from banana import *

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monkey Sort the Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Sprite Groups for easier handling of game objects
all_sprites = pygame.sprite.Group()
monkeys = pygame.sprite.Group()

font = pygame.font.SysFont(None, 36)  # Use default font with size 36

HIGH_SCORE = 0
HIGHEST_ROUND = 0

def show_intro(screen):
    """
    Display the game's introductory screen until the player clicks.
    """
    intro_running = True
    intro_image = pygame.image.load(IMAGE_PATH + "intro.jpg")

    # Scale the image to fit the screen's size
    intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while intro_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                intro_running = False
            if event.type == pygame.KEYDOWN:  # Check for keyboard event
                if event.key == pygame.K_SPACE:  # Then check if the key pressed is SPACE
                    intro_running = False

        screen.blit(intro_image, (0, 0))  # Draw the image from top-left corner
        pygame.display.flip()
        clock.tick(60)


def initialize_game():
    # Initialize screen dimensions and settings
    screen, original_flags, original_size, background_image = initialize_settings()

    # Setup bananaman
    bananaman = Bananaman(900, 400, IMAGE_PATH + "BananaMan.png")

    # Setup banana
    banana = Banana(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, IMAGE_PATH + "banana.png")

    key_states = {
        pygame.K_d: False,
        pygame.K_a: False,
        pygame.K_w: False,
        pygame.K_s: False,
        pygame.K_l: False
    }

    return screen, original_flags, original_size, background_image, bananaman, banana, key_states


def game_over(screen, round_number, score):
    """
    Display a game over screen and ask the player if they want to restart or return to the main menu.
    Returns True if the player chooses to restart, False otherwise.
    """
    global HIGH_SCORE
    if HIGH_SCORE < score:
        HIGH_SCORE = score
    global HIGHEST_ROUND
    if HIGHEST_ROUND < round_number:
        HIGHEST_ROUND = round_number

    main_font = pygame.font.SysFont(None, 100)
    message = main_font.render("Game Over!", True, (255, 0, 0))

    choice_font = pygame.font.SysFont(None, 36)
    restart_message = choice_font.render("Press R to Restart", True, (0, 255, 0))  # Green color
    menu_message = choice_font.render("Press M for Main Menu", True, (0, 0, 255))  # Blue color

    # New messages with different colors
    round_message = choice_font.render(f"Round Reached: {round_number}", True, (255, 255, 0))  # Yellow color
    highest_round_message = choice_font.render(f"Highest Round Ever: {HIGHEST_ROUND}", True, (255, 165, 0))  # Orange color
    monkeys_killed_message = choice_font.render(f"Score: {score}", True, (255, 255, 255))  # White color
    most_monkeys_killed_message = choice_font.render(f"High score: {HIGH_SCORE}", True, (160, 32, 240))  # Purple color

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_m:
                    return False

        screen.fill((0, 0, 0))  # Black background
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, 100))  # Slightly further down
        screen.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, SCREEN_HEIGHT // 2 - 50))  # Moved up
        screen.blit(menu_message, (SCREEN_WIDTH // 2 - menu_message.get_width() // 2, SCREEN_HEIGHT // 2))  # Moved up

        # Start scores from the bottom and move upwards
        screen.blit(most_monkeys_killed_message, (SCREEN_WIDTH // 2 - most_monkeys_killed_message.get_width() // 2, SCREEN_HEIGHT - 50))
        screen.blit(monkeys_killed_message, (SCREEN_WIDTH // 2 - monkeys_killed_message.get_width() // 2, SCREEN_HEIGHT - 100))
        screen.blit(highest_round_message, (SCREEN_WIDTH // 2 - highest_round_message.get_width() // 2, SCREEN_HEIGHT - 150))
        screen.blit(round_message, (SCREEN_WIDTH // 2 - round_message.get_width() // 2, SCREEN_HEIGHT - 200))

        pygame.display.flip()


def run_game():
    screen, original_flags, original_size, background_image, bananaman, banana, key_states = initialize_game()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(bananaman)  # Add Bananaman to the all_sprites group
    all_sprites.add(banana)

    monkeys = pygame.sprite.Group()

    spawn_timer = 0
    round_number = 1
    monkeys_killed = 0
    monkeys_to_spawn = randomsort(round_number) if round_number != 1 else 1
    monkeys_spawned = 0
    score = 0
    countdown = 0
    running = True
    victory = True
    while running:
        monkeys_killed_delta, screen, key_states = handle_events(pygame.event.get(), screen,
                                                                             original_size,
                                                                             original_flags, monkeys, key_states,
                                                                         bananaman)

        if key_states[pygame.K_d] and bananaman.stun_timer <= 0 and countdown <= 0:
            bananaman.walk('right')
        if key_states[pygame.K_a] and bananaman.stun_timer <= 0 and countdown <= 0:
            bananaman.walk('left')
        if key_states[pygame.K_w] and bananaman.stun_timer <= 0 and countdown <= 0:
            bananaman.walk('up')
        if key_states[pygame.K_s] and bananaman.stun_timer <= 0 and countdown <= 0:
            bananaman.walk('down')
        if key_states[pygame.K_l] and bananaman.stun_timer <= 0 and countdown <= 0:
            i = bananaman.attack(monkeys)
            monkeys_killed += i
            score += i
            bananaman.a_key_pressed = True  # Set the flag to True when 'a' is pressed
        else:
            bananaman.a_key_pressed = False

        monkeys_killed += monkeys_killed_delta

        global HIGH_SCORE
        if score > HIGH_SCORE:
            HIGH_SCORE = score

        # Check if all monkeys for the round have been killed
        if monkeys_killed == monkeys_to_spawn and victory:
            countdown = 180


        all_sprites.update()

        spawn_timer += 1
        if spawn_timer >= random.randint(50, 150):
            if monkeys_spawned < monkeys_to_spawn:  # Only spawn up to the required number of monkeys
                monkey_type = random.randint(1, 3)
                if monkey_type == 1:
                    monkey = Seeker(banana)
                elif monkey_type == 2:
                    monkey = Mage(bananaman)
                elif monkey_type == 3:
                    monkey = Tank(bananaman)
                all_sprites.add(monkey)
                monkeys.add(monkey)
                spawn_timer = 0  # Reset the spawn timer
                monkeys_spawned += 1  # Increment the spawned monkeys counter

        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        for monkey in monkeys:
            if isinstance(monkey, Seeker) and monkey.has_banana:
                screen.blit(monkey.banana.image, monkey.banana.rect.topleft)
                if monkey.rect.left > SCREEN_WIDTH or \
                        monkey.rect.right < 0 or \
                        monkey.rect.top > SCREEN_HEIGHT or \
                        monkey.rect.bottom < 0:
                    # Monkey has gone outside the screen.
                    if game_over(screen, round_number - 1, score):
                        return True
                    else:
                        return False

            elif isinstance(monkey, Mage):
                monkey.projectiles_group.update()
                monkey.projectiles_group.draw(screen)
                monkey.handle_projectile_collision(bananaman)
            elif isinstance(monkey, Tank):
                bananaman.handle_tank_collision(bananaman, monkey)

        if countdown >= 0:
            victory = False
            bananaman.victory()
            if countdown == 0:
                round_number += 1
                monkeys_killed = 0
                monkeys_to_spawn = randomsort(round_number) if round_number != 1 else 1

                # Reset the spawn timer and spawned monkeys counter
                spawn_timer = 0
                monkeys_spawned = 0
                victory = True
                bananaman.idle()

            # Display "Round Completed" message in the middle of the screen
            round_completed_text = font.render(f"Round Completed: Starting Round {round_number}", True,
                                                   (255, 255, 255))
            screen.blit(round_completed_text, (SCREEN_WIDTH // 2 - round_completed_text.get_width() // 2,
                                                   SCREEN_HEIGHT // 2 - round_completed_text.get_height() // 2))

            countdown -= 1

        round_text = font.render(f"Round: {round_number - 1}", True, (0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0,0,0))
        monkeys_text = font.render(f"Monkeys Killed: {monkeys_killed}/{monkeys_to_spawn}", True, (0, 0, 0))
        screen.blit(round_text, (10, 10))
        screen.blit(score_text, (SCREEN_WIDTH/2, 10))
        screen.blit(monkeys_text, (SCREEN_WIDTH - 300, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Start the game
if __name__ == "__main__":

    while True:
        restart = True
        show_intro(screen)
        while restart:
            restart = run_game()