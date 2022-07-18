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

image = np.empty((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)
image.fill(250)
im = plt.imshow(image, extent=[0, CANVAS_SIZE, 0, CANVAS_SIZE])


def add_image(tile, index):
    image[index[0] * TILE_SIZE:(index[0] + 1) * TILE_SIZE, index[1] * TILE_SIZE:(index[1] + 1) * TILE_SIZE] = tile.get_image()



def animate(time):
    grid.set_random_possible_tile_at_current_index()
    add_image(grid.get_current_cell().tile, grid.current_index)
    im.set_array(image)
    grid.set_connection_points_adjacent_cells()
    grid.refresh_possible_tiles_adjacent_cells()
    lowest_cell_index = grid.get_index_lowest_cell()
    if lowest_cell_index is None:
        ani.event_source.stop()
        image_array = Image.fromarray(image)
        image_array.save('image.png')
    grid.set_current_index(lowest_cell_index)
    return im,


ani = FuncAnimation(fig, animate, interval=10)
plt.show()
