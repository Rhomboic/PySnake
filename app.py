from consts import *
from game2d import *
from wave import *
from models import *
import random
import pprint


class PySnake(GameApp):

    def start(self):
        self.snake = Snake(x=GAME_WIDTH - 5*SEGMENT_LENGTH -
                           SEGMENT_LENGTH/2, y=GAME_HEIGHT/2)
        self.apple = Apple(x=5*SEGMENT_LENGTH +
                           SEGMENT_LENGTH/2, y=GAME_HEIGHT/2)
        self.time = 0
        self.last_keys = ()
        self.lines = []
        self.grid()

    def update(self, dt):
        self.time += dt
        self.handleInput()

        if self.time > BASE_SPEED:
            self.handleHeadMovement()
            self.handleBodyMovement()
            self.handleGrowth()
            self.time = 0

        self.appleSpawner()

    def draw(self):
        GRectangle(x=GAME_WIDTH/2, y=GAME_HEIGHT/2, width=GAME_WIDTH,
                   height=GAME_HEIGHT, fillcolor='black').draw(self.view)

        for line in self.lines:
            line.draw(self.view)

        for segment in self.snake.segments:
            segment.draw(self.view)

        if self.apple is not None:
            self.apple.draw(self.view)

    # HELPERS
    def grid(self):
        vert_lines = GAME_WIDTH//30
        horz_lines = GAME_HEIGHT//30

        for i in range(vert_lines):
            self.lines.append(GPath(points=(30*(i), 0, 30*(i), GAME_HEIGHT),
                                    linewidth=1,
                                    linecolor="gray"))
        for i in range(int(horz_lines)):
            self.lines.append(GPath(points=(0, 30*(i+1), GAME_WIDTH, 30*(i+1)),
                                    linewidth=1,
                                    linecolor="gray"))

    def handleHeadMovement(self):
        snake_head = self.snake.segments[0]
        if snake_head.direction == UP:
            snake_head.y += SEGMENT_LENGTH
        elif snake_head.direction == RIGHT:
            snake_head.x += SEGMENT_LENGTH
        elif snake_head.direction == DOWN:
            snake_head.y -= SEGMENT_LENGTH
        elif snake_head.direction == LEFT:
            snake_head.x -= SEGMENT_LENGTH

    def handleBodyMovement(self):
        for i in range(1, len(self.snake.segments)):
            self.snake.segments[i].x = self.snake.segments[i-1].x
            self.snake.segments[i].y = self.snake.segments[i-1].y

    def handleGrowth(self):
        if self.eaten():
            last = self.snake.segments[-1]
            x_pos = None
            y_pos = None
            if last.direction == UP:
                x_pos = last.x
                y_pos = last.y-SEGMENT_LENGTH
            elif last.direction == DOWN:
                x_pos = last.x
                y_pos = last.y+SEGMENT_LENGTH
            elif last.direction == LEFT:
                x_pos = last.x + SEGMENT_LENGTH
                y_pos = last.y
            elif last.direction == RIGHT:
                x_pos = last.x - SEGMENT_LENGTH
                y_pos = last.y

            self.snake.segments.append(Block(x=x_pos, y=y_pos,
                                             width=SEGMENT_LENGTH, height=SEGMENT_LENGTH))

    def handleInput(self):

        if 'up' in self.input.keys and 'up' not in self.last_keys:
            self.snake.segments[0].direction = UP

        if 'down' in self.input.keys and 'down' not in self.last_keys:
            self.snake.segments[0].direction = DOWN

        if 'left' in self.input.keys and 'left' not in self.last_keys:
            self.snake.segments[0].direction = LEFT

        if 'right' in self.input.keys and 'right' not in self.last_keys:
            self.snake.segments[0].direction = RIGHT

    def eaten(self):
        return self.snake.segments[0].x == self.apple.x and self.snake.segments[0].y == self.apple.y

    def appleSpawner(self):
        x = GAME_WIDTH//SEGMENT_LENGTH
        y = GAME_HEIGHT//SEGMENT_LENGTH

        if self.eaten():
            self.apple.x = random.randint(0, 30*x) + SEGMENT_LENGTH/2
            self.apple.y = random.randint(0, 30*y) + SEGMENT_LENGTH/2
