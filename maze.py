import arcade

CELL_SIZE = 40

class Maze:
    def __init__(self, screen_width, screen_height):
        self.layout = [
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 1
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 2
            [1, 2, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 3
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1], # 4
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1], # 5
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1], # 6
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 7
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1], # 8
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1], # 9
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], # 10
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], # 11
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1], # 12
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 13
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], # 14
            [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1], # 15
            [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], # 16
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1], # 17
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3], # 18
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 19
        ]

        self.num_rows = len(self.layout)
        self.num_cols = len(self.layout[0])
        # Calculate cell size to fit the screen
        self.cell_size = min(screen_width // self.num_cols, screen_height // self.num_rows)
        self.offset_x = (screen_width - self.num_cols * self.cell_size) // 2
        self.offset_y = (screen_height - self.num_rows * self.cell_size) // 2

    def draw(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                # Calculate the position dynamically
                x = self.offset_x + col_index * self.cell_size + self.cell_size / 2
                y = self.offset_y + (self.num_rows - row_index - 1) * self.cell_size + self.cell_size / 2
                
                if cell == 1:  # Wall
                    arcade.draw_rectangle_filled(x, y, self.cell_size, self.cell_size, arcade.color.BLACK)
                elif cell == 2:  # Door
                    arcade.draw_rectangle_filled(x, y, self.cell_size, self.cell_size, arcade.color.GOLD)
                elif cell == 0:  # Path
                    arcade.draw_rectangle_filled(x, y, self.cell_size, self.cell_size, arcade.color.LIGHT_GRAY)