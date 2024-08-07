
# World Config
MAP_DIMENSION = 25

WINDOW_SIZE = (1200, 800)
GAMEBOARD_SIZE = (800,800)  # Total area of the grid in pixels
GRID_SIZE = (MAP_DIMENSION, MAP_DIMENSION)  # Number of squares in each row and column
SQUARE_SIZE = GAMEBOARD_SIZE[0] // GRID_SIZE[0]  # Size of each square in pixels

COLORS = {
    "DARK_GRAY": (64, 64, 64),
    "LIGHT_GRAY": (192, 192, 192),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 165, 0),
    "PURPLE": (128, 0, 128),
}

BACKGROUND_COLOR = COLORS["LIGHT_GRAY"]
GRID_LINE_COLOR = COLORS["DARK_GRAY"]

BALLS = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE"]#,"DARK_GRAY", "BLACK", "WHITE"]
VECTORS = ["UP", "DOWN", "LEFT", "RIGHT", "UP_LEFT", "UP_RIGHT", "DOWN_LEFT", "DOWN_RIGHT"]

