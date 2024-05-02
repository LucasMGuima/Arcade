from typing import List
import arcade, random
import resources.Entitys.entity as entity
import resources.Utils.enums as enums
from resources.Utils.enums import Direcitons as dir

class Player(entity.Entity):
    def __init__(
            self,
            sound_jump: arcade.Sound,
            sound_hit: arcade.Sound,
            sound_hurt: arcade.Sound,
            health=1,
            imortal_time=30, 
            speed_on_solid: int = 3, 
            speed_on_water: int = 1, 
            jump_speed: int = 6
        ):
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

        self.time_between_frame = 10

        self.has_key = False

        self.sound_jump = sound_jump
        self.sound_hurt = sound_hurt
        self.sound_hit = sound_hit

        self.moving_animation = [
            self.load_texture_pair("../assets/Tiles/Characters/tile_0000.png"),
            self.load_texture_pair("../assets/Tiles/Characters/tile_0001.png")
        ]

        self.idle_animation = self.load_texture_pair("../assets/Tiles/Characters/tile_0000.png")

    def process_colision(self, collision_list: List[arcade.Sprite], scene: arcade.Scene, tile_map: arcade.TileMap) -> None:
        '''
            Processa a colisão do jogador com outros elementos
        '''

        self.speed = self._speed_on_solid
        for collision in collision_list:
            if (tile_map.get_tilemap_layer(enums.Layers.LAYER_NAME_AGUA) and 
                scene[enums.Layers.LAYER_NAME_AGUA] in collision.sprite_lists):

                # Muda a velocidade do jogador se na agua
                self.speed = self._speed_on_water
                self.process_keychange(False, False)


            # Checa por colisão com um inimigo
            if (tile_map.get_tilemap_layer(enums.Layers.LAYER_NAME_ENEMY) and 
                scene[enums.Layers.LAYER_NAME_ENEMY] in collision.sprite_lists):

                if self.center_y > collision.center_y:
                    self.change_y = self.jump_speed * 0.75
                    if not collision.spike_head:
                        collision.take_damage(1)
                        arcade.play_sound(self.sound_hit, volume=0.5)
                    else:
                        self.health -= 1
                        arcade.play_sound(self.sound_hurt, volume=0.5)
                elif self.can_take_damge:
                    self.health -= 1
                    arcade.play_sound(self.sound_hurt, volume=0.5)
                    self.can_take_damge = False


            # Checa por colisão com espinhos
            if (tile_map.get_tilemap_layer(enums.Layers.LAYER_NAME_ESPINHOS) and
                scene[enums.Layers.LAYER_NAME_ESPINHOS] in collision.sprite_lists):

                if self.change_y < 0 and self.can_take_damge:
                    self.health -= 1
                    arcade.play_sound(self.sound_hurt, volume=0.5)
                    self.can_take_damge = False
                else:
                    self.can_take_damge = True

            # Checa por uma colisão com trampolins
            if (tile_map.get_tilemap_layer(enums.Layers.LAYER_NAME_TRAMPOLINS) and
                scene[enums.Layers.LAYER_NAME_TRAMPOLINS] in collision.sprite_lists):

                if (self.center_y > collision.center_y) and self.change_y != 0:
                    self.change_y = self.jump_speed * 1.5

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
                arcade.play_sound(self.sound_jump, volume=0.5)
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