﻿from z3 import Solver, Not, And, unsat, Int, Distinct

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class FutoshikiSolver(GameSolver):
    def __init__(self, grid: Grid, higher_positions: list[tuple[Position, Position]]):
        self._grid = grid
        self._higher_positions = higher_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution_grid: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._number(Position(r, c))).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        exclusion_constraint = Not(
            And([self._number(Position(r, c)) == self._previous_solution_grid[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number) if self._previous_solution_grid.value(r, c)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _number(self, position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_range_constraints()
        self._add_initial_constraints()
        self._add_distinct_constraints()
        self._add_higher_constraints()

    def _add_initial_constraints(self):
        for position, value in [(p, v) for p, v in self._grid if v != -1]:
            self._solver.add(self._number(position) == value)

    def _add_range_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(value >= 1)
            self._solver.add(value <= self.columns_number)

    def _add_distinct_constraints(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(Distinct(row))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(Distinct(column))

    def _add_higher_constraints(self):
        for first_position, second_position in self._higher_positions:
            self._solver.add(self._number(first_position) > self._number(second_position))
