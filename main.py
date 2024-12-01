import arcade
from maze import Maze
from player import Player
import random

# Screen dimensions and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Math Maze Game"

class Main(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GRAY)
        
        # Initialize maze and player objects
        self.maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = Player(
            start_row=1,
            start_col=1,
            cell_size=self.maze.cell_size,
            offset_x=self.maze.offset_x,
            offset_y=self.maze.offset_y,
            maze_rows=len(self.maze.layout)
        )
        
        # Movement variables
        self.movement = (0, 0)  # Tracks player's movement direction
        self.movement_cooldown = 0  # Prevents rapid movement
        self.movement_speed = 0.2  # Time delay between movements
        
        # Math problem variables
        self.current_problem = None  # Holds the current math problem
        self.show_problem = False  # Indicates if a problem should be displayed
        self.input_text = ""  # Tracks user input for answers
        
        # Feedback and UI
        self.show_door_message = False  # Display message near doors
        self.feedback_message = ""  # Feedback on math problem answers
        self.feedback_timer = 0  # Timer for feedback display
        self.show_win_message = False  # Indicates if the win message should be displayed

    def on_draw(self):
        """Render the game screen."""
        arcade.start_render()
        self.maze.draw()  # Draw the maze
        self.player.draw()  # Draw the player

        # Show door encounter message
        if self.show_door_message:
            arcade.draw_text(
                "You encountered a door! Press 'E' to try opening it.",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 50,
                arcade.color.DARK_GREEN,
                font_size=18,
                anchor_x="center"
            )

        # Display the win message
        if self.show_win_message:
            arcade.draw_text(
                "You found the exit!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.GOLD,
                font_size=36,
                anchor_x="center"
            )

        # Display the math problem
        if self.show_problem:
            rect_width = 400
            rect_height = 200
            rect_x = SCREEN_WIDTH / 2
            rect_y = SCREEN_HEIGHT / 2
            arcade.draw_rectangle_filled(rect_x, rect_y, rect_width, rect_height, arcade.color.WHITE_SMOKE)
            arcade.draw_rectangle_outline(rect_x, rect_y, rect_width, rect_height, arcade.color.BLACK, 3)
            arcade.draw_text(self.current_problem["question"], rect_x, rect_y + 30, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")
            arcade.draw_text(f"Enter your answer: {self.input_text}", rect_x, rect_y - 30, arcade.color.DIM_GRAY, font_size=16, anchor_x="center", anchor_y="center")

        # Show feedback message
        if self.feedback_timer > 0:
            arcade.draw_text(self.feedback_message, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, arcade.color.RED, font_size=18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if not self.show_problem:
            # Movement keys
            if key == arcade.key.UP:
                self.movement = (-1, 0)
            elif key == arcade.key.DOWN:
                self.movement = (1, 0)
            elif key == arcade.key.LEFT:
                self.movement = (0, -1)
            elif key == arcade.key.RIGHT:
                self.movement = (0, 1)
            elif key == arcade.key.E:
                # Check if the player is near a door
                door_position = self.is_near_door()
                if door_position:
                    self.current_problem = self.generate_math_problem()
                    self.show_problem = True
                    self.door_position = door_position  # Save door position for later
                    self.show_door_message = False
        else:
            # Handle input for solving math problems
            if key == arcade.key.ENTER:
                self.check_answer()
            elif key == arcade.key.BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif key == arcade.key.MINUS and not self.input_text:
                self.input_text += "-"
            elif key in range(arcade.key.KEY_0, arcade.key.KEY_9 + 1):
                self.input_text += chr(key)

    def on_key_release(self, key, modifiers):
        """Stop movement when keys are released."""
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.movement = (0, 0)

    def generate_math_problem(self):
        """Generate a random math problem."""
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operation = random.choice(["+", "-"])
        if operation == "-":
            num1, num2 = max(num1, num2), min(num1, num2)
        answer = eval(f"{num1} {operation} {num2}")
        return {"question": f"{num1} {operation} {num2} = ?", "answer": answer}

    def check_answer(self):
        """Check if the player's answer is correct."""
        try:
            if int(self.input_text) == self.current_problem["answer"]:
                door_row, door_col = self.door_position
                self.maze.layout[door_row][door_col] = 0  # Open the door
                self.show_problem = False
            else:
                self.feedback_message = "Incorrect answer. Try again!"
                self.feedback_timer = 2
        except ValueError:
            self.feedback_message = "Invalid input. Please enter a number."
            self.feedback_timer = 2
        self.input_text = ""

    def on_update(self, delta_time):
        """Game update logic."""
        if self.movement_cooldown > 0:
            self.movement_cooldown -= delta_time

        if self.movement_cooldown <= 0 and self.movement != (0, 0):
            delta_row, delta_col = self.movement
            self.player.move(delta_row, delta_col, self.maze.layout)
            self.movement_cooldown = self.movement_speed

        if self.feedback_timer > 0:
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.feedback_message = ""

        self.door_position = self.is_near_door()
        self.show_door_message = bool(self.door_position)

        if self.is_near_goal():
            self.show_win_message = True

    def is_near_door(self):
        """Check if the player is near a door."""
        row, col = self.player.row, self.player.col
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nearby_row, nearby_col = row + dr, col + dc
            if 0 <= nearby_row < len(self.maze.layout) and 0 <= nearby_col < len(self.maze.layout[0]):
                if self.maze.layout[nearby_row][nearby_col] == 2:
                    return nearby_row, nearby_col
        return False

    def is_near_goal(self):
        """Check if the player is near the goal."""
        row, col = self.player.row, self.player.col
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nearby_row, nearby_col = row + dr, col + dc
            if 0 <= nearby_row < len(self.maze.layout) and 0 <= nearby_col < len(self.maze.layout[0]):
                if self.maze.layout[nearby_row][nearby_col] == 3:
                    return True
        return False

def main():
    game = Main()
    arcade.run()

if __name__ == "__main__":
    main()
