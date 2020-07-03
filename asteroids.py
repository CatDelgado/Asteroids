import random, math, arcade, os
from typing import cast
from PIL import Image

# Sprite info
SPRITE_SCALING = 0.40
SPRITE_IMG = Image.open("ship_transparent.png")
SPRITE_SIZE = (SPRITE_IMG.width * SPRITE_SCALING, SPRITE_IMG.height * SPRITE_SCALING)

# Screen info
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OFFSCREEN_SPACE = 200
SCREEN_TITLE = "ASTEROIDS! \n based off of the original Atari Asteroids"

# Screen limits and speed
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
MOVEMENT_SPEED = 5

ASTEROID_MIN = 12
ASTEROID_MAX = 20
ASTEROID_COUNT = random.randint(ASTEROID_MIN, ASTEROID_MAX)
ASTEROID_SIZES = [1, 2, 3]

class Ship(arcade.Sprite):

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        # self.center_x = random.choice([random.randint(), random.randint()])

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        if self.center_x < -OFFSCREEN_SPACE:
            self.center_x = SCREEN_WIDTH + OFFSCREEN_SPACE
        elif self.center_x > SCREEN_WIDTH + OFFSCREEN_SPACE:
            self.center_x = -OFFSCREEN_SPACE

        if self.center_y < -OFFSCREEN_SPACE:
            self.center_y = SCREEN_HEIGHT + OFFSCREEN_SPACE
        elif self.center_y > SCREEN_HEIGHT + OFFSCREEN_SPACE:
            self.center_y = -OFFSCREEN_SPACE

    def size(self):
        return SPRITE_SIZE


class Asteroid(arcade.Sprite):
    def __init__(self, image, size, pos):
        scale = 0
        if size == 1:
            scale = random.uniform(0.2, 0.3)
        elif size == 2:
            scale = random.uniform(0.4, 0.5)
        else:
            scale = random.uniform(0.6, 0.7)

        super().__init__(image, scale)

        self.angle = random.randint(0, 359)
        self.reset_position(pos)        

    def move(self):
        self.center_x += self.rand_x_speed
        self.center_y += self.rand_y_speed

    def reset_position(self, pos):
        if pos == 0:
            self.center_x = -OFFSCREEN_SPACE
            self.center_y = random.randint(-OFFSCREEN_SPACE, SCREEN_HEIGHT + OFFSCREEN_SPACE)
            self.rand_x_speed = random.randint(1, 3)
            self.rand_y_speed = random.randint(1, 3) * random.choice([-1, 1])
        elif pos == 1:
            self.center_x = random.randint(-OFFSCREEN_SPACE, SCREEN_WIDTH + OFFSCREEN_SPACE)
            self.center_y = -OFFSCREEN_SPACE
            self.rand_x_speed = random.randint(1, 3) * random.choice([-1, 1])
            self.rand_y_speed = random.randint(1, 3)
        elif pos == 2:
            self.center_x = SCREEN_WIDTH + OFFSCREEN_SPACE
            self.center_y = random.randint(-OFFSCREEN_SPACE, SCREEN_HEIGHT + OFFSCREEN_SPACE)
            self.rand_x_speed = -random.randint(1, 3)
            self.rand_y_speed = random.randint(1, 3) * random.choice([-1, 1])
        else:
            self.center_x = random.randint(-OFFSCREEN_SPACE, SCREEN_WIDTH + OFFSCREEN_SPACE)
            self.center_y = SCREEN_HEIGHT + OFFSCREEN_SPACE
            self.rand_x_speed = random.randint(1, 3) * random.choice([-1, 1])
            self.rand_y_speed = -random.randint(1, 3)

        self.rand_x_speed /= 3
        self.rand_y_speed /= 3

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.asteroid_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Ship("ship_transparent.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)


        for i in range(ASTEROID_COUNT):
            asteroid_size = ASTEROID_SIZES[random.randint(0, 2)]
            asteroid_spawn_position = random.randint(0, 3)
            asteroid = Asteroid("asteroid.png", asteroid_size, asteroid_spawn_position)

            self.asteroid_list.append(asteroid)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()
        self.asteroid_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        angle_rad = math.radians(self.player_sprite.angle)
        
        if self.up_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED * math.cos(angle_rad)
            self.player_sprite.change_x = -MOVEMENT_SPEED * math.sin(angle_rad)
            
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_angle = 5
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_angle = -5

        for asteroid in self.asteroid_list:
            asteroid.move()

            asteroid_off_x = asteroid.center_x < -OFFSCREEN_SPACE or \
                asteroid.center_x > SCREEN_WIDTH + OFFSCREEN_SPACE
            asteroid_off_y = asteroid.center_y < -OFFSCREEN_SPACE or \
                asteroid.center_y > SCREEN_HEIGHT + OFFSCREEN_SPACE
            if asteroid_off_x or asteroid_off_y:
                asteroid.reset_position(random.randint(0, 3))

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.player_sprite.change_angle = 0
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.player_sprite.change_angle = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()