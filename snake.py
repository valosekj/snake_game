#########################################################################################
#
# Final project for pyladies course - SNAKE game
#
# Jan Valosek, VER = 16-04-2020
#
#########################################################################################

import pyglet
from random import randint

SQUARE_SIZE = [64, 64]      # tile size in px
WINDOW_SIZE = [640, 640]    # window size in px
green_path = 'images/green.png'
apple_path = 'images/apple.png'
# head_path = 'images/head.png'
head_path = 'images/green.png'


objects = list()            # list of sprite objects (snake parts and food)

# create main window
window = pyglet.window.Window(width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])


def load_image(filename):
    """
    Load image
    :param filename: path to image
    :return: loaded image
    """
    image = pyglet.image.load(filename)
    #image.anchor_x = image.width // 2
    #image.anchor_y = image.height // 2
    return image


green_image = load_image(green_path)
apple_image = load_image(apple_path)
head_image = load_image(head_path)

# Define text properties for counter
label = pyglet.text.Label(color=(255, 0, 0, 255), x=1/2*SQUARE_SIZE[0], y=1/2*SQUARE_SIZE[1], font_size=36)


class Snake:

    def __init__(self):
        self.speed = 1 / 4                                  # snake speed in seconds
        self.snake_positions = [[3, 5], [3, 4], [3, 3]]     # initial snake
        self.direction = 'UP'                               # initial direction of snake movement
        self.score_counter = 0                              # initial score counter
        #self.apple_position = [7, 7]                       # initial food position
        self.place_apple()                                  # generate initial food position randomly

    def move(self):
        """
        Change snake position based on direction.
        Direction is changed by key press.
        """
        new_head = [self.snake_positions[0][0], self.snake_positions[0][1]]
        if self.direction == 'UP':
            new_head[1] += 1
        elif self.direction == 'DOWN':
            new_head[1] -= 1
        elif self.direction == 'RIGHT':
            new_head[0] += 1
        elif self.direction == 'LEFT':
            new_head[0] -= 1

        # Snake ate apple, so generate new apple positions and do not shorten snake
        if new_head == self.apple_position:
            self.place_apple()
            self.score_counter += 1       # increment score counter
            self.increase_speed()
        # END game when snake hits window's edge
        elif new_head[0] < 0 or new_head[0] >= WINDOW_SIZE[0] / SQUARE_SIZE[0] or new_head[1] < 0 or new_head[1] >= \
                WINDOW_SIZE[1] / SQUARE_SIZE[1]:
            self.print_end()
        # END game when snake hits itself
        elif new_head in [i for i in self.snake_positions]:
            self.print_end()
        # Delete last element from snake
        else:
            self.snake_positions.pop()

        self.snake_positions.insert(0, new_head)

    def place_apple(self):
        """
        Generate position of food outside of snake.
        """
        while True:
            self.apple_position = [randint(1, WINDOW_SIZE[0] / SQUARE_SIZE[0] - 1),
                                   randint(1, WINDOW_SIZE[1] / SQUARE_SIZE[1] - 1)]
            # if food is not in snake break loop
            if self.apple_position not in [i for i in self.snake_positions]:
                break

    def increase_speed(self):
        """
        Increase snake speed
        """
        if self.score_counter in range(0,50,5):
            self.speed = self.speed / 1.5
            pyglet.clock._default._current_interval_item.interval = self.speed  # refresh pyglet.clock variable

    def print_end(self):
        """
        End game and print score
        """
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
    objects.append(pyglet.sprite.Sprite(head_image, my_snake.snake_positions[0][0] * SQUARE_SIZE[0],
                                        my_snake.snake_positions[0][1] * SQUARE_SIZE[1], batch=batch))
    # TODO - add head rotation
    #objects[0].rotation = 180

    # SNAKE's BODY
    for x, y in my_snake.snake_positions[1:]:
        # snake_parts - list of sprite objects
        objects.append(pyglet.sprite.Sprite(green_image, x * SQUARE_SIZE[0], y * SQUARE_SIZE[1], batch=batch))

    # FOOD
    objects.append(pyglet.sprite.Sprite(apple_image, my_snake.apple_position[0] * SQUARE_SIZE[0],
                                        my_snake.apple_position[1] * SQUARE_SIZE[1], batch=batch))

    return batch


@window.event
def on_draw():
    window.clear()
    batch = show()
    batch.draw()
    label.text = (str(my_snake.score_counter))  # update counter
    label.draw()                                # display counter


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
