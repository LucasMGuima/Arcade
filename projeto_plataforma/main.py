import arcade

# Constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_NAME = "Projeto Plataforma"

# Constanres usadas para escalhonar os sprites de seu tamanho original
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Nome das layer
LAYER_NAME_PLATAFORMS = "Plataformas"
LAYER_NAME_COLETAVEIS = "Coletaveis"
LAYER_NAME_AGUA = "Agua"
LAYER_NAME_PLAYER = "Player"

# Physics
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30


class Game(arcade.Window):
    def __init__(self):
        super().__init__()

        # Variavies
        self.tile_map = None
        self.scene = None
        
        self.player_sprite = None
        self.score = 0

        self.physics_engine = None

    def setup(self):
        map_name = "assets/map1.tmx"

        layer_options = {
            LAYER_NAME_PLATAFORMS: {
                "use_spatial_hash": True
            },
            LAYER_NAME_COLETAVEIS: {
                "use_spatial_hash": True
            },
            LAYER_NAME_AGUA: {
                "use_spatial_hash": True
            }
        }

        # Carrega o TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        # Carrega a scena
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        """self.score = 0
        path = "./assets/player.png"
        self.player_sprite = arcade.Sprite(path, TILE_SCALING)
        self.player_sprite.center_x = 27
        self.player_sprite.center_y = 27"""
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            walls=self.scene[LAYER_NAME_PLATAFORMS],
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()

        self.scene.draw()

def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()