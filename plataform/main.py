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
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of the plater, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

GRAVITY = 1
PLAYER_JUMP_SPEED = 20

#Plater starting position
PLAYER_START_X = 64
PLAYER_START_Y = 225

#Layer names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"

class Colectable(arcade.Sprite):
    def __init__(self, filename: str, value: int):
        super().__init__(filename, COIN_SCALING)
        self.value = value

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

        #Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        #A camera that can be used for scrolling the screen
        self.camera = None

        #A camera that can be used to draw GUI elements
        self.gui_camera = None

        #Keep track of the score
        self.score = 0

        #Do we need to reset the score
        self.reset_score = True

        #Our TileMap Object 
        self.tile_map = None

        #Where is the right edge of the map
        self.end_of_map = 0

        #Level
        self.level = 1

        #Load sounds
        self.collet_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def setup(self):
        """
            Set up the game here. Call this function to restart the game.
        """
        #Set up the camera
        self.camera = arcade.Camera(self.width, self.height)

        #Set up the GUI camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        #Name of the map file to load
        map_name = f":resources:tiled_maps/map2_level_{self.level}.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            LAYER_NAME_PLATFORMS:{
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS:{
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH:{
                "use_spatial_hash": True,
            },
        }

        #Read in the tile map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #Keep track of the socre, make sure to keep the score if player finish level
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Add Player Spritelist before "Foreground" layer. This will make the foreground
        # be drawn after the player, making it appear to be in front of the Player.
        # Setting before using scene.add_sprite allows us to define where the SpriteList
        # will be in the draw order. If we just use add_sprite, it will be appended to the
        # end of the order.
        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)

        #Set up the player, specificaly placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        #Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Platforms"], gravity_constant=GRAVITY
        )

        #Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

    def update_player_speed(self):
        #Calculate speed based on key pressed
        self.player_sprite.change_x = 0

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        
    def center_camera_on_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height/2)

        #Dont't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_key_press(self, key: int, modifiers: int):
        """Caled whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key: int, modifiers: int):
        """Caled when the user release a key"""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()

    def on_update(self, delta_time: float):
        """Movement and game logic"""

        #Move player with the physics engine
        self.physics_engine.update()
     
        #Position the camera
        self.center_camera_on_player()

        #See if we hit any coin
        colectable_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene['Coins'])

        #Loop through each coin (if any) and remove
        for colectable in colectable_hit_list:
            #Remove the coin
            colectable.remove_from_sprite_lists()
            #Play sound
            arcade.play_sound(self.collet_coin_sound)
            #Update score
            self.score += 1

        #Did the player fall of the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)
        
        #Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)

        #Se if the player got to the end of level
        if self.player_sprite.center_x >= self.end_of_map:
            #Advance to the next level
            self.level += 1

            #Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            #Load the next Level
            self.setup()

    def on_draw(self):
        """
            Render the screen
        """
        #Clear the screen to the background color
        self.clear()
        
        #Activate our camera
        self.camera.use()

        #Draw our scene
        self.scene.draw()

        #Active the GUI camera before draw the GUI elements
        self.gui_camera.use()

        #Draw our socre on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18
        )

def main():
    """Main Function"""
    window = MyGame()
    window.setup()
    window.run()

if __name__ == "__main__":
    main()