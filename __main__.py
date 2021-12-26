"""
The primary application script for PySnake

This is the module with the application code.  Make sure that this module is
in a folder with the following files:

    app.py      (the primary controller class)
    level.py    (the subcontroller for a single game level)
    models.py   (the model classes)
    consts.py   (the application constants)

In addition, you should have the following subfolders

    Fonts         (fonts to use for GLabel)
    Sounds        (sound effects for the game)
    Images        (image files to use in the game)

Moving any of these folders or files will prevent the game from working properly

Author: Adam Issah
Date: December 24th, 2021
"""
from consts import *
from app import *

# Application code
if __name__ == '__main__':
    PySnake(width=GAME_WIDTH, height=GAME_HEIGHT).run()
