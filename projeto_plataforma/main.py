import arcade
import Entitys.Enemys.enemy as Enemy
import Entitys.player
import Entitys.colletable as collect
import Entitys.follower as follower
import Utils.camera as camera
import Utils.enums as enums

# Constantes
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 360
SCREEN_NAME = "Projeto Plataforma"

# Constanres usadas para escalhonar os sprites de seu tamanho original
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 18
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Physics
PLAYER_MOVEMENT_SPEED_SOLID = 3
PLAYER_MOVEMENT_SPEED_WATER = 1
GRAVITY = 1
PLAYER_JUMP_SPEED = 14

# Player start
PLAYER_START_X = 2
PLAYER_START_Y = 4

PLAYER_LIFE = 5
PLAYER_IMORTAL_TIME = 30

class Game(arcade.View):
    def __init__(self):
        super().__init__()

        # Variavies
        self.tile_map = None
        self.scene = None
        
        # Camera
        self.camera = None
        self.gui_camera = None
        self.end_of_map = 0
        
        # Player
        self.player_sprite = None
        self.score = 0
        self.player_imortal_timer = 0
        self.score = 0

        self.physics_engine = None

        # Set background color
        arcade.set_background_color(arcade.color.BLUE_GRAY)

    def setup(self):
        # Reset score
        self.score = 0

        # Configura as cameras
        self.camera = camera.Camera(self.window.width, self.window.height)
        self.gui_camera = camera.Camera(self.window.width, self.window.height)

        # Carrega o TileMap
        map_name = "../assets/Tiled/map_1.tmx"

        layer_options = {
            enums.Layers.LAYER_NAME_PLATAFORMS: {
                "use_spatial_hash": True
            },
            enums.Layers.LAYER_NAME_DECORACAO: {
                "use_spatial_hash": True
            },
            enums.Layers.LAYER_NAME_AGUA: {
                "use_spatial_hash": True
            },
            enums.Layers.LAYER_NAME_ESCADA: {
                "use_spatial_hash": True
            },
            enums.Layers.LAYER_NAME_COLLETABLES: {
                "use_spatial_hash": True
            },
            enums.Layers.LAYER_NAME_DECORACAO_DETALHES: {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        # Carrega a scena
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Player
        self.player_sprite = Entitys.player.Player(health=PLAYER_LIFE, jump_speed=PLAYER_JUMP_SPEED)
        self.player_imortal_timer = 0
        self.player_sprite.center_x = (
            self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y
        )
        self.scene.add_sprite_list_before(enums.Layers.LAYER_NAME_PLAYER, enums.Layers.LAYER_NAME_AGUA, False, self.player_sprite)


        # Enemies
        enemies_layer = self.tile_map.object_lists[enums.Layers.LAYER_NAME_ENEMY]

        for object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                object.shape[0], object.shape[1]
            )

            enemy_type = object.type.lower()
            tileMap_size = (self.tile_map.tile_width, self.tile_map.tile_height)

            if enemy_type == "flying":
                enemy = Enemy.Flying(object, cartesian, tileMap_size)
            elif enemy_type == "stomping":
                enemy = Enemy.Stomping(object, cartesian, tileMap_size)
            elif enemy_type == "drill":
                enemy = Enemy.Drill(object, cartesian, tileMap_size)

            self.scene.add_sprite(enums.Layers.LAYER_NAME_ENEMY, enemy)

        # Coletaveis
        colletables_layer = self.tile_map.object_lists[enums.Layers.LAYER_NAME_COLLETABLES]

        for object in colletables_layer:
            cartesian = self.tile_map.get_cartesian(
                object.shape[0], object.shape[1]
            )

            colletable_type = object.type.lower()
            tileMap_size = (self.tile_map.tile_width, self.tile_map.tile_height)

            #TODO: Separar a layer de coletaveis em coletaveis e containers
            if colletable_type == enums.ObjectTypes.COIN:
                colletable = collect.Coin(cartesian, tileMap_size)
            elif colletable_type == enums.ObjectTypes.GEN:
                colletable = collect.Gen(cartesian, tileMap_size)
            elif colletable_type == enums.ObjectTypes.KEY:
                colletable = follower.Follower(cartesian, tileMap_size)
            
            self.scene.add_sprite(enums.Layers.LAYER_NAME_COLLETABLES, colletable)

        # Carrega o motor
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.scene[enums.Layers.LAYER_NAME_PLATAFORMS],
            ladders=self.scene[enums.Layers.LAYER_NAME_ESCADA],
            gravity_constant=GRAVITY
        )

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        # Posiciona a camera
        self.camera.center_on_sprite(self.player_sprite)

        # Atualiza as layer da scena
        self.scene.update([
            enums.Layers.LAYER_NAME_ENEMY,
            enums.Layers.LAYER_NAME_COLLETABLES
        ])

        # Atualiza os inimgos
        for enemy in self.scene[enums.Layers.LAYER_NAME_ENEMY]:
            # Atualiza a direção
            enemy.update_direction()

        # Player collision
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[enums.Layers.LAYER_NAME_AGUA],
                self.scene[enums.Layers.LAYER_NAME_ENEMY],
                self.scene[enums.Layers.LAYER_NAME_ESPINHOS],
                self.scene[enums.Layers.LAYER_NAME_TRAMPOLINS]
            ]
        )

        # Timer de imortalidade pos dano do jogador
        if not self.player_sprite.can_take_damge:
            self.player_imortal_timer += 1
            if self.player_imortal_timer >= self.player_sprite.imortal_time:
                self.player_sprite.can_take_damge = True
                self.player_imortal_timer = 0

        # Processa a colisão do jogador
        self.player_sprite.process_colision(player_collision_list, self.scene)

        # Colisão dos coletaveis
        collectabels_collision_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene[enums.Layers.LAYER_NAME_COLLETABLES]
        )

        for collectable in collectabels_collision_list:
            if "follower" in str(type(collectable)):
                collectable.collision(self.player_sprite)
            else:
                collectable.collision()
                self.score += collectable.value


        # Checa se o jogador chegou a uma porta
        door_collision = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.scene[enums.Layers.LAYER_NAME_PORTAS]
        )

        for door in door_collision:
            # Se o jogador tiver uma chave vai pro próximo nivel
            if self.player_sprite.has_key:
                self.setup()

        # Checa se o jogador morreu
        if self.player_sprite.health <= 0:
            self.setup()

        # Atualiza as animações
        self.scene.update_animation(
            delta_time,
            [
                enums.Layers.LAYER_NAME_PLAYER,
                enums.Layers.LAYER_NAME_ENEMY,
                enums.Layers.LAYER_NAME_COLLETABLES
            ]
        )
                

    def on_draw(self):
        self.clear()

        # Ativa a camera
        self.camera.use()

        self.scene.draw()

        # Ativa GUI
        self.gui_camera.use()
        self.draw_hearts()
        self.draw_score()

    def increment_score(self, value: int) -> None:
        '''
            Incrementa a pontuação atual
        '''
        self.score += value

    def draw_score(self):
        score_text = f"{self.score}"
        pos_num = 0
        for num in score_text:
            arcade.draw_texture_rectangle(
                texture = arcade.load_texture(f"../assets/Tiles/tile_016{num}.png"),
                center_x = 10 * (pos_num+1),
                center_y = SCREEN_HEIGHT - 34,
                width=18,
                height=18
            )
            pos_num += 1

    def draw_hearts(self):
        health = self.player_sprite.health

        qtd_full_heart = health//2
        qtd_halth_heart = health%2

        # Desenha os corações cheios
        for heart in range(qtd_full_heart):
            arcade.draw_texture_rectangle(
                center_x = 18 * (heart+1),
                center_y = SCREEN_HEIGHT - 18,
                texture = arcade.load_texture("../assets/Tiles/tile_0044.png"),
                width=18,
                height=18
            )

        # Desenha os corações meiados
        for heart in range(qtd_halth_heart):
            arcade.draw_texture_rectangle(
                center_x = 18 * (heart+qtd_full_heart+1),
                center_y = SCREEN_HEIGHT - 18,
                texture = arcade.load_texture("../assets/Tiles/tile_0045.png"),
                width=18,
                height=18
            )

    def on_key_press(self, key: int, modifiers: int):
        
        if key == arcade.key.R:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_spritedown_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.right_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.left_pressed = True

        self.player_sprite.process_keychange(self.physics_engine.is_on_ladder(), self.physics_engine.can_jump(10))

    def on_key_release(self, key: int, modifiers: int):
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.up_pressed = False
            self.player_sprite.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.down_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.right_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.left_pressed = False

        self.player_sprite.process_keychange(self.physics_engine.is_on_ladder(), self.physics_engine.can_jump(10))

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_NAME)
    gameWindow = Game()
    window.show_view(gameWindow)
    arcade.run()

if __name__ == "__main__":
    main()