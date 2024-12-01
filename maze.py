import arcade

CELL_SIZE = 40  # Default cell size

class Maze:
    def __init__(self, screen_width, screen_height):
        self.layout = self._initialize_layout()
        self.num_rows = len(self.layout)
        self.num_cols = len(self.layout[0])

        # Calculate dynamic cell size to fit the screen
        self.cell_size = min(screen_width // self.num_cols, screen_height // self.num_rows)
        self.offset_x = (screen_width - self.num_cols * self.cell_size) // 2
        self.offset_y = (screen_height - self.num_rows * self.cell_size) // 2

    @staticmethod
    def _initialize_layout():
        """
        Returns the predefined maze layout. This separation allows for easier modification and testing.
        """
        return [
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 2, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 2, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def draw(self):
        """
        Renders the maze by drawing walls, paths, and doors based on the layout.
        """
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x, y = self._calculate_cell_center(col_index, row_index)
                self._draw_cell(cell, x, y)

    def _calculate_cell_center(self, col_index, row_index):
        """
        Calculates the center position of a cell for drawing.
        """
        x = self.offset_x + col_index * self.cell_size + self.cell_size / 2
        y = self.offset_y + (self.num_rows - row_index - 1) * self.cell_size + self.cell_size / 2
        return x, y

    def _draw_cell(self, cell, x, y):
        """
        Draws a single cell based on its type (wall, door, path).
        """
        if cell == 1:  # Wall
            color = arcade.color.BLACK
        elif cell == 2:  # Door
            color = arcade.color.GOLD
        elif cell == 0:  # Path
            color = arcade.color.LIGHT_GRAY
        else:
            return  # Undefined cell type, skip drawing
        
        arcade.draw_rectangle_filled(x, y, self.cell_size, self.cell_size, color)
