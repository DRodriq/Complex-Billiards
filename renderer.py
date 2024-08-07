import pygame
from pygame.locals import *
import config
import math


class Renderer():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(config.WINDOW_SIZE)
        pygame.display.set_caption("Simulation")
        self.screen.fill(config.BACKGROUND_COLOR)

        self.game_surface = pygame.Surface(config.GAMEBOARD_SIZE)

    
    def set_drawing_map(self, drawing_map):
        self.drawing_map = drawing_map


    def refresh_gameboard(self):
        self.game_surface.fill(config.BACKGROUND_COLOR)
        grid_size = config.GRID_SIZE
        square_size = config.SQUARE_SIZE
        grid_line_color = config.GRID_LINE_COLOR
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(self.game_surface, grid_line_color, rect, 1)  # Draw the square outline

        self.screen.blit(self.game_surface, dest=(0, 0), area=self.game_surface.get_rect())

    def draw_overlay(self, overlay):
        square_size = config.SQUARE_SIZE
        colors = config.COLORS
        draw_map = self.drawing_map

        # Precompute positions and sizes
        circle_data = []
        square_data = []
        triangle_data = []  # New list to store star data
        for i in range(len(overlay)):
            for j in range(len(overlay[i])):
                val = overlay[i][j]
                shape = None
                # Determine the color and shape based on the value
                for draw in draw_map:
                    if draw.value == val:
                        color = draw.color
                        shape = draw.shape

                if shape == 'circle':
                    # Calculate the position and radius of the circle
                    circle_x = j * square_size + square_size // 2
                    circle_y = i * square_size + square_size // 2
                    circle_radius = square_size // 2
                    # Store the circle data
                    circle_data.append((color, (circle_x, circle_y), circle_radius))
                elif shape == 'square':
                    # Calculate the position and size of the square
                    rect_x = j * square_size
                    rect_y = i * square_size
                    rect_width = square_size
                    rect_height = square_size
                    # Store the rectangle data
                    square_data.append((color, (rect_x, rect_y, rect_width, rect_height)))
                elif shape == 'triangle':  # New condition for stars
                # Calculate the position and size of the triangle
                    triangle_x = j * square_size + square_size // 2
                    triangle_y = i * square_size + square_size // 2
                    triangle_size = square_size
                    # Store the triangle data
                    triangle_points = calculate_triangle_points((triangle_x, triangle_y), triangle_size)
                    triangle_data.append((color, triangle_points))

        # Draw all squares
        for color, rect in square_data:
            pygame.draw.rect(self.game_surface, color, rect)
        # Draw all triangles
        for color, points in triangle_data:
            pygame.draw.polygon(self.game_surface, color, points)   
        # Draw all circles
        for color, position, radius in circle_data:
            pygame.draw.circle(self.game_surface, color, position, radius)

        # Blit the game surface onto the screen
        self.screen.blit(self.game_surface, dest=(0, 0), area=self.game_surface.get_rect())


def calculate_triangle_points(center, size):
    points = []
    height = size * math.sqrt(3) / 2  # Height of an equilateral triangle

    # Calculate the three vertices of the triangle
    points.append((center[0], center[1] - height / 2))  # Top vertex
    points.append((center[0] - size / 2, center[1] + height / 2))  # Bottom-left vertex
    points.append((center[0] + size / 2, center[1] + height / 2))  # Bottom-right vertex

    return points


if __name__ == "__main__":
    import time
    import numpy as np
    from collections import namedtuple

    renderer = Renderer()

    Drawing_Map = namedtuple('Drawings', ['color', 'shape', 'size', 'value'])
    drawing_map = []
    drawing_map.append(Drawing_Map(color=config.COLORS["FOREST"], shape="square", size=4, value=2))
    drawing_map.append(Drawing_Map(color=config.COLORS["RED"], shape="triangle", size=6, value=5))
    drawing_map.append(Drawing_Map(color=config.COLORS["BLUE"], shape="circle", size=5, value=1))
    drawing_map.append(Drawing_Map(color=config.COLORS["YELLOW"], shape="circle", size=4, value=4))

    renderer.set_drawing_map(drawing_map)

    renderer.refresh_gameboard()
    pygame.display.flip()
    
    delay = 0.2
    iterations = 1000
    bench_now = time.time()
    for _ in range(iterations):
        overlay = np.random.randint(0, 11, size=(config.MAP_DIMENSION, config.MAP_DIMENSION))
        #overlay = np.random.randint(0, 11, size=(config.MAP_DIMENSION, config.MAP_DIMENSION, 3)).tolist()
        renderer.refresh_gameboard()
        renderer.draw_overlay(overlay)
        pygame.display.flip()
        time.sleep(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    bench_end = time.time()
    print(f"Time taken for 100 iterations of overlay 1: {bench_end - bench_now - (delay*iterations)} seconds")

    """
    now = time.time()
    for _ in range(1000):
        overlay = np.random.randint(0, 11, size=(config.MAP_DIMENSION, config.MAP_DIMENSION))
        renderer.refresh_gameboard()
        renderer.draw_overlay(overlay)
        pygame.display.flip()
    end = time.time()
    print(f"Time taken for 100 iterations of overlay 1: {end - now} seconds")

    now = time.time()
    for _ in range(1000):
        overlay = np.random.randint(0, 11, size=(config.MAP_DIMENSION, config.MAP_DIMENSION))
        renderer.refresh_gameboard()
        renderer.draw_overlay(overlay)
        pygame.display.flip()
    end = time.time()
    print(f"Time taken for 100 iterations of overlay 2: {end - now} seconds")
    """