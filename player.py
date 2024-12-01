import arcade

# -------------------------------
# Player Class
# -------------------------------

class Player:
    """
    Represents a player in the maze.
    Responsible for rendering the player and managing movement within the maze.
    """

    # ---------------------------
    # Initialization
    # ---------------------------
    def __init__(self, start_row, start_col, cell_size, offset_x, offset_y, maze_rows):
        """
        Initialize the player with its starting position, cell size, and maze configuration.

        Args:
            start_row (int): Starting row position of the player.
            start_col (int): Starting column position of the player.
            cell_size (int): The size of each maze cell in pixels.
            offset_x (int): Horizontal offset for the maze rendering.
            offset_y (int): Vertical offset for the maze rendering.
            maze_rows (int): Total number of rows in the maze layout.
        """
        self.row = start_row  # Player's current row position
        self.col = start_col  # Player's current column position
        self.cell_size = cell_size  # Size of a maze cell
        self.offset_x = offset_x  # Offset for horizontal alignment
        self.offset_y = offset_y  # Offset for vertical alignment
        self.maze_rows = maze_rows  # Number of rows in the maze

    # ---------------------------
    # Rendering
    # ---------------------------
    def draw(self):
        """
        Draw the player as a red circle at its current position within the maze.
        """
        # Calculate player's position in screen coordinates
        x = self.offset_x + self.col * self.cell_size + self.cell_size / 2
        y = self.offset_y + (self.maze_rows - self.row - 1) * self.cell_size + self.cell_size / 2
        arcade.draw_circle_filled(x, y, self.cell_size / 3, arcade.color.RED)

    # ---------------------------
    # Movement
    # ---------------------------
    def move(self, delta_row, delta_col, maze_layout):
        """
        Move the player within the maze if the destination is valid.

        Args:
            delta_row (int): The change in row position (-1, 0, or 1).
            delta_col (int): The change in column position (-1, 0, or 1).
            maze_layout (list of list of int): The maze's grid layout.
        """
        # Calculate the potential new position
        new_row = self.row + delta_row
        new_col = self.col + delta_col

        # Check if the new position is within bounds and not a wall
        if 0 <= new_row < len(maze_layout) and 0 <= new_col < len(maze_layout[0]):
            if maze_layout[new_row][new_col] == 0:  # Only move if the new cell is a path
                self.row = new_row
                self.col = new_col
