import arcade

class Camera(arcade.Camera):
    def __init__(self, viewport_width: int = 0, viewport_height: int = 0, window: arcade.Window = None):
        super().__init__(viewport_width, viewport_height, window)

    def center_on_sprite(self, sprite: arcade.SpriteCircle) -> None:
        '''
            Centraliza a camera no sprite entrado.
        '''

        screen_center_x = sprite.center_x - (self.viewport_width/2)
        screen_center_y = sprite.center_y - (self.viewport_height/2)

        # Não deixa a camera sair do mapa
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_x > self.viewport_width:
            screen_center_x = self.viewport_width
        if screen_center_y < 0:
            screen_center_y = 0
        sprite_centered = screen_center_x, screen_center_y

        self.move_to(sprite_centered)
