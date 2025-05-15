﻿from collections import defaultdict

from z3 import Solver, Not, And, Or, Implies, Int, sat, If

from Domain.Board.Grid import Grid
from Domain.Board.LinearPathGrid import LinearPathGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NumberChainSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._start_position = Position(0, 0)
        self._end_position = Position(self._grid.rows_number - 1, self._grid.columns_number - 1)
        self._start_value = self._grid[self._start_position]
        self._end_value = self._grid[self._end_position]
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution if value > 0])))
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        while self._solver.check() == sat:
            model = self._solver.model()
            matrix_number = [[(model.eval(self._grid_z3.value(i, j))).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)]
            attempt = Grid(matrix_number)
            attempt_bool = Grid([[True if matrix_number[i][j] > 0 else False for j in range(self.columns_number)] for i in range(self.rows_number)])
            attempt_bool.set_value(self._end_position, 2)
            linear_path_grid = LinearPathGrid.from_grid_and_checkpoints(attempt_bool, {1: self._start_position, 2: self._end_position})
            if linear_path_grid == Grid.empty():
                self._solver.add(Not(And([self._grid_z3[position] == value for position, value in attempt if value > 0])))
                continue
            self._previous_solution = attempt
            return linear_path_grid
        return Grid.empty()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_way_cells_count_constraint()
        self._add_way_distinct_cells_constraint()
        self._add_neighbors_count_constraints()

    def _add_initial_constraints(self):
        self._solver.add(self._grid_z3[self._start_position] == self._start_value)
        self._solver.add(self._grid_z3[self._end_position] == self._end_value)
        for position, value in self._grid_z3:
            self._solver.add(value >= -self._end_value)
            self._solver.add(value <= self._end_value)

    def _add_neighbors_count_constraints(self):
        same_value_start_position_neighbors_count = self._same_value_neighbors_count(self._start_position)
        self._solver.add(same_value_start_position_neighbors_count >= 1)

        same_value_end_position_neighbors_count = self._same_value_neighbors_count(self._end_position)
        self._solver.add(same_value_end_position_neighbors_count >= 1)

        for position in [position for position, _ in self._grid if position != self._start_position and position != self._end_position]:
            same_value_start_position_neighbors_count = self._same_value_neighbors_count(position)
            self._solver.add(Implies(self._grid_z3[position] > 0, same_value_start_position_neighbors_count >= 2))

    def _same_value_neighbors_count(self, position):
        return sum([neighbor_value > 0 for neighbor_value in self._grid_z3.neighbors_values(position)])

    def _add_way_cells_count_constraint(self):
        self._solver.add(sum([If(self._grid_z3[position] > 0, 1, 0) for position, _ in self._grid]) == self._end_value)

    def _add_way_distinct_cells_constraint(self):
        values_to_positions = defaultdict(list)
        for position, value in [(position, value) for position, value in self._grid if value > 0]:
            values_to_positions[value].append(position)

        for value, positions in values_to_positions.items():
            if len(positions) == 1:
                self._solver.add(self._grid_z3[positions[0]] == value)
                continue
            for index, position in enumerate(positions):
                self._solver.add(Or(self._grid_z3[position] == value, self._grid_z3[position] == -index))
            self._solver.add(sum([If(self._grid_z3[position] == value, 1, 0) for position in positions]) == 1)
