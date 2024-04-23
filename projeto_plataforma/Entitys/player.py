import Entitys.entity as entity

class Player(entity.Entity):
    def __init__(self, health=1):
        file_path = "../assets/Tiles/Characters/tile_0000.png"
        super().__init__(file_path, health)