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

# Because the physics engine works with small floating point numbers, 
# it often flips above and below zero by small amounts. It is a good idea not to change 
# the animation as the x and y float around zero. For that reason, 
# in this code we have a “dead zone.” We don’t change the animation until it gets outside of that zone.

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
SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_TILE = 0.25

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show in screen, in number of tiles
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

# Close enough to not-moving to have to change the animation to idle
DEAD_ZONE = 0.1

# Constants used to treck if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to move before we change the texture in the wlaking animation
DISTANCE_TO_CHANGE_TEXTURE = 20

# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 750

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going to fast
PLAYER_MAX_HORIZONTAL_SPEED = 225
PLAYER_MAX_VERTICAL_SPEED = 800

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 8000
# Force applied when moving left/right in the ar
PLAYER_MOVE_FORCE_ON_AIR = 900

# Strenght of jump
PLAYER_JUMP_IMPULSE = 2000

# If we use the same gravity for the bullet as everything else, 
# it tends to drop too fast. We could set this to zero if we 
# wanted it to not drop at all.

# How much force to put on the bullet
BULLET_MOVE_FORCE = 4500

# Mass of the bullet
BULLET_MASS = 0.1

# Make bullet less affected by gravity
BULLET_GRAVITY = 300

class PlayerSprite(arcade.Sprite):
    """Player Sprite"""
    def __init__(self):
        """ Init """
        super().__init__()
        
        # Set out scale
        self.scale = SPRITE_SCALING_PLAYER

        main_path = ":resources:images/animated_characters/female_person/femalePerson"

        # Load texture for idle standing
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        # Load texture for walking
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used
        self.hit_box = self.texture.hit_box_points

        # Default face right
        self.character_face_direction = RIGHT_FACING

        # Index of our current texture
        self.cur_texture = 0

        # How far have we traveled horizontally since changing the texture
        self.x_odometer = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """
        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Are we on the ground?
        is_on_ground = physics_engine.is_on_ground(self)

        # Add to the odometer how far we have moved
        self.x_odometer += dx

        # Jumping animation
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return
            
        # Idle animation
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        
        # Have we moved far enought to change texture?
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            # Reset the odometer
            self.x_odometer = 0

            # Advance the walking animation
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
        

class GameWindow(arcade.Window):
    """Main Window"""
    def __init__(self, width, height, title):
        """Create the variavbles"""

        # Init the parent class
        super().__init__(width, height, title)

        # Player sprite
        self.player_sprite: Optional[PlayerSprite] = None

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None

        # Check the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False

        # Physics engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

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
        self.player_sprite = PlayerSprite()

        # Set player location
        grid_x = 1
        grid_y = 1
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2

        # Add player to sprite list
        self.player_list.append(self.player_sprite)

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Create the items
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked """

        bullet = arcade.SpriteSolidColor(20, 5, arcade.color.DARK_YELLOW)
        self.bullet_list.append(bullet)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.position = self.player_sprite.position

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrooling screen, you will also need
        # to add in self.view_botton and self.view_left
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # What is the 1/2 size of the sprite, so we can figure out how far
        # away to spawn the bullet.
        size = max(self.player_sprite.width, self.player_sprite.height)/2

        # Use angel to spawn the bullet away from player in proper direction
        bullet.center_x += size * math.cos(angle)
        bullet.center_y += size * math.sin(angle)

        # Set angle of the bullet
        bullet.angle = math.degrees(angle)

        # Gravity to use for the bullet
        # If we don't use custom gravity, bullet drops too fast, or we have
        # to make it go too fast.
        # Force is in relation to bullet's angle.
        bullet_gravity = (0, -BULLET_GRAVITY)

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.physics_engine.add_sprite(bullet,
                                       mass=BULLET_MASS,
                                       damping=1.0,
                                       friction=0.6,
                                       collision_type="bullet",
                                       gravity=bullet_gravity,
                                       elasticity=0.9)

        # Add force to bullet
        force = (BULLET_MOVE_FORCE, 0)
        self.physics_engine.apply_force(bullet, force)

    def on_key_press(self, symbol: int, modifiers: int):
        """ Called whenever a key is pressed. """
        if symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.UP:
            # find if player is standing on ground
            if self.physics_engine.is_on_ground(self.player_sprite):
                # She is, go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)

    def on_key_release(self, symbol: int, modifiers: int):
        """ Called whenever a key is released. """
        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False


    def on_update(self, delta_time: float):
        """ Movement and game logic """

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Update player forces based on keys pressed
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            if is_on_ground:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_ON_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            if is_on_ground:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_ON_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            # Player's feet are not moving. Therefore up the friction so we stop
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        self.physics_engine.step()

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