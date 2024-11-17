import arcade


class Player:
    def __init__(self, start_row, start_col, cell_size, offset_x, offset_y, maze_rows):
        self.row = start_row
        self.col = start_col
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.maze_rows = maze_rows

    def draw(self):
        x = self.offset_x + self.col * self.cell_size + self.cell_size / 2
        y = self.offset_y + (self.maze_rows - self.row - 1) * self.cell_size + self.cell_size / 2
        arcade.draw_circle_filled(x, y, self.cell_size / 3, arcade.color.RED)


    def move(self, delta_row, delta_col, maze_layout):
        new_row = self.row + delta_row
        new_col = self.col + delta_col

        if 0 <= new_row < len(maze_layout) and 0 <= new_col < len(maze_layout[0]):
            if maze_layout[new_row][new_col] == 0:
                self.row = new_row
                self.col = new_col