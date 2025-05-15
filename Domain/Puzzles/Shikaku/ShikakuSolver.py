﻿
from z3 import Solver, And, unsat, Or, Int

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class ShikakuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 5 or self.columns_number < 5:
            raise ValueError("The grid must be at least 5x5")
        numbers_sum = sum([cell for row in self._grid.matrix for cell in row if cell != -1])
        if numbers_sum != self.rows_number * self.columns_number:
            raise ValueError("Sum of numbers must be equal to the number of cells")
        self._solver = Solver()
        self._matrix_z3 = None
        self._position_number_by_rectangle_index = self._get_position_number_by_rectangle_index()

    def _get_position_number_by_rectangle_index(self) -> dict[int, tuple[tuple[int, int], int]]:
        rectangles = {}
        for i, (position, number) in enumerate([((r, c), self._grid.matrix[r][c]) for r in range(self.rows_number) for c in range(self.columns_number) if self._grid.value(r, c) != -1]):
            rectangles[i] = position, number
        return rectangles

    def get_solution(self) -> Grid:
        self._matrix_z3 = [[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._matrix_z3[i][j]).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _add_constraints(self):
        self._add_rectangles_constraints()

    def _add_rectangles_constraints(self):
        for rectangle_index, (position, cells_number) in self._position_number_by_rectangle_index.items():
            current_rectangle_constraints = []
            r, c = position
            cells_of_biggest_rectangle = self._get_cells_of_biggest_rectangle((r, c))
            max_width, max_height, min_position, max_position = self.get_width_height_positions(cells_of_biggest_rectangle)
            all_rectangles_size = self._get_all_rectangles_size(cells_number)
            possibles_rectangles_size = [rectangles_size for rectangles_size in all_rectangles_size if rectangles_size[0] <= max_height and rectangles_size[1] <= max_width]
            for height, width in possibles_rectangles_size:
                for r in range(min_position[0], max_position[0] + 1 - (height - 1)):
                    for c in range(min_position[1], max_position[1] + 1 - (width - 1)):
                        rectangle_cells = {(r + dr, c + dc) for dr in range(height) for dc in range(width)}
                        rectangle_cells = {cell for cell in rectangle_cells if cell in cells_of_biggest_rectangle}
                        if position not in rectangle_cells or len(rectangle_cells) != width * height:
                            continue
                        constraint = And([self._matrix_z3[r][c] == rectangle_index for r, c in rectangle_cells])
                        current_rectangle_constraints.append(constraint)
            self._solver.add(Or(current_rectangle_constraints))

    @staticmethod
    def _get_all_rectangles_size(cells_number) -> set[tuple[int, int]]:
        divisors = []
        for i in range(1, int(cells_number**0.5) + 1):
            if cells_number % i == 0:
                divisors.append(i)
                if i != cells_number // i:
                    divisors.append(cells_number // i)

        return {(divisor, cells_number // divisor) for divisor in divisors}

    @staticmethod
    def get_width_height_positions(possible_cells) -> (int, int, (int, int), (int, int)):
        min_r_position = min(possible_cells, key=lambda x: x[0])
        max_r_position = max(possible_cells, key=lambda x: x[0])
        min_c_position = min(possible_cells, key=lambda x: x[1])
        max_c_position = max(possible_cells, key=lambda x: x[1])
        width = max_c_position[1] - min_c_position[1] + 1
        height = max_r_position[0] - min_r_position[0] + 1
        return width, height, (min_r_position[0], min_c_position[1]), (max_r_position[0], max_c_position[1])

    @staticmethod
    def _invert_width_height(width: int, height: int) -> (int, int):
        return height, width

    def _get_cells_of_biggest_rectangle(self, position: (int, int)) -> set[tuple[int, int]]:
        moves_rows = [(1, 0), (-1, 0)]
        moves_columns = [(0, 1), (0, -1)]
        moves = moves_rows + moves_columns
        cells = set()
        cells.add(position)
        for dr, dc in moves:
            r, c = position
            while 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number:
                r += dr
                c += dc
                if self._grid.value(r, c) != -1:
                    break
                cells.add((r, c))
        max_r_position = max(cells, key=lambda x: x[0])
        min_r_position = min(cells, key=lambda x: x[0])
        max_c_position = max(cells, key=lambda x: x[1])
        min_c_position = min(cells, key=lambda x: x[1])

        for r in range(min_r_position[0], max_r_position[0] + 1):
            for c in range(min_c_position[1], max_c_position[1] + 1):
                if self._grid.value(r, c) == -1:
                    cells.add((r, c))

        return cells
