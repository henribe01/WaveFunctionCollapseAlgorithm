from random import choice

import numpy as np

from tile import Tile

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


class Grid:
    def __init__(self, rows):
        self.grid = [[Cell() for i in range(rows)] for j in range(rows)]
        self.current_index = np.array([rows // 2, rows // 2])
        self.rows = rows

    def get_random_free_index(self):
        """Returns a random index with no tile"""
        free_index = []
        for i in range(self.rows):
            for j in range(self.rows):
                if self.grid[i][j].tile is None:
                    free_index.append([i, j])
        return choice(free_index)

    def get_index_lowest_cell(self):
        """Returns the index of the lowest cell"""
        all_non_zero_cells = [self.grid[i][j].entropy_value for i in range(self.rows) for j in range(self.rows) if self.grid[i][j].entropy_value != 0]
        if len(all_non_zero_cells) == 0:
            return None
        lowest_entropy = min(all_non_zero_cells)
        lowest_entropy_cells = [
            [i, j] for i in range(self.rows) for j in range(self.rows)
            if self.grid[i][j].entropy_value == lowest_entropy]
        return choice(lowest_entropy_cells)

    def get_index_lowest_adjacent_cell(self):
        """Get the lowest cell in adjacent cells, that is not 0, if multiple
        have the same value, a random one is picked """
        possible_direction = []
        for direction in DIRECTIONS:
            adjacent_cell = self.get_adjacent_cell(direction)
            if adjacent_cell is not None:
                if adjacent_cell.entropy_value != 0:
                    possible_direction.append(direction)
        if len(possible_direction) == 0:
            return self.get_random_free_index()
        lowest_entropy = min(
            [self.get_adjacent_cell(direction).entropy_value for direction in
             possible_direction])
        lowest_entropy_cells = [direction for direction in possible_direction
                                if self.get_adjacent_cell(
                direction).entropy_value == lowest_entropy]
        move_direction = choice(lowest_entropy_cells)
        return self.current_index + move_direction

    def get_adjacent_cell(self, direction):
        """Returns the cell in the given direction"""
        new_index = self.current_index + direction
        if new_index[0] < 0 or new_index[0] >= self.rows or new_index[1] < 0 or \
                new_index[1] >= self.rows:
            return None
        return self.grid[new_index[0]][new_index[1]]

    def set_tile_at_current_index(self, tile):
        """Sets the tile at the current index"""
        self.get_current_cell().set_tile(tile)

    def get_current_cell(self):
        """Returns the current cell"""
        return self.grid[self.current_index[0]][self.current_index[1]]

    def set_current_index(self, index):
        """Sets the current index"""
        self.current_index = index

    def get_cell(self, index):
        """Returns the cell at the given index"""
        return self.grid[index[0]][index[1]]

    def set_connection_points_adjacent_cells(self):
        """Sets the connection points of the adjacent cells"""
        for index, direction in enumerate(DIRECTIONS):
            current_cell_connection_points = self.get_current_cell().connection_points
            adjacent_cell = self.get_adjacent_cell(direction)
            direction = -1 * direction  # Flips the direction, so that the connection points are in the same direction as the adjacent cells
            if adjacent_cell is not None:
                adjacent_cell.set_connection_point(direction, current_cell_connection_points[index])

    def refresh_possible_tiles_adjacent_cells(self):
        """Refreshes the possible tiles of the adjacent cells"""
        for direction in DIRECTIONS:
            adjacent_cell = self.get_adjacent_cell(direction)
            if adjacent_cell is not None and adjacent_cell.entropy_value != 0:
                adjacent_cell.refresh_possible_tiles()

    def set_random_possible_tile_at_current_index(self):
        """Sets a random possible tile at the current index"""
        tile = choice(self.get_current_cell().possible_tiles)
        self.set_tile_at_current_index(tile)

class Cell:
    def __init__(self):
        # -1 = Not set; 0 = White; 1 = Black
        # Start at top, then go clockwise
        self.connection_points = [-1, -1, -1, -1]
        self.connection_points_outside = [-1, -1, -1, -1]
        self.tile = None
        self.possible_tiles = Tile.all_tiles
        self.entropy_value = len(self.possible_tiles)

    def set_tile(self, tile):
        self.entropy_value = 0
        self.connection_points = tile.connection_points
        self.tile = tile

    def set_connection_point(self, direction, value):
        direction_index = [i for i, x in enumerate(DIRECTIONS) if np.array_equal(x, direction)][0]
        if self.connection_points_outside[direction_index] == -1:
            self.connection_points_outside[direction_index] = value

    def refresh_possible_tiles(self):
        self.possible_tiles = []
        for tile in Tile.all_tiles:
            tile_fits = True
            for index in range(4):
                if tile.connection_points[index] != self.connection_points_outside[index] and \
                        self.connection_points_outside[index] != -1:
                    tile_fits = False
                    break
            if tile_fits:
                self.possible_tiles.append(tile)
        self.entropy_value = len(self.possible_tiles)

    def get_random_tile(self):
        return choice(self.possible_tiles)