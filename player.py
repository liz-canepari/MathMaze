import arcade

CELL_SIZE = 40

class Player:
    def __init__(self, start_row, start_col):
        self.row = start_row
        self.col = start_col

    def draw(self):
        x = self.col * CELL_SIZE + CELL_SIZE / 2
        y = 600 - (self.row * CELL_SIZE + CELL_SIZE / 2)
        arcade.draw_circle_filled(x, y, CELL_SIZE / 3, arcade.color.RED)

    def move(self, delta_row, delta_col, maze_layout):
        new_row = self.row + delta_row
        new_col = self.col + delta_col

        if 0 <= new_row < len(maze_layout) and 0 <= new_col < len(maze_layout[0]):
            if maze_layout[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col
            elif maze_layout[new_row][new_col] == 2:
                print("You encountered a door! Press 'E' to try opening it.")