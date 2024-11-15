import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Math Maze Game"

class Main(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        arcade.start_render()
        
def main():
    game = Main()
    arcade.run()

if __name__ == "__main__":
    main()