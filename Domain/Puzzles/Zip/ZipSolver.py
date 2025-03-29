﻿from Board.LinearPathGrid import LinearPathGrid
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from GameSolver import GameSolver


class ZipSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._path_positions = set([position for position, value in self._grid if value == 0])
        self._checkpoints = {value: position for position, value in self._grid if value > 0}
        self._start_position = self._checkpoints[min(self._checkpoints.keys())]
        self._finish_position = self._checkpoints[max(self._checkpoints.keys())]
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid, list[Position]):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._grid_z3.copy_walls_from_grid(self._grid)
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> (Grid, list[Position]):
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        while self._solver.has_solution():
            grid_solution = Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
            grid_solution.set_walls(self._grid.walls)
            linear_path_grid = LinearPathGrid.from_grid_and_checkpoints(grid_solution, self._checkpoints)
            if linear_path_grid == Grid.empty():
                self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in grid_solution])))
                continue
            self._previous_solution = grid_solution
            return linear_path_grid
        return Grid.empty()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_finish_checkpoint_no_same_value_neighbors_constraints()
        self._add_checkpoints_neighbors_count_constraints()
        self._add_path_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position in self._checkpoints.values():
            self._solver.add(self._grid_z3[position] == self._grid[position])
        for position in self._path_positions:
            self._solver.add(self._grid_z3[position] >= self._grid[self._start_position])
            self._solver.add(self._grid_z3[position] < self._grid[self._finish_position])

    def _add_finish_checkpoint_no_same_value_neighbors_constraints(self):
        neighbors_values = self._get_neighbors_values(self._finish_position)
        finish_value = self._grid[self._finish_position]
        self._solver.add([neighbor_value != finish_value for neighbor_value in neighbors_values])

    def _add_path_neighbors_count_constraints(self):
        for position in self._path_positions:
            neighbors_values = self._get_neighbors_values(position)
            same_value_neighbors_count = self._solver.sum([self._grid_z3[position] == neighbor_value for neighbor_value in neighbors_values])
            self._solver.add(same_value_neighbors_count >= 2)

    def _add_checkpoints_neighbors_count_constraints(self):
        self._add_checkpoint_same_neighbors_count_constraint(self._start_position)
        self._add_checkpoint_minus_one_same_neighbors_count_constraint(self._finish_position)

        for position in set(self._checkpoints.values()) - {self._start_position, self._finish_position}:
            self._add_checkpoint_same_neighbors_count_constraint(position)
            self._add_checkpoint_minus_one_same_neighbors_count_constraint(position)

    def _add_checkpoint_same_neighbors_count_constraint(self, position):
        neighbors_values = self._get_neighbors_values(position)
        checkpoint_value = self._grid[position]
        same_value_neighbors_count = self._solver.sum([neighbor_value == checkpoint_value for neighbor_value in neighbors_values])
        self._solver.add(same_value_neighbors_count >= 1)

    def _add_checkpoint_minus_one_same_neighbors_count_constraint(self, position):
        neighbors_values = self._get_neighbors_values(position)
        previous_checkpoint_value = self._grid_z3[position] - 1
        minus_one_same_value_neighbors_count = self._solver.sum([neighbor_value == previous_checkpoint_value for neighbor_value in neighbors_values])
        self._solver.add(minus_one_same_value_neighbors_count >= 1)

    def _get_neighbors_values(self, position):
        neighbors_positions = self._grid_z3.neighbors_positions(position)
        neighbors_values = (
                [self._grid_z3[position] for position in neighbors_positions if position not in self._checkpoints.values()] +
                [self._grid[position] for position in neighbors_positions if position in self._checkpoints.values()] +
                [self._grid[position] - 1 for position in neighbors_positions if position in set(self._checkpoints.values()) - {self._start_position}]
        )
        return neighbors_values
