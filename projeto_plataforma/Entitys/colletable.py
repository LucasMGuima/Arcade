import arcade, math
from abc import abstractmethod
from main import Game as Game

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

    @abstractmethod
    def collected(self):
        pass

class ScoreCollectable(Colletable):
    def __init__(self, filepath: str, cartesian: tuple, tileMap_size: tuple):
        super().__init__(filepath, cartesian, tileMap_size)
        self.value = 0

    def collected(collectable: Colletable, game: Game):
        '''
            Se retira da lista de coletaveis e avisa o jogo para atualizar o score
        '''
        collectable.remove_from_sprite_lists()
        game.increment_score(collectable.value)

class Coin(ScoreCollectable):
    def __init__(self, cartesian: tuple, tileMap_size: tuple):
        super().__init__("../assets/Tiles/tile_0151.png", cartesian, tileMap_size)
        self.value = 1
    
class Gen(ScoreCollectable):
    def __init__(self, cartesian: tuple, tileMap_size: tuple):
        super().__init__("../assets/Tiles/tile_0067.png", cartesian, tileMap_size)
        self.value = 5