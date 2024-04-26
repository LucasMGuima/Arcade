import arcade, math
from Entitys.player import Player as Player
import Utils.enums as enums

class Follower(arcade.Sprite):
    def __init__(self, cartesian: tuple,  tileMap_size: tuple, TILE_SCALING = 1):
        super().__init__()

        self.fallowing = False

        # Carrega a textura
        self.texture = arcade.load_texture("../assets/Tiles/tile_0027.png")

        # Corrige a posição do sprite
        self.center_x = math.floor(
            cartesian[0] * TILE_SCALING * tileMap_size[0]
        )
        self.center_y = math.floor(
            (cartesian[1] + 0.7) * (tileMap_size[1] * TILE_SCALING)
        )

    def collision(self, player: Player):
        if not self.fallowing:
            self.fallowing = True
            player.has_key = True
            self.tracking = player

    def update(self):
        if self.fallowing:
            if self.tracking.facing_direction == enums.Direcitons.RIGHT_FACING:
                self.center_x = self.tracking.center_x - 18
            else:
                self.center_x = self.tracking.center_x + 18
            self.center_y = self.tracking.center_y + 18