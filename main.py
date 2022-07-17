import matplotlib
import numpy as np
from PIL import Image
from matplotlib.animation import FuncAnimation

from grid import Grid
from tile import Tile

matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from config import *

fig, ax = plt.subplots()
ax.set_xlim(0, CANVAS_SIZE)
ax.set_ylim(0, CANVAS_SIZE)
ax.set_aspect('equal')

Tile.setup_tiles()
grid = Grid(CANVAS_SIZE // TILE_SIZE)

def flatten_image_grid():
    image = np.empty((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)
    for grid_index_row in range(CANVAS_SIZE//TILE_SIZE):
        grid_image_row = np.empty((TILE_SIZE, CANVAS_SIZE, 3))
        for row_in_tile in range(TILE_SIZE):
            row = np.array([])
            for grid_index_col in range(CANVAS_SIZE//TILE_SIZE):
                if grid_index_col == 0:
                    row = image_grid[grid_index_row][grid_index_col][row_in_tile]
                else:
                    row = np.concatenate((row, image_grid[grid_index_row][grid_index_col][row_in_tile]))
            if row_in_tile == 0:
                grid_image_row[0] = row
            else:
                grid_image_row[row_in_tile] = row
        if grid_index_row == 0:
            image[0:TILE_SIZE] = grid_image_row
        else:
            image[grid_index_row*TILE_SIZE:(grid_index_row+1)*TILE_SIZE] = grid_image_row
    return image

image_grid = np.empty((CANVAS_SIZE // TILE_SIZE, CANVAS_SIZE // TILE_SIZE, TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)
image_grid.fill(250)
image = flatten_image_grid()
im = plt.imshow(image, extent=[0, CANVAS_SIZE, 0, CANVAS_SIZE])

def add_image(tile, index):
    image_grid[index[0]][index[1]] = tile.get_image()


def animate(time):
    grid.set_random_possible_tile_at_current_index()
    add_image(grid.get_current_cell().tile, grid.current_index)
    image = flatten_image_grid()
    im.set_array(image)
    grid.set_connection_points_adjacent_cells()
    grid.refresh_possible_tiles_adjacent_cells()
    lowest_cell_index = grid.get_index_lowest_cell()
    if lowest_cell_index is None:
        ani.event_source.stop()
        image_array = Image.fromarray(image_grid[0][0])
        image_array.save('image.png')
    grid.set_current_index(lowest_cell_index)
    return im,


ani = FuncAnimation(fig, animate, interval=10)
plt.show()
