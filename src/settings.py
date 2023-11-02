import os
import pygame

pygame.display.init()

# --- SCREEN SETTINGS ---
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
SCREEN_TITLE = "Monkey Sort the Game"
FPS = 30  # Frames per second

# --- COLORS ---
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black

# --- ASSETS ---
# Paths to game assets, relative to the main game script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_PATH = os.path.join(BASE_DIR, '../resources/images/')
SOUND_PATH = os.path.join(BASE_DIR, '../resources/sounds/')
FONT_PATH = os.path.join(BASE_DIR, '../resources/fonts/')

# --- GAMEPLAY SETTINGS ---
MONKEY_SIZE = (50, 50)  # Width, Height
MAX_ROUNDS = 10  # Number of rounds before the game ends