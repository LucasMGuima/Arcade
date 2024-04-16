"""
    Platformer Game
"""
import arcade
import arcade.color
import arcade.csscolor

#Cosntantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SCREEN_TITLE = "Platformer 0.1"

class MyGame(arcade.Window):
    """
        Main aplication class
    """
    def __init__(self):
        #Chama a classe pai para configurar a tela
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
        
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def setup(self):
        """
            Set up the game here. Call this function to restart the game.
        """
        pass

    def on_draw(self):
        """
            Render the screen
        """

        self.clear()
        #Code to draw the screen goes here

def main():
    """Main Function"""
    window = MyGame()
    window.setup()
    window.run()

if __name__ == "__main__":
    main()