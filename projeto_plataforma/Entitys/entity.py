import arcade

class Entity(arcade.Sprite):
    def __init__(self, file_path):
        super().__init__()

        self.texture = arcade.load_texture(file_path)
        self.set_hit_box(self.texture.hit_box_points)