import matplotlib.pyplot as plt
import numpy as np

from config import *


def rotate_list(l, n):
    return l[n:] + l[:n]


class Tile:
    all_tiles = []

    def __init__(self, tile_type, rotation=0):
        self.tile_type = tile_type
        self.rotation = rotation
        # 0 = black, 1 = white
        # start at top, then go clockwise
        self.connection_points = []
        if tile_type == 'Blank':
            self.connection_points = [0, 0, 0, 0]
        elif tile_type == 'I':
            self.connection_points = [1, 0, 1, 0]
        elif tile_type == 'L':
            self.connection_points = [1, 1, 0, 0]
        elif tile_type == 'T':
            self.connection_points = [0, 1, 1, 1]
        self.connection_points = rotate_list(self.connection_points, rotation)
        Tile.all_tiles.append(self)

    def get_image(self):
        img = plt.imread(IMAGE_PATH + self.tile_type + '.png')
        return np.rot90(img, self.rotation)
