from typing import List
import arcade
import Entitys.entity as entity
import Utils.enums as enums

class Player(entity.Entity):
    def __init__(self, health=1, imortal_time=30, speed_on_solid: int = 3, speed_on_water: int = 1, jump_speed: int = 6):
        file_path = "../assets/Tiles/Characters/tile_0000.png"
        super().__init__(file_path, health)

        self._speed_on_solid = speed_on_solid
        self._speed_on_water = speed_on_water

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.jump_needs_reset = False
        self.jump_speed = jump_speed

        self.can_take_damge = True
        self.imortal_time = imortal_time #60fps

    def process_colision(self, collision_list: List[arcade.Sprite], scene: arcade.Scene) -> None:
        '''
            Processa a colisão do jogador com outros elementos
        '''

        self.speed = self._speed_on_solid
        for collision in collision_list:
            if scene[enums.Layers.LAYER_NAME_AGUA] in collision.sprite_lists:
                # Muda a velocidade do jogador se na agua
                self.speed = self._speed_on_water
                self.process_keychange(False, False)

            # Checa por colisão com um inimigo
            if scene[enums.Layers.LAYER_NAME_ENEMY] in collision.sprite_lists:
                if self.can_take_damge:
                    self.health -= 1
                    self.can_take_damge = False

    def process_keychange(self, on_ladder: bool, can_jump: bool) -> None:
        '''
            Processa a alteração das teclas cima/baixo e esquerda/direita ou quando nos movemos ou saimos de uma escada.
        '''
        # Cima/Baixo
        if self.up_pressed and not self.down_pressed:
            if on_ladder:
                self.change_y = self.speed
            elif(can_jump and not self.jump_needs_reset):
                self.change_y = self.jump_speed
                self.jump_needs_reset = True
        elif self.down_pressed and not self.up_pressed:
            if on_ladder:
                self.change_y = -self.speed

        # Cima/Baixo quando em uma escada e não se movendo
        if on_ladder:
            if not self.up_pressed and not self.down_pressed:
                self.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.change_y = 0

        # Esquerda/Direita
        if self.right_pressed and not self.left_pressed:
            self.change_x = self.speed
        elif self.left_pressed and not self.right_pressed:
            self.change_x = -self.speed
        else:
            self.change_x = 0
