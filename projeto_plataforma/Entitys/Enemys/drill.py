import enemy

class Drill(enemy.Enemy):
    def __init__(self):
        file_path = "../assets/Tiles/Characters/tile_0015.png"
        super().__init__(file_path)