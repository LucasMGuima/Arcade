import enemy

class Stomping(enemy.Enemy):
    def __init__(self):
        file_path = "../assets/Tiles/Characters/tile_0021.png"
        super().__init__(file_path)