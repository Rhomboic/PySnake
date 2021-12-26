"""
Constants for PySnake

This module global constants for the game PySnake.
"""
### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH = 900
#: the height of the game display
GAME_HEIGHT = 690

SEGMENT_LENGTH = 30
SEGMENT_BORDER = 1

BASE_SPEED = 0.15

STATE_START = 0
STATE_PAUSED = 2
STATE_ACTIVE = 1
STATE_END = 3
STATE_FINISH = 4
STATE_BEGIN = -1
# STATE_FINISH = 3

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

SOUNDS = ['lose.wav', 'crunch.wav', 'level.wav', 'pause.wav', 'start.flac']
