import arcade, math
from typing import List
from abc import abstractmethod
from main import Game as Game

class Colletable(arcade.Sprite):
    def __init__(self, filepath: str, cartesian: tuple,  tileMap_size: tuple, TILE_SCALING: int = 1):
        super().__init__()

        self.time_between_frame = 10
        self.animation_timer = 0
        self.cur_texture = 0

        # Carrega a textura
        self.texture = arcade.load_texture(filepath)

        # Corrige a posição do sprite
        self.center_x = math.floor(
            cartesian[0] * TILE_SCALING * tileMap_size[0]
        )
        self.center_y = math.floor(
            (cartesian[1] + 0.7) * (tileMap_size[1] * TILE_SCALING)
        )

    def collision(self) -> None:
        self.collected()

    def update_animation(self, delta_time: float = 1 / 60):
        pass

    @abstractmethod
    def collected(self):
        pass

class ScoreCollectable(Colletable):
    def __init__(self, filepath: str, cartesian: tuple, tileMap_size: tuple):
        super().__init__(filepath, cartesian, tileMap_size)
        self.value = 0

    def collected(self):
        '''
            Se retira da lista de coletaveis e avisa o jogo para atualizar o score
        '''
        self.remove_from_sprite_lists()

class Coin(ScoreCollectable):
    def __init__(self, cartesian: tuple, tileMap_size: tuple):
        super().__init__("resources/Imagens/tile_0151.png", cartesian, tileMap_size)
        self.value = 1

        self.animation = [
            arcade.load_texture("resources/Imagens/tile_0151.png"),
            arcade.load_texture("resources/Imagens/tile_0152.png")
        ]
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self.animation != None:
            self.animation_timer += 1
            if self.animation_timer >= self.time_between_frame:
                self.cur_texture += 1
                if self.cur_texture > len(self.animation)-1:
                    self.cur_texture = 0
                self.texture = self.animation[self.cur_texture]

                self.animation_timer = 0

class Gen(ScoreCollectable):
    def __init__(self, cartesian: tuple, tileMap_size: tuple):
        super().__init__("resources/Imagens/tile_0067.png", cartesian, tileMap_size)
        self.value = 5