﻿from collections import defaultdict
from itertools import combinations
from typing import Tuple, Set, FrozenSet, Dict

from bitarray import bitarray

from Utils.colors import console_back_ground_colors, console_police_colors


class Grid:
    def __init__(self, matrix: list[list]):
        self._matrix = matrix
        self.rows_number = len(matrix)
        self.columns_number = len(matrix[0])

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return self.matrix == other.matrix

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self._matrix)

    @property
    def matrix(self):
        return self._matrix

    @staticmethod
    def empty() -> 'Grid':
        return Grid([[]])

    def value(self, r, c):
        return self._matrix[r][c]

    def set_value(self, r, c, value):
        self._matrix[r][c] = value

    def to_console_string(self, police_color_grid=None, back_ground_color_grid=None, interline=False):
        color_matrix = [[console_police_colors[police_color_grid.value(r, c) % (len(console_police_colors) - 1)] if police_color_grid else '' for c in range(self.columns_number)] for r in range(self.rows_number)]
        background_color_matrix = [[console_back_ground_colors[back_ground_color_grid.value(r, c) % (len(console_police_colors) - 1)] if back_ground_color_grid else '' for c in range(self.columns_number)] for r in range(self.rows_number)]
        end_color = console_back_ground_colors['end'] if police_color_grid or back_ground_color_grid else ''
        end_space = ' ' if back_ground_color_grid else ''
        result = []
        cell_len = max(len(f'{cell}') for row in self._matrix for cell in row)
        for r in range(self.rows_number):
            result.append(self._row_to_string(r, cell_len, background_color_matrix, color_matrix, end_color, end_space))
            if interline and r < self.rows_number - 1:
                result.append(''.join(f'{background_color_matrix[r][c]}{end_color}' for c in range(self.columns_number)))
        return '\n'.join(result)

    def _row_to_string(self, r, max_len, background_color_matrix, color_matrix, end_color, end_space):
        return ''.join(f'{background_color_matrix[r][c]}{color_matrix[r][c]}{end_space}{self._matrix[r][c]}{end_space}{end_color}'.rjust(max_len) for c in range(self.columns_number))

    def get_regions(self) -> Dict[int, FrozenSet[Tuple[int, int]]]:
        regions = defaultdict(set)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._matrix[r][c] not in regions:
                    regions[self._matrix[r][c]] = set()
                regions[self._matrix[r][c]].add((r, c))
        return {key: frozenset(value) for key, value in regions.items()} if regions else {}

    def are_all_cells_connected(self, value=True, mode='orthogonal') -> bool:
        r, c = self._get_cell(value)
        if r is None:
            return False
        visited = self._depth_first_search(r, c, value, mode)
        return len(visited) == sum(cell == value for row in self._matrix for cell in row)

    def get_all_shapes(self, value, mode='orthogonal') -> Set[FrozenSet[Tuple[int, int]]]:
        excluded = []
        shapes = set()
        while True:
            r, c = self._get_cell(value, excluded)
            if r is None:
                return shapes
            if any((r, c) in shape for shape in shapes):
                excluded.append((r, c))
                continue
            visited = self._depth_first_search(r, c, value, mode)
            shapes.add(frozenset(visited))
            excluded.append((r, c))

    def are_min_2_connected_cells_touch_border(self, r, c, mode='orthogonal') -> Tuple[bool, Set[Tuple[int, int]]]:
        value = self._matrix[r][c]
        visited = self._depth_first_search(r, c, value, mode)
        if len(visited) <= 1:
            return False, set()
        border_cells = set()
        for cell in visited:
            if cell[0] == 0 or cell[0] == self.rows_number - 1 or cell[1] == 0 or cell[1] == self.columns_number - 1:
                border_cells.add(cell)
        return len(border_cells) >= 2, visited

    def find_all_min_2_connected_cells_touch_border(self, value, mode='orthogonal') -> Set[FrozenSet[Tuple[int, int]]]:
        excluded = []
        cells_sets: Set[FrozenSet[Tuple[int, int]]] = set()
        while True:
            r, c = self._get_cell(value, excluded)
            if r is None:
                return cells_sets
            if any((r, c) in cells_set for cells_set in cells_sets):
                excluded.append((r, c))
                continue
            are_touch_border, cells = self.are_min_2_connected_cells_touch_border(r, c, mode)
            if are_touch_border:
                cells_sets.add(frozenset(cells))
            excluded.append((r, c))

    def _depth_first_search(self, r, c, value, mode='orthogonal', visited=None) -> set:
        if visited is None:
            visited = set()
        if (self._matrix[r][c] != value) or ((r, c) in visited):
            return visited
        visited.add((r, c))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] if mode != 'diagonal' else [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number and (r + dr, c + dc) not in visited:
                if self._matrix[r + dr][c + dc] == value:
                    new_visited = self._depth_first_search(r + dr, c + dc, value, mode, visited)
                    if new_visited != visited:
                        return new_visited

        return visited

    def _get_cell(self, value, excluded=None):
        if excluded is None:
            excluded = []
        return next(((i, j) for i in range(self.rows_number) for j in range(self.columns_number) if self._matrix[i][j] == value and (i, j) not in excluded), (None, None))

    def get_console_grid(self, bool_grid):
        background_grid = Grid([[1 if bool_grid.value(r, c) else 0 for c in range(bool_grid.columns_number)] for r in range(bool_grid.rows_number)])
        numbers_grid = Grid([[Grid.list_to_string(self.value(r, c)) if isinstance(self.value(r, c), list) else ' ' for c in range(self.columns_number)] for r in range(self.rows_number)])
        police_color_grid = Grid([[16 for _ in range(bool_grid.columns_number)] for _ in range(bool_grid.rows_number)])
        console_grid = numbers_grid.to_console_string(police_color_grid, background_grid)
        return console_grid

    @staticmethod
    def get_adjacent_combinations(neighbour_length, block_length, circular) -> list[list[bool]]:
        if block_length == 0:
            return [[False for _ in range(neighbour_length)]]
        if block_length == neighbour_length:
            return [[True for _ in range(neighbour_length)]]
        result = []
        for combo in combinations(range(neighbour_length), block_length):
            cell_adjacent = [True for i in range(1, block_length) if combo[i] - combo[i - 1] == 1]
            if circular and combo[0] + neighbour_length - combo[-1] == 1:
                cell_adjacent.append(True)
            if cell_adjacent.count(True) == block_length - 1:
                indexes = [index in combo for index in range(neighbour_length)]
                result.append(indexes)
        return result

    @staticmethod
    def get_bit_array_adjacent_combinations(neighbour_length, block_length, circular) -> list[bitarray]:
        bitarrays = []
        first_bitarray = bitarray(neighbour_length)
        for i in range(block_length):
            first_bitarray[i] = True
        bitarrays.append(first_bitarray)
        current_bitarray = first_bitarray
        for i in range(neighbour_length - block_length):
            current_bitarray = current_bitarray >> 1
            bitarrays.append(current_bitarray)
        if circular:
            for i in range(block_length - 1):
                current_bitarray = current_bitarray >> 1
                current_bitarray[0] = True
                bitarrays.append(current_bitarray)
        return bitarrays

    @staticmethod
    def list_to_string(array):
        return sum(array)

    def is_empty(self):
        return self == Grid.empty()
