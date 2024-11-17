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
        arcade.set_background_color(arcade.color.GRAY)
        self.maze = Maze()
        self.player = Player(1, 1)
        self.movement = (0, 0)
        self.current_problem = None
        self.show_problem = False
        self.input_text = ""
        self.show_door_message = False
        self.movement_cooldown = 0
        self.movement_speed = 0.2
        self.feedback_message = ""
        self.feedback_timer = 0

    def on_draw(self):
        arcade.start_render()
        self.maze.draw()
        self.player.draw()

        if self.show_door_message:
            arcade.draw_text(
            "You encountered a door! Press 'E' to try opening it.",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 50,
            arcade.color.GRANNY_SMITH_APPLE,
            font_size=18,
            anchor_x="center"
        )

        if self.show_problem:
            rect_width = 400
            rect_height = 200
            rect_x = SCREEN_WIDTH / 2
            rect_y = SCREEN_HEIGHT / 2
            arcade.draw_rectangle_filled(
            rect_x, rect_y, rect_width, rect_height, arcade.color.WHITE_SMOKE
            )

            arcade.draw_rectangle_outline(
                rect_x, rect_y, rect_width, rect_height, arcade.color.BLACK, 3
            )

            arcade.draw_text(
                self.current_problem["question"],
                rect_x,
                rect_y + 30,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                f"Enter your answer: {self.input_text}",
                rect_x,
                rect_y - 30,
                arcade.color.DIM_GRAY,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )

        if self.feedback_timer > 0:
            arcade.draw_text(
            self.feedback_message,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 4,
            arcade.color.RED,
            font_size=18,
            anchor_x="center"
            )
        

    def on_key_press(self, key, modifiers):
        if not self.show_problem:
            if key == arcade.key.UP:
                self.movement = (-1, 0)  
            elif key == arcade.key.DOWN:
                self.movement = (1, 0)  
            elif key == arcade.key.LEFT:
                self.movement = (0, -1)  
            elif key == arcade.key.RIGHT:
                self.movement = (0, 1)
            elif key == arcade.key.E:
                print(f"Player position: ({self.player.row}, {self.player.col})")
                door_position = self.is_near_door()
                if door_position:
                    print(f"Door detected at position: {door_position}. Showing problem...")
                    self.current_problem = self.generate_math_problem()
                    self.show_problem = True
                    self.door_position = door_position 
                    self.show_door_message = False
                else:
                    print("No door nearby.")
            
                
        else: 
            if key == arcade.key.ENTER:
                self.check_answer()
            elif key == arcade.key.BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif key == arcade.key.MINUS:
                if not self.input_text:
                    self.input_text += "-"
            elif key in range(arcade.key.KEY_0, arcade.key.KEY_9 + 1):
                self.input_text += chr(key)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.movement = (0, 0)

    def generate_math_problem(self):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operation = random.choice(["+", "-"])
        if operation == "-":
            num1, num2 = max(num1, num2), min(num1, num2)
        answer = eval(f"{num1} {operation} {num2}")
        print(f"Generated problem: {num1} {operation} {num2} = {answer}")
        return {"question": f"{num1} {operation} {num2} = ?", "answer": answer}

    def check_answer(self):
        try:
            if int(self.input_text) == self.current_problem["answer"]:
                print("Correct answer! The door is open.")
                door_row, door_col = self.door_position
                self.maze.layout[door_row][door_col] = 0
                self.show_problem = False
            else:
                self.feedback_message = "Incorrect answer. Try again!"
                self.feedback_timer = 2
        except ValueError:
            self.feedback_message = "Invalid input. Please enter a number."
            self.feedback_timer = 2

        self.input_text = ""
    
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
        # Reduce the cooldown timer
        if self.movement_cooldown > 0:
            self.movement_cooldown -= delta_time

        # Allow movement only if cooldown has elapsed
        if self.movement_cooldown <= 0 and self.movement != (0, 0):
            delta_row, delta_col = self.movement
            self.player.move(delta_row, delta_col, self.maze.layout)
            self.movement_cooldown = self.movement_speed  # Reset the cooldown timer

        # Reduce the feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.feedback_message = ""

        # Check for a nearby door
        self.door_position = self.is_near_door()
        self.show_door_message = bool(self.door_position)  # Show message if near a door

    def is_near_door(self):
        row, col = self.player.row, self.player.col
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        for dr, dc in directions:
            nearby_row, nearby_col = row + dr, col + dc
            if 0 <= nearby_row < len(self.maze.layout) and 0 <= nearby_col < len(self.maze.layout[0]):
                if self.maze.layout[nearby_row][nearby_col] == 2: 
                    return nearby_row, nearby_col
        return False
        
def main():
    game = Main()
    arcade.run()

if __name__ == "__main__":
    main()