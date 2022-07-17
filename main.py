from random import choice

import matplotlib
from matplotlib.animation import FuncAnimation

from grid import Grid
from tile import Tile

matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from config import *

tile_types = ['Blank', 'I', 'L', 'T']
tiles = []
for tile_type in tile_types:
    if tile_type == 'Blank':
        tile = Tile(tile_type)
        tiles.append(tile)
    elif tile_type == 'I':
        for i in range(2):
            tile = Tile(tile_type, i)
            tiles.append(tile)
    else:
        for i in range(4):
            tile = Tile(tile_type, i)
            tiles.append(tile)

fig, ax = plt.subplots()
ax.set_xlim(0, CANVAS_SIZE)
ax.set_ylim(0, CANVAS_SIZE)
ax.set_aspect('equal')

grid = Grid(CANVAS_SIZE // TILE_SIZE)


def animate(time):
    grid.set_random_possible_tile_at_current_index()
    ax.imshow(grid.get_current_cell().tile.get_image(),
              extent=[grid.current_index[1] * TILE_SIZE,
                      (grid.current_index[1] + 1) * TILE_SIZE,
                      CANVAS_SIZE - (grid.current_index[0] + 1) * TILE_SIZE,
                        CANVAS_SIZE - grid.current_index[0] * TILE_SIZE])
    grid.set_connection_points_adjacent_cells()
    grid.refresh_possible_tiles_adjacent_cells()
    lowest_cell_index = grid.get_index_lowest_cell()
    if lowest_cell_index is None:
        ani.event_source.stop()
    grid.set_current_index(lowest_cell_index)

ani = FuncAnimation(fig, animate, interval=10)
plt.show()
