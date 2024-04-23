import arcade

class Entity(arcade.Sprite):
    def __init__(self, file_path, health = 1):
        super().__init__()

        self.health = health
        self.speed = 0

        self.texture = arcade.load_texture(file_path, flipped_horizontally=True)
        self.set_hit_box(self.texture.hit_box_points)