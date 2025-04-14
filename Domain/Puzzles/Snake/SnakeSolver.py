﻿from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver


class SnakeSolver(GameSolver):
    def __init__(self, grid: Grid, row_numbers: list[int], column_numbers: list[int], solver_engine: SolverEngine):
        self._grid = grid
        self._row_numbers = row_numbers
        self._column_numbers = column_numbers
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()
        return Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_cells_sum_constraints()

    def _add_initial_constraints(self):
        for position in [position for position, value in self._grid if value == 1]:
            self._solver.add(self._grid_z3[position])

    def _add_cells_sum_constraints(self):
        for row_index, row_number in enumerate(range(self.rows_number)):
            self._solver.add(self._solver.sum([self._grid_z3[row_index, c] for c in range(self.columns_number)]) == self._row_numbers[row_index])
        for column_index, column_number in enumerate(range(self.columns_number)):
            self._solver.add(self._solver.sum([self._grid_z3[r, column_index] for r in range(self.rows_number)]) == self._column_numbers[column_index])
