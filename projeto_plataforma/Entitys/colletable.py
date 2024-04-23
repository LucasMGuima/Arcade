import arcade, math

class Colletable(arcade.Sprite):
    def __init__(self, filepath: str, cartesian: tuple,  tileMap_size: tuple, TILE_SCALING: int = 1):
        super().__init__()

        # Carrega a textura
        self.texture = arcade.load_texture(filepath)

        # Corrige a posição do sprite
        self.center_x = math.floor(
            cartesian[0] * TILE_SCALING * tileMap_size[0]
        )
        self.center_y = math.floor(
            (cartesian[1] + 0.7) * (tileMap_size[1] * TILE_SCALING)
        )

    def collected(self):
        self.remove_from_sprite_lists()

class Coin(Colletable):
    def __init__(self, cartesian: tuple, tileMap_size: tuple):
        super().__init__("../assets/Tiles/tile_0151.png", cartesian, tileMap_size)
        self.value = 1
    
    def collected(self) -> int:
        '''
            Se retira da lista de coletaveis e retorna o seu valor
        '''
        super().collected()
        return self.value

