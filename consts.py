"""
Constants for Tetris

This module global constants for the game Tetris.
"""
import enum
### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH = 600
BOARD_WIDTH = 300
#: the height of the game display
GAME_HEIGHT = 600

BLOCK_LENGTH = 30

LEVELS_TO_UPGRADE = 2

BASE_SPEED = 0.8


class ORIENTATION(enum.Enum):
    North = 1
    East = 2
    South = 3
    West = 4


DROP = 'block.wav'
LOSE = 'lose.wav'

STATE_PAUSED = 0
STATE_ACTIVE = 1
STATE_END = 2
STATE_FINISH = 3
