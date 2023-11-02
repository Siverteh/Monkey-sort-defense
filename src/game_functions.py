import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, IMAGE_PATH, \
    BACKGROUND_COLOR  # assuming you have these constants in a settings file



def initialize_settings():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    original_flags = screen.get_flags()
    original_size = screen.get_size()

    background_image = pygame.image.load(IMAGE_PATH + "grass_background.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen, original_flags, original_size, background_image


def toggle_fullscreen(fullscreen, screen, original_size, original_flags):
    if fullscreen:
        screen = pygame.display.set_mode(original_size, original_flags)
        fullscreen = False
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        fullscreen = True
    return fullscreen, screen

def handle_mouse_event(pos, monkeys):
    clicked_monkeys = [m for m in monkeys if m.rect.collidepoint(pos)]
    monkeys_killed = 0
    for monkey in clicked_monkeys:
        monkey.clicked()
        if monkey.is_dead():  # Check if the monkey is dead after being clicked.
            monkeys_killed += 1
    return monkeys_killed

def handle_events(events, screen, original_size, original_flags, monkeys, key_states, bananaman):
    monkeys_killed = 0
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                screen = toggle_fullscreen(screen, original_size, original_flags)
            elif event.key in key_states:
                key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in key_states:
                key_states[event.key] = False
                bananaman.stop_walking()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            monkeys_killed += handle_mouse_event(pos, monkeys)
    return monkeys_killed, screen, key_states