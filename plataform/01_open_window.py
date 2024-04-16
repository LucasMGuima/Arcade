"""
    Platformer Game
"""
import arcade
import arcade.color
import arcade.csscolor

#Cosntantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer 0.1"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

class MyGame(arcade.Window):
    """
        Main aplication class
    """
    def __init__(self):
        #Chama a classe pai para configurar a tela
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
        
        #This lists keep track of our sprites. Each sprite should go into a list
        self.wall_list = None
        self.player_list = None
        self.decore_list = None

        #Separete variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def setup(self):
        """
            Set up the game here. Call this function to restart the game.
        """
        #Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.decore_list = arcade.SpriteList()

        #Set up the player, specificaly placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        #Create the ground
        #This place multiple sprites horizontale with a loop
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassmid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        #Put some creates on the ground
        #This place sprites using a list
        coordinates_list = ([512, 96], [256, 96], [768, 96])

        for coordinate in coordinates_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        #Put some decoration in the gorund
        for x in range(0, 512, 54):
            decor = arcade.Sprite(":resources:images/items/ladderTop.png", TILE_SCALING)
            decor.center_x = x
            decor.center_y = 96
            self.decore_list.append(decor)

    def on_draw(self):
        """
            Render the screen
        """
    
        self.clear()
        
        #Draw our sprites
        self.decore_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

def main():
    """Main Function"""
    window = MyGame()
    window.setup()
    window.run()

if __name__ == "__main__":
    main()