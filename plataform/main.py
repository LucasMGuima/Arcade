"""
    Platformer Game
"""
import arcade
import arcade.color
import arcade.csscolor
import arcade.key

#Cosntantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer 0.1"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Movement speed of the plater, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    """
        Main aplication class
    """
    def __init__(self):
        #Chama a classe pai para configurar a tela
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
        
        #Our Scene object
        self.scene = None

        #Separete variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def setup(self):
        """
            Set up the game here. Call this function to restart the game.
        """
        #Initialize Scene
        self.scene = arcade.Scene()

        #Create the Sprite lists
        self.scene.add_sprite_list("Decore")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")
        
         #Put some decoration in the ground
        for x in range(0, 512, 54):
            decor = arcade.Sprite(":resources:images/items/ladderTop.png", TILE_SCALING)
            decor.center_x = x
            decor.center_y = 96
            self.scene.add_sprite("Decor", decor)

        #Set up the player, specificaly placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        #Create the ground
        #This place multiple sprites horizontale with a loop
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassmid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        #Put some creates on the ground
        #This place sprites using a list
        coordinates_list = ([512, 96], [256, 96], [768, 96])

        for coordinate in coordinates_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        #Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

    def on_key_press(self, key: int, modifiers: int):
        """Caled whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int):
        """Caled when the user release a key"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        """Movement and game logic"""

        # Move player with the physics engine
        self.physics_engine.update()
     
    def on_draw(self):
        """
            Render the screen
        """
    
        self.clear()
        
        #Draw our scene
        self.scene.draw(["Decor", "Walls", "Player"])

def main():
    """Main Function"""
    window = MyGame()
    window.setup()
    window.run()

if __name__ == "__main__":
    main()