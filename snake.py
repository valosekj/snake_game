#########################################################################################
#
# Final project for pyladies course - SNAKE game
#
# Jan Valosek, VER = 16-04-2020
#
#########################################################################################

import pyglet
from random import randint
from pathlib import Path

SQUARE_SIZE = [64, 64]      # tile size in px
WINDOW_SIZE = [640, 640]    # window size in px
TILES_DIRECTORY = Path('snake-tiles')

objects = list()            # list of sprite objects (snake parts and food)

# create main window
window = pyglet.window.Window(width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

# TODO - snake has anchor in middle -> does not fit properly to game window

def load_image(filename):
    """
    Load image
    :param filename: path to image
    :return: loaded image
    """
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = load_image(path)

# Define text properties for counter
label = pyglet.text.Label(color=(255, 0, 0, 255), x=1/2*SQUARE_SIZE[0], y=1/2*SQUARE_SIZE[1], font_size=36)
# Define text properties for gameover sign
#gameover = pyglet.text.Label(color=(255, 0, 0, 255), x=1/4*WINDOW_SIZE[0], y=1/2*WINDOW_SIZE[1], font_size=25)

class Snake:

    def __init__(self):
        self.speed = 1 / 4                                  # snake speed in seconds
        self.snake_positions = [[3, 5, 0], [3, 4, 0], [3, 3, 0]]     # initial snake
        self.direction = 'UP'                               # initial direction of snake movement
        self.score_counter = 0                              # initial score counter
        #self.apple_position = [7, 7]                       # initial food position
        self.place_apple()                                  # generate initial food position randomly

    def move(self):
        """
        Change snake position based on direction.
        Direction is changed by key press.
        """
        new_head = [self.snake_positions[0][0], self.snake_positions[0][1], self.snake_positions[0][2]]
        if self.direction == 'UP':
            new_head[1] += 1
            new_head[2] = 0
        elif self.direction == 'DOWN':
            new_head[1] -= 1
            new_head[2] = 180
        elif self.direction == 'RIGHT':
            new_head[0] += 1
            new_head[2] = 90
        elif self.direction == 'LEFT':
            new_head[0] -= 1
            new_head[2] = 270

        # Snake ate apple, so generate new apple positions and do not shorten snake
        if new_head[:2] == self.apple_position:
            self.place_apple()
            self.score_counter += 1       # increment score counter
            self.increase_speed()
        # END game when snake hits window's edge
        elif new_head[0] < 0 or new_head[0] >= WINDOW_SIZE[0] / SQUARE_SIZE[0] or new_head[1] < 0 or new_head[1] >= \
                WINDOW_SIZE[1] / SQUARE_SIZE[1]:
            self.print_end()
        # END game when snake hits itself
        elif new_head[:2] in [[x, y] for x, y, _ in self.snake_positions]:
            self.print_end()
        # Delete last element from snake
        else:
            self.snake_positions.pop()

        self.snake_positions.insert(0, new_head)
        print(self.snake_positions)

    def place_apple(self):
        """
        Generate position of food outside of snake.
        """
        while True:
            self.apple_position = [randint(1, WINDOW_SIZE[0] / SQUARE_SIZE[0] - 1),
                                   randint(1, WINDOW_SIZE[1] / SQUARE_SIZE[1] - 1)]
            # if food is not in snake break loop
            if self.apple_position not in [[x, y] for x, y, _ in self.snake_positions]:
                break

    def increase_speed(self):
        """
        Increase snake speed
        """
        if self.score_counter in range(0,50,5):
            self.speed = self.speed / 1.5
            pyglet.clock.unschedule(move)                       # unregister move
            pyglet.clock.schedule_interval(move, self.speed)    # set new interval

    def print_end(self):
        """
        End game and print score
        """
        #gameover.text = ('GAME OVER - SCORE: {}'.format(str(self.score_counter)))
        exit('GAME OVER\nSCORE: {}'.format(str(self.score_counter)))


def show():
    """
    Create batch containing snake parts and food
    :return: batch
    """
    # drawing multiple sprites - https://pyglet.readthedocs.io/en/latest/modules/sprite.html
    # all individual sprites are batched into batch using Batch method
    batch = pyglet.graphics.Batch()

    # SNAKE's HEAD
    objects.append(pyglet.sprite.Sprite(snake_tiles['bottom-tongue'], my_snake.snake_positions[0][0] * SQUARE_SIZE[0],
                                        my_snake.snake_positions[0][1] * SQUARE_SIZE[1], batch=batch))
    # head rotattion
    objects[-1].rotation = my_snake.snake_positions[0][2]

    # TODO - add body and tail rotation

    # SNAKE's BODY
    for x, y, _ in my_snake.snake_positions[1:]:
        # snake_parts - list of sprite objects
        objects.append(pyglet.sprite.Sprite(snake_tiles['end-end'], x * SQUARE_SIZE[0], y * SQUARE_SIZE[1], batch=batch))

    # FOOD
    objects.append(pyglet.sprite.Sprite(snake_tiles['apple'], my_snake.apple_position[0] * SQUARE_SIZE[0],
                                        my_snake.apple_position[1] * SQUARE_SIZE[1], batch=batch))

    return batch


@window.event
def on_draw():
    window.clear()
    batch = show()
    batch.draw()
    label.text = (str(my_snake.score_counter))  # update counter
    label.draw()                                # display counter
    #gameover.draw()


@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.UP:
        my_snake.direction = 'UP'
    elif key_code == pyglet.window.key.DOWN:
        my_snake.direction = 'DOWN'
    elif key_code == pyglet.window.key.RIGHT:
        my_snake.direction = 'RIGHT'
    elif key_code == pyglet.window.key.LEFT:
        my_snake.direction = 'LEFT'


my_snake = Snake()      # create instance of Snake class


def move(dt):
    my_snake.move()     # call periodically method from Snake class in interval defined by speed variable

pyglet.clock.schedule_interval(move, my_snake.speed)

pyglet.app.run()
