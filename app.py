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
        self.state = STATE_START
        self.maintext = GLabel(text="PySnake",
                               font_size=110,
                               font_name='Arcade.ttf',
                               x=GAME_WIDTH/2,
                               y=GAME_HEIGHT/2,
                               linecolor="green")
        self.aidtext = GLabel(text="Press S to Start",
                              font_size=50,
                              font_name='Arcade.ttf',
                              x=GAME_WIDTH/2,
                              y=GAME_HEIGHT/3,
                              linecolor="green")
        self.grid()

    def update(self, dt):

        self.time += dt
        self.determineState()
        if self.state == STATE_ACTIVE:
            self.handleInput()
            self.wallCollision()

            if self.time > BASE_SPEED:
                self.handleHeadMovement()
                self.handleBodyMovement()
                self.handleGrowth()
                self.time = 0

            self.appleSpawner()
        if self.state == STATE_PAUSED:
            self.maintext = GLabel(text="Paused",
                                   font_size=70,
                                   font_name='Arcade.ttf',
                                   x=GAME_WIDTH/2,
                                   y=GAME_HEIGHT//2,
                                   linecolor="green")
            self.aidtext = GLabel(text="Press S to Resume",
                                  font_size=50,
                                  font_name='Arcade.ttf',
                                  x=GAME_WIDTH/2,
                                  y=GAME_HEIGHT/3,
                                  linecolor="green")

        if self.state == STATE_ACTIVE and self.bodyCollision():
            self.state = STATE_END
            self.maintext = GLabel(text="Game Over",
                                   font_size=70,
                                   font_name='Arcade.ttf',
                                   x=GAME_WIDTH/2,
                                   y=GAME_HEIGHT//2,
                                   linecolor="green")
            self.aidtext = GLabel(text="You Lose",
                                  font_size=50,
                                  font_name='Arcade.ttf',
                                  x=GAME_WIDTH/2,
                                  y=GAME_HEIGHT/3,
                                  linecolor="green")

        self.last_keys = self.input.keys

    def draw(self):
        GRectangle(x=GAME_WIDTH/2, y=GAME_HEIGHT/2, width=GAME_WIDTH,
                   height=GAME_HEIGHT, fillcolor='black').draw(self.view)

        if self.state == STATE_ACTIVE:
            for line in self.lines:
                line.draw(self.view)

            for segment in self.snake.segments:
                segment.draw(self.view)

            if self.apple is not None:
                self.apple.draw(self.view)

        if self.state == STATE_PAUSED:
            self.maintext.draw(self.view)
            self.aidtext.draw(self.view)

        if self.state == STATE_START or self.state == STATE_END:
            self.maintext.draw(self.view)
            self.aidtext.draw(self.view)

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
        self.updateLastPos(snake_head)
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
            self.updateLastPos(self.snake.segments[i])
            self.snake.segments[i].x = self.snake.segments[i-1].last_x
            self.snake.segments[i].y = self.snake.segments[i-1].last_y

    def handleGrowth(self):
        if self.eaten():
            last = self.snake.segments[-1]
            x_pos = last.last_x
            y_pos = last.last_y

            self.snake.segments.append(Block(x=x_pos, y=y_pos,
                                             width=SEGMENT_LENGTH, height=SEGMENT_LENGTH, fillcolor='green'))

    def handleInput(self):

        if 'up' in self.input.keys and self.last_keys == ():
            self.snake.segments[0].direction = UP

        if 'down' in self.input.keys and self.last_keys == ():
            self.snake.segments[0].direction = DOWN

        if 'left' in self.input.keys and self.last_keys == ():
            self.snake.segments[0].direction = LEFT

        if 'right' in self.input.keys and self.last_keys == ():
            self.snake.segments[0].direction = RIGHT

    def eaten(self):
        return self.snake.segments[0].x == self.apple.x and self.snake.segments[0].y == self.apple.y

    def appleSpawner(self):
        x = GAME_WIDTH//SEGMENT_LENGTH
        y = GAME_HEIGHT//SEGMENT_LENGTH

        real_left = SEGMENT_LENGTH * (random.randint(1, x-1))
        real_top = SEGMENT_LENGTH * (random.randint(1, y-1))

        if self.eaten():
            while any(segment.left == real_left for segment in self.snake.segments) and any(segment.top == real_top for segment in self.snake.segments):
                real_left = SEGMENT_LENGTH * (random.randint(1, x-1))
                real_top = SEGMENT_LENGTH * (random.randint(1, y-1))

            self.apple.left = real_left
            self.apple.top = real_top

        print(self.apple.left, self.apple.top, len(
            self.snake.segments), self.last_keys)

    def updateLastPos(self, segment):
        segment.last_x = segment.x
        segment.last_y = segment.y

    def wallCollision(self):
        head = self.snake.segments[0]
        if head.left >= GAME_WIDTH:
            head.left = 0
        if head.right <= 0:
            head.right = GAME_WIDTH
        if head.bottom >= GAME_HEIGHT:
            head.bottom = 0
        if head.top <= 0:
            head.top = GAME_HEIGHT

    def bodyCollision(self):
        return any(segment.contains((self.snake.segments[0].x, self.snake.segments[0].y)) for segment in self.snake.segments[1:])

    def determineState(self):
        # Starting a game/Resuming a game
        if 's' in self.input.keys and self.last_keys == () and (self.state == STATE_START):
            self.state = STATE_ACTIVE

        # Pausing midgame
        elif 's' in self.input.keys and self.last_keys == () and self.state == STATE_ACTIVE:
            self.state = STATE_PAUSED

        elif 's' in self.input.keys and self.last_keys == () and self.state == STATE_PAUSED:
            self.state = STATE_ACTIVE
