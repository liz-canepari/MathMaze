import arcade
from maze import Maze
from player import Player
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Math Maze Game"

class Main(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.maze = Maze()
        self.player = Player(1, 1)
        self.movement = (0, 0)
        self.current_problem = None
        self.show_problem = False

    def on_draw(self):
        arcade.start_render()
        self.maze.draw()
        self.player.draw()

        if self.show_problem:
            arcade.draw_text(
                self.current_problem["question"],
                SCREEN_WIDTH / 2, 
                SCREEN_HEIGHT / 2, 
                arcade.color.WHITE, 
                font_size= 20,
                anchor_x="center"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.movement = (-1, 0)  
        elif key == arcade.key.DOWN:
            self.movement = (1, 0)  
        elif key == arcade.key.LEFT:
            self.movement = (0, -1)  
        elif key == arcade.key.RIGHT:
            self.movement = (0, 1)
        elif key == arcade.key.E:
            self.current_problem = self.generate_math_problem() 
            self.show_problem = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.movement = (0, 0)

    def generate_math_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(["+", "-"])
        answer = eval(f"{num1} {operation} {num2}")
        return {"question": f"{num1} {operation} {num2} = ?", "answer": answer}
    
    def on_text_input(self, text):
        if self.show_problem:
            try:
                if int(text) == self.current_problem["answer"]:
                    print("Correct answer! The door is open.")
                    self.maze.layout[self.player.row][self.player.col] = 0
                    self.show_problem = False
                else:
                    print("Incorrect answer. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def on_update(self, delta_time):
        if self.movement != (0, 0):
            delta_row, delta_col = self.movement
            self.player.move(delta_row, delta_col, self.maze.layout) 
        
def main():
    game = Main()
    arcade.run()

if __name__ == "__main__":
    main()