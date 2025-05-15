﻿from z3 import Solver, Bool, Not, unsat, And, is_true

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class BinairoSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 6:
            raise ValueError("Binairo grid must be at least 6x6")
        if self.rows_number % 2 != 0 or self.columns_number % 2 != 0:
            raise ValueError("Binairo grid must have an even number of rows/columns")
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"matrix_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()

        model = self._solver.model()
        return Grid([[is_true(model.eval(self._grid_z3[r][c])) for c in range(self.columns_number)] for r in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_half_true_false_by_line_constraints()
        self._add_unique_line_constraints()
        self._add_not_same_3_adjacent_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 0:
                    self._solver.add(Not(self._grid_z3[r][c]))
                elif self._grid.value(r, c) == 1:
                    self._solver.add(self._grid_z3[r][c])

    def _add_half_true_false_by_line_constraints(self):
        half_columns = self.columns_number / 2
        half_rows = self.rows_number / 2
        for row_z3 in self._grid_z3.matrix:
            self._solver.add(sum(row_z3[c] for c in range(self.columns_number)) == half_columns)
        for column_z3 in zip(*self._grid_z3.matrix):
            self._solver.add(sum(column_z3[r] for r in range(self.rows_number)) == half_rows)

    def _add_unique_line_constraints(self):
        for r0 in range(1, self.rows_number):
            for r1 in range(r0):
                self._solver.add(Not(And([self._grid_z3[r0][c] == self._grid_z3[r1][c] for c in range(self.columns_number)])))
        for c0 in range(1, self.columns_number):
            for c1 in range(c0):
                self._solver.add(Not(And([self._grid_z3[r][c0] == self._grid_z3[r][c1] for r in range(self.rows_number)])))

    def _add_not_same_3_adjacent_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 2):
                self._solver.add(Not(And(self._grid_z3[r][c] == self._grid_z3[r][c + 1], self._grid_z3[r][c + 1] == self._grid_z3[r][c + 2])))
        for c in range(self.columns_number):
            for r in range(self.rows_number - 2):
                self._solver.add(Not(And(self._grid_z3[r][c] == self._grid_z3[r + 1][c], self._grid_z3[r + 1][c] == self._grid_z3[r + 2][c])))
