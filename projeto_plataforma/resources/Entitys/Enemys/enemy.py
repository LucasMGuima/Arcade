import resources.Entitys.entity as entity
import arcade, math, resources.Utils.enums
from resources.Utils.enums import Direcitons as dir

class Enemy(entity.Entity):
    def __init__(self, file_path, object: arcade.TiledObject, cartesian: tuple, tileMap_size: tuple, TILE_SCALING = 1):
        super().__init__(file_path)

        # Corrige a posição do sprite
        self.center_x = math.floor(
            cartesian[0] * TILE_SCALING * tileMap_size[0]
        )
        self.center_y = math.floor(
            (cartesian[1] + 0.7) * (tileMap_size[1] * TILE_SCALING)
        )

        # Carrega as propriedas
        p = resources.Utils.enums.Propriets()
        if p.BOUNDARY_LEFT in object.properties:
            self.boundary_left = object.properties[p.BOUNDARY_LEFT]
        if p.BOUNDARY_RIGHT in object.properties:
            self.boundary_right = object.properties[p.BOUNDARY_RIGHT]
        if p.CHANGE_X in object.properties:
            self.change_x = object.properties[p.CHANGE_X]
        self.spike_head = False

    def update_direction(self) -> None:
        '''
            Ve se o inimigo atingil algum limite latera e altera a direção
        '''
        if(
            self.boundary_right
            and self.right > self.boundary_right
            and self.change_x > 0
        ):
            # Acerto o limite direto, altera a direção
            self.change_x *= -1
        
        if(
            self.boundary_left
            and self.left < self.boundary_left
            and self.change_x < 0
        ):
            # Acerto o limite esquerdo, altera adireção
            self.change_x *= -1

    def take_damage(self, damage: int) -> None:
        self.health -= damage
            
        if self.health <= 0: self.remove_from_sprite_lists()

class Flying(Enemy):
    def __init__(self, object: arcade.TiledObject, cartesian: tuple, tileMap_size: tuple):
        file_path = "../assets/Tiles/Characters/tile_0024.png"
        super().__init__(file_path, object, cartesian, tileMap_size)

        self.moving_animation = [
            self.load_texture_pair("../assets/Tiles/Characters/tile_0024.png"),
            self.load_texture_pair("../assets/Tiles/Characters/tile_0025.png"),
            self.load_texture_pair("../assets/Tiles/Characters/tile_0026.png")
        ]

        self.health = 1

class Drill(Enemy):
    def __init__(self, object: arcade.TiledObject, cartesian: tuple, tileMap_size: tuple):
        file_path = "../assets/Tiles/Characters/tile_0015.png"
        super().__init__(file_path, object, cartesian, tileMap_size)

        self.moving_animation = [
            self.load_texture_pair("../assets/Tiles/Characters/tile_0015.png"),
            self.load_texture_pair("../assets/Tiles/Characters/tile_0016.png")
        ]

        self.idle_animation = self.load_texture_pair("../assets/Tiles/Characters/tile_0017.png")

        self.health = 2
        self.spike_head = True

class Stomping(Enemy):
    def __init__(self, object: arcade.TiledObject, cartesian: tuple, tileMap_size: tuple):
        file_path = "../assets/Tiles/Characters/tile_0021.png"
        super().__init__(file_path, object, cartesian, tileMap_size)

        self.moving_animation = [
            self.load_texture_pair("../assets/Tiles/Characters/tile_0021.png"),
            self.load_texture_pair("../assets/Tiles/Characters/tile_0022.png")
        ]

        self.idle_animation = self.load_texture_pair("../assets/Tiles/Characters/tile_0023.png")

        self.health = 4