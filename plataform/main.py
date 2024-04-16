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

# Movement speed of the plater, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

GRAVITY = 1
PLAYER_JUMP_SPEED = 20

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

        #Keep track of the socre
        self.score = 0

        #Load sounds
        self.collet_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def setup(self):
        """
            Set up the game here. Call this function to restart the game.
        """
        #Initialize Scene
        self.scene = arcade.Scene()

        #Set up the camera
        self.camera = arcade.Camera(self.width, self.height)

        #Set up the GUI camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        #Keep track of the socre
        self.score = 0

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

        #Use a loop to place some coins to pick up
        for x in range(128, 1250, 256):
            coin = Colectable(":resources:images/items/coinGold.png", 1)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Colectables", coin)

        #Put some gems to pick up
        coordinates_list = ([256, 288], [512, 288])

        for coordinate in coordinates_list:
            gem = Colectable(":resources:images/items/gemBlue.png", 5)
            gem.position = coordinate
            self.scene.add_sprite("Colectables", gem)

        gem = Colectable(":resources:images/items/gemYellow.png", 10)
        gem.center_x = 768
        gem.center_y = 288
        self.scene.add_sprite("Colectables", gem)

        #Put some creates on the ground
        #This place sprites using a list
        coordinates_list = ([512, 96], [256, 96], [768, 96])

        for coordinate in coordinates_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        #Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene.get_sprite_list("Walls"), gravity_constant=GRAVITY
        )

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
        colectable_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene['Colectables'])

        #Loop through each coin (if any) and remove
        for colectable in colectable_hit_list:
            #Remove the coin
            colectable.remove_from_sprite_lists()
            #Play sound
            arcade.play_sound(self.collet_coin_sound)
            #Update score
            self.score += colectable.value

    def on_draw(self):
        """
            Render the screen
        """
        #Clear the screen to the background color
        self.clear()
        
        #Activate our camera
        self.camera.use()

        #Draw our scene
        self.scene.draw(["Decor", "Colectables", "Walls", "Player"])

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