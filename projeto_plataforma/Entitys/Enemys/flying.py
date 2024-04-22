import enemy

class Flying(enemy.Enemy):
    def __init__(self):
        file_path = "../assets/Tiles/Characters/tile_0024.png"
        super().__init__(file_path)