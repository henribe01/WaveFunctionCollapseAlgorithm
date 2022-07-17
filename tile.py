import matplotlib.pyplot as plt
import numpy as np

from config import *


def rotate_list(l, n):
    return l[n:] + l[:n]


class Tile:
    all_tiles = []
    tile_types = ['Blank', 'I', 'L', 'T']

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

    def get_image(self):
        img = plt.imread(IMAGE_PATH + self.tile_type + '.png')
        return np.rot90(img, self.rotation)

    @staticmethod
    def setup_tiles():
        for tile_type in Tile.tile_types:
            if tile_type == 'Blank':
                tile = Tile(tile_type)
                Tile.all_tiles.append(tile)
            elif tile_type == 'I':
                for i in range(2):
                    tile = Tile(tile_type, i)
                    Tile.all_tiles.append(tile)
            else:
                for i in range(4):
                    tile = Tile(tile_type, i)
                    Tile.all_tiles.append(tile)