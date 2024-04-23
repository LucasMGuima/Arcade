import Entitys.entity as entity

class Player(entity.Entity):
    def __init__(self, health=1, imortal_time=30):
        file_path = "../assets/Tiles/Characters/tile_0000.png"
        super().__init__(file_path, health)

        self.can_take_damge = True
        self.imortal_time = imortal_time #60fps