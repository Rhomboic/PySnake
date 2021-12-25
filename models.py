"""
Object Classes for PySnake

This module global objects class definitions for the game PySnake.
"""

from consts import *
from game2d import *
from consts import *


class Block(GRectangle):
    def __init__(self, x, y, width=SEGMENT_LENGTH, height=SEGMENT_LENGTH, fillcolor='blue'):
        super().__init__(x=x, y=y, width=width, height=height, fillcolor=fillcolor)
        self.direction = LEFT
        self.last_x = x
        self.last_y = y


class Snake:
    """
    The snake object

    Attributes:
          head_x: the x coordinate of the snake's head
          head_y: the y coordinate of the snake's head
          segments: the list of the snake's body segments
    """

    def __init__(self, x, y, fillcolor='green'):
        self.head_x = x
        self.head_y = y
        self.segments = [Block(x=self.head_x, y=self.head_y,
                               width=SEGMENT_LENGTH, height=SEGMENT_LENGTH, fillcolor=fillcolor)]


class Apple(Block):
    def __init__(self, x, y, width=SEGMENT_LENGTH, height=SEGMENT_LENGTH, fillcolor='red'):
        super().__init__(x=x, y=y, width=width, height=height, fillcolor=fillcolor)
