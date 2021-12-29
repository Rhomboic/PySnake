from consts import *
from game2d import *
from wave import *
from models import *
import random


class PySnake(GameApp):

    def start(self):
        self.snake = Snake(x=SEGMENT_LENGTH * (random.randint(1, GAME_WIDTH//SEGMENT_LENGTH-1)) + SEGMENT_LENGTH//2,
                           y=SEGMENT_LENGTH * (random.randint(1, GAME_HEIGHT//SEGMENT_LENGTH-1)) + SEGMENT_LENGTH//2)
        self.apple = Apple(x=SEGMENT_LENGTH * (random.randint(1, GAME_WIDTH//SEGMENT_LENGTH-1)) + SEGMENT_LENGTH//2,
                           y=SEGMENT_LENGTH * (random.randint(1, GAME_HEIGHT//SEGMENT_LENGTH-1)) + SEGMENT_LENGTH//2)
        # Keep searching for another spot if apple happens to spawn on snake at start
        while self.apple.x == self.snake.head_x and self.apple.y == self.snake.head_y:
            self.apple = Apple(x=SEGMENT_LENGTH * (random.randint(1, GAME_WIDTH//SEGMENT_LENGTH-1)) + SEGMENT_LENGTH//2,
                               y=SEGMENT_LENGTH * (random.randint(1, GAME_HEIGHT//SEGMENT_LENGTH-1)) + SEGMENT_LENGTH//2)
        self.time = 0
        self.last_keys = ()
        self.lines = []
        self.state = STATE_START
        self.maintext = GLabel(text="PySnake",
                               font_size=150,
                               font_name='Arcade.ttf',
                               x=GAME_WIDTH/2,
                               y=2.8*GAME_HEIGHT/8,
                               linecolor="yellow")
        self.aidtext = GLabel(text="Press S to Start",
                              font_size=50,
                              font_name='Arcade.ttf',
                              x=GAME_WIDTH/2,
                              y=GAME_HEIGHT/4,
                              linecolor="green")

        self.SnakeImage = GImage(
            x=GAME_WIDTH/2, y=3*GAME_HEIGHT/5, width=300, height=300, source='snake.png')

        self.eatsound = Sound(SOUNDS[1])
        self.theme = Sound(SOUNDS[2])
        self.deaththeme = Sound(SOUNDS[0])
        self.pausesound = Sound(SOUNDS[3])
        self.starttheme = Sound(SOUNDS[4])
        self.starttheme.play()

    def update(self, dt):

        self.time += dt

        if self.state != STATE_START:
            self.starttheme.volume = 0

        self.determineState()
        if self.state == STATE_BEGIN:
            self.theme.play(loop=True)
            self.theme.volume = 0.3
            self.state = STATE_ACTIVE

        if self.state == STATE_ACTIVE:
            self.theme.volume = 0.3
            self.handleInput()
            self.wallCollision()

            if self.time > BASE_SPEED:
                self.handleHeadMovement()
                self.handleBodyMovement()
                self.handleGrowth()
                self.time = 0

            self.appleSpawner()
        if self.state == STATE_PAUSED:
            self.theme.volume = 0.0
            self.maintext = GLabel(text="Paused",
                                   font_size=70,
                                   font_name='Arcade.ttf',
                                   x=GAME_WIDTH/2,
                                   y=5*GAME_HEIGHT//8,
                                   linecolor="yellow")
            self.aidtext = GLabel(text=f"Score: {len(self.snake.segments)}\nPress S to Resume",
                                  font_size=50,
                                  font_name='Arcade.ttf',
                                  x=GAME_WIDTH/2,
                                  y=GAME_HEIGHT/3,
                                  linecolor="yellow")

        if self.state == STATE_ACTIVE and self.bodyCollision():
            self.state = STATE_END
            self.maintext = GLabel(text="Game Over",
                                   font_size=70,
                                   font_name='Arcade.ttf',
                                   x=GAME_WIDTH/2,
                                   y=5*GAME_HEIGHT/8,
                                   linecolor="yellow")
            self.aidtext = GLabel(text=f'You Lose\nScore:\n{len(self.snake.segments)}',
                                  font_size=50,
                                  font_name='Arcade.ttf',
                                  x=GAME_WIDTH/2,
                                  y=3*GAME_HEIGHT/8,
                                  linecolor="yellow")
        if self.state == STATE_END:
            self.theme.volume = 0.0
            self.deaththeme.play()
            self.state = STATE_FINISH

        self.last_keys = self.input.keys

    def draw(self):
        GRectangle(x=GAME_WIDTH/2, y=GAME_HEIGHT/2, width=GAME_WIDTH,
                   height=GAME_HEIGHT, fillcolor='black').draw(self.view)

        if self.state == STATE_START:
            self.SnakeImage.draw(self.view)

        if self.state != STATE_START:
            for line in self.lines:
                line.draw(self.view)

            for segment in self.snake.segments:
                segment.draw(self.view)

            if self.apple is not None:
                self.apple.draw(self.view)

        if self.state != STATE_ACTIVE:
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
            # if self.time < 0.2:
            self.eatsound.play()
            for i in range(4):
                last = self.snake.segments[-1]
                x_pos = last.last_x
                y_pos = last.last_y

                self.snake.segments.append(Block(x=x_pos, y=y_pos,
                                                 width=SEGMENT_LENGTH, height=SEGMENT_LENGTH, fillcolor='green'))

    def handleInput(self):

        if 'up' in self.input.keys and self.last_keys == () and self.snake.segments[0].direction != DOWN:
            self.snake.segments[0].direction = UP

        if 'down' in self.input.keys and self.last_keys == () and self.snake.segments[0].direction != UP:
            self.snake.segments[0].direction = DOWN

        if 'left' in self.input.keys and self.last_keys == () and self.snake.segments[0].direction != RIGHT:
            self.snake.segments[0].direction = LEFT

        if 'right' in self.input.keys and self.last_keys == () and self.snake.segments[0].direction != LEFT:
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

        # print(self.apple.left, self.apple.top, len(
        #     self.snake.segments), self.last_keys)

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
        # Starting a game
        if 's' in self.input.keys and self.last_keys == () and (self.state == STATE_START):
            self.state = STATE_BEGIN

        # Pausing midgame
        elif 's' in self.input.keys and self.last_keys == () and self.state == STATE_ACTIVE:
            self.pausesound.play()
            self.state = STATE_PAUSED
        # Resuming a game
        elif 's' in self.input.keys and self.last_keys == () and self.state == STATE_PAUSED:
            self.pausesound.play()
            self.state = STATE_ACTIVE
