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

from typing import Optional
import math
import arcade

SCREEN_TITLE = "PyMunk Plataformer"

# How big are our imagem files?
SPRITE_IMAGE_SIZE = 128

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILE = 0.5

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show in screen, in number of tiles
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

class GameWindow(arcade.Window):
    """Main Window"""
    def __ini__(self, width, height, title):
        """Create the variavbles"""

        # Init the parent class
        super().__init__(width, height, title)

        # Player sprite
        self.player_srpite = Optional[arcade.Sprite] = None

        # Sprite lists we need
        self.player_list = Optional[arcade.SpriteList] = None
        self.wall_list = Optional[arcade.SpriteList] = None
        self.bullet_list = Optional[arcade.SpriteList] = None
        self.item_list = Optional[arcade.SpriteList] = None

        # Check the current state of what key is pressed
        self.left_pressed : bool = False
        self.right_pressed : bool = False

        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up everything with the game """

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Map name
        map_name = ":resources:/tiled_maps/pymunk_test_map.json"

        # Load in TileMap
        tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILE)

        # Pull the sprites layers out of the tile map
        self.wall_list = tile_map.sprite_lists["Platforms"]
        self.item_list = tile_map.sprite_lists["Dynamic Items"]

        # Create player sprite
        self.player_srpite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)

        # Set player location
        grid_x = 1
        grid_y = 1
        self.player_srpite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_srpite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2

        # Add player to sprite list
        self.player_list.append(self.player_srpite)

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

        self.wall_list.draw()
        self.bullet_list.draw()
        self.item_list.draw()
        self.player_list.draw()

def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()