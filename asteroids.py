import random, math, arcade, os

from typing import cast

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OFFSCREEN_SPACE = 300
SCREEN_TITEL = "ASTEROIDS! \n based off of the original Atari Asteroids"
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE

class Asteroid(arcarde.Sprite):
  # Sprite that represents an asteroid
  
