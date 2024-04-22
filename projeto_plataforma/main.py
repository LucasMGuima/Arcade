import arcade

# Constantes
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 360
SCREEN_NAME = "Projeto Plataforma"

# Constanres usadas para escalhonar os sprites de seu tamanho original
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 18
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Nome das layer
LAYER_NAME_PLATAFORMS = "Plataformas"
LAYER_NAME_ESCADA = "Escada"
LAYER_NAME_DECORACAO = "Decoracao"
LAYER_NAME_AGUA = "Agua"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMY = "Inimigos"

# Physics
PLAYER_MOVEMENT_SPEED_SOLID = 3
PLAYER_MOVEMENT_SPEED_WATER = 1
GRAVITY = 1
PLAYER_JUMP_SPEED = 14

# Player start
PLAYER_START_X = 2
PLAYER_START_Y = 4


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME)

        # Variavies
        self.tile_map = None
        self.scene = None
        
        self.player_sprite = None
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.jump_needs_reset = False
        self.score = 0
        self.player_speed = PLAYER_MOVEMENT_SPEED_SOLID

        self.physics_engine = None

        # Set background color
        arcade.set_background_color(arcade.color.BLUE_GRAY)

    def setup(self):
        # Carrega o TileMap
        map_name = "../assets/Tiled/map_1.tmx"

        layer_options = {
            LAYER_NAME_PLATAFORMS: {
                "use_spatial_hash": True
            },
            LAYER_NAME_DECORACAO: {
                "use_spatial_hash": True
            },
            LAYER_NAME_AGUA: {
                "use_spatial_hash": True
            },
            LAYER_NAME_ESCADA: {
                "use_spatial_hash": True
            },
            LAYER_NAME_ENEMY: {
                "use_spatial_hash": False
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        # Carrega a scena
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Player
        sprite_name = "../assets/Tiles/Characters/tile_0000.png"
        self.player_sprite = arcade.Sprite(sprite_name, flipped_horizontally=True)
        self.player_sprite.center_x = (
            self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y
        )
        self.scene.add_sprite_list_before(LAYER_NAME_PLAYER, LAYER_NAME_AGUA, False, self.player_sprite)

        # Carrega o motor
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.scene[LAYER_NAME_PLATAFORMS],
            ladders=self.scene[LAYER_NAME_ESCADA],
            gravity_constant=GRAVITY
        )

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        # Player collision
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_AGUA],
            ]
        )

        # Reset player speed
        self.player_speed = PLAYER_MOVEMENT_SPEED_SOLID
        for collsion in player_collision_list:
            if self.scene[LAYER_NAME_AGUA] in collsion.sprite_lists:
                # Change player speed if on water
                self.player_speed = PLAYER_MOVEMENT_SPEED_WATER
                self.process_keychange()
                

    def on_draw(self):
        self.clear()

        self.scene.draw()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = self.player_speed
            elif(self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -self.player_speed
        
        # Process up/down when on ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.player_speed
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.player_speed
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key: int, modifiers: int):
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True

        self.process_keychange()

    def on_key_release(self, key: int, modifiers: int):
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False

        self.process_keychange()

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()