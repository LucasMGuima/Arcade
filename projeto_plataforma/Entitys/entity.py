import arcade
from Utils.enums import Direcitons as dir

class Entity(arcade.Sprite):
    def __init__(self, file_path, health = 1):
        super().__init__()

        self.texture = arcade.load_texture(file_path, flipped_horizontally=True)
        self.set_hit_box(self.texture.hit_box_points)

        self.health = health
        self.speed = 0

        self.facing_direction = dir.RIGHT_FACING
        
        self.cur_texture = 0
        self.animation_timer = 0
        self.time_between_frame = 10

        self.moving_animation = None
        self.idle_animation = None

    def load_texture_pair(self, filename: str) -> tuple:
        '''
            Carrega o par de textura, com a sgunda sendo uma imagem espelhada
        '''
        return[
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x > 0 and self.facing_direction == dir.LEFT_FACING:
            self.facing_direction = dir.RIGHT_FACING
        elif self.change_x < 0 and self.facing_direction == dir.RIGHT_FACING:
            self.facing_direction = dir.LEFT_FACING

        # Animação parado, se tiver
        if self.idle_animation != None:
            if self.change_x == 0:
                self.texture = self.idle_animation[self.facing_direction]
                return

        # Animação de movimento, se tiver
        if self.moving_animation != None:
            self.animation_timer += 1
            if self.animation_timer >= self.time_between_frame:
                self.cur_texture += 1
                if self.cur_texture > len(self.moving_animation)-1:
                    self.cur_texture = 0
                self.texture = self.moving_animation[self.cur_texture][self.facing_direction]

                self.animation_timer = 0