import Entitys.entity as entity

class Enemy(entity.Entity):
    def __init__(self, file_path):
        super().__init__(file_path)

class Flying(Enemy):
    def __init__(self):
        file_path = "../assets/Tiles/Characters/tile_0024.png"
        super().__init__(file_path)

class Drill(Enemy):
    def __init__(self):
        file_path = "../assets/Tiles/Characters/tile_0015.png"
        super().__init__(file_path)

class Stomping(Enemy):
    def __init__(self):
        file_path = "../assets/Tiles/Characters/tile_0021.png"
        super().__init__(file_path)