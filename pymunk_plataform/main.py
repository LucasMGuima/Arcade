# Problemas comuns usando Pymunk:
# Object overlap - 
#   A fast moving object is allowed to overlap with the object it collides with, 
#   and Pymunk will push them apart later.
#
# Pass-through - 
#   A fast moving object can pass through another object if its speed is so quick 
#   it never overlaps the other object between frames.
#
# When stepping the physics engine forward in time, 
# the default is to move forward 1/60th of a second. Whatever increment is picked, 
# increments should always be kept the same. Don’t use the variable delta_time from 
# the update method as a unit, or results will be unstable and unpredictable. For a 
# more accurate simulation, you can step forward 1/120th of a second twice per frame. 
# This increases the time required, but takes more time to calculate.
#
# A sprite moving across a floor made up of many rectangles can get “caught” on the edges. 
# The corner of the player sprite can get caught the corner of the floor sprite. To get around this, 
# make sure the hit box for the bottom of the player sprite is rounded. 
# Also, look into the possibility of merging horizontal rows of sprites.

""""
    Example of Pymunk Physiscs Engine Plataformer
"""

import arcade

SCREEN_TITLE = "PyMunk Plataformer"

# Size of screen to show, in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GameWindow(arcade.Window):
    """Main Window"""
    def __ini__(self, width, height, title):
        """Create the variavbles"""

        #Init the parent class
        super().__init__(width, height, title)

    def setup(self):
        """ Set up everything with the game """
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        """ Called whenever a key is pressed. """
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        """ Called whenever a key is released. """
        pass

    def on_update(self, delta_time: float):
        """ Movement and game logic """
        pass

    def on_draw(self):
        """ Draw everting """
        self.clear()

def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()