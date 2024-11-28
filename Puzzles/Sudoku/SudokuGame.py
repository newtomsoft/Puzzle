﻿import math

from z3 import Int, Solver, And, sat, Distinct

from Utils.Grid import Grid
from Utils.utils import is_perfect_square


class SudokuGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("Sudoku grid must be square")
        if not is_perfect_square(self.rows_number) and self.rows_number != 6 and self.rows_number != 12:
            raise ValueError("Sudoku subgrid must have size n x n or 3x2 or 4x3")
        if not self._initial_numbers_are_different_in_row_and_column():
            raise ValueError("initial numbers must be different in rows and columns")

        if is_perfect_square(self.rows_number):
            self._sub_square_row_number = int(math.sqrt(self.rows_number))
            self._sub_square_column_number = int(self._sub_square_row_number)
        elif self.rows_number == 6:
            self._sub_square_row_number = 2
            self._sub_square_column_number = 3
        else:
            self._sub_square_row_number = 3
            self._sub_square_column_number = 4
        if not self._initial_numbers_are_different_in_sub_square():
            raise ValueError("initial numbers must be different in sub squares")

        if not self._initial_numbers_between_1_and_nxn():
            raise ValueError("initial numbers must be between 1 and n x n")
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return None
        model = self._solver.model()
        grid = Grid([[model.eval(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constraints(self):
        self._distinct_in_sub_squares_constraints()
        self._different_in_rows_and_columns_constraints()
        self._initials_constraints()

    def _distinct_in_sub_squares_constraints(self):
        constraints = []
        for sub_square_row in range(0, self.rows_number, self._sub_square_row_number):
            for sub_square_column in range(0, self.columns_number, self._sub_square_column_number):
                for r in range(self._sub_square_row_number):
                    for c in range(self._sub_square_column_number):
                        constraints.append(Distinct([self._grid_z3.value(sub_square_row + r, sub_square_column + c) for c in range(self._sub_square_column_number) for r in range(self._sub_square_row_number)]))
        self._solver.add(constraints)

    def _different_in_rows_and_columns_constraints(self):
        constraints = []
        for r in range(self.rows_number):
            constraints.append(Distinct([self._grid_z3.value(r, c) for c in range(self.columns_number)]))
        for c in range(self.columns_number):
            constraints.append(Distinct([self._grid_z3.value(r, c) for r in range(self.rows_number)]))
        self._solver.add(And(constraints))

    def _initials_constraints(self):
        constraints = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == -1:
                    constraints.append(And(1 <= self._grid_z3.value(r, c), self._grid_z3.value(r, c) <= self.rows_number))
                else:
                    constraints.append(self._grid_z3.value(r, c) == self._grid.value(r, c))
        self._solver.add(And(constraints))

    def _initial_numbers_are_different_in_row_and_column(self):
        seen_in_rows = [set() for _ in range(self.rows_number)]
        seen_in_columns = [set() for _ in range(self.columns_number)]
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                value = self._grid.value(r, c)
                if value == -1:
                    continue
                if value in seen_in_rows[r] or value in seen_in_columns[c]:
                    return False
                seen_in_rows[r].add(value)
                seen_in_columns[c].add(value)
        return True

    def _initial_numbers_are_different_in_sub_square(self):
        for sub_square_row in range(0, self.rows_number, self._sub_square_row_number):
            for sub_square_column in range(0, self.columns_number, self._sub_square_column_number):
                seen_in_sub_square = set()
                for r in range(self._sub_square_row_number):
                    for c in range(self._sub_square_column_number):
                        value = self._grid.value(sub_square_row + r, sub_square_column + c)
                        if value == -1:
                            continue
                        if value in seen_in_sub_square:
                            return False
                        seen_in_sub_square.add(value)
        return True

    def _initial_numbers_between_1_and_nxn(self):
        return all(
            self._grid.value(r, c) == -1 or 1 <= self._grid.value(r, c) <= self.rows_number
            for r in range(self.rows_number)
            for c in range(self.columns_number)
        )
