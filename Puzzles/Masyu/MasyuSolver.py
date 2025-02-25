﻿from typing import Dict

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Island import Island
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class MasyuSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._solver = solver_engine
        self._island_bridges_z3: Dict[Position, Dict[Direction, any]] = {}
        self._last_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: self._solver.int(f"{island.position}_{direction}") for direction in Direction.orthogonal()} for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> (Grid, int):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = model.eval(bridges).as_long()
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._last_solution = self._island_grid
                return self._island_grid, proposition_count

            not_loop_constraints = []
            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        cell_constraints.append(self._island_bridges_z3[position][direction] == value)
                not_loop_constraints.append(self._solver.Not(self._solver.And(cell_constraints)))
            self._solver.add(self._solver.And(not_loop_constraints))
            self.init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._last_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_constraints()

    def _add_initial_constraints(self):
        for _island_bridges_z3 in self._island_bridges_z3.values():
            for direction_bridges in _island_bridges_z3.values():
                self._solver.add(self._solver.Or(direction_bridges == 0, direction_bridges == 1))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][
                        direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            sum_constraint_0 = self._solver.sum(
                [self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 0
            sum_constraint_2 = self._solver.sum(
                [self._island_bridges_z3[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]) == 2
            self._solver.add(self._solver.Or(sum_constraint_0, sum_constraint_2))

    def _add_dots_constraints(self):
        for position, value in self.input_grid:
            if value == 'w':
                horizontal_constraint = False
                vertical_constraint = False
                if position.left in self._island_bridges_z3 and position.right in self._island_bridges_z3:
                    horizontal_constraint = self._solver.And(self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position][Direction.right()] == 1)
                    left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint = False, False, False, False
                    if Direction.up() in self._island_bridges_z3[position.left]:
                        left_up_constraint = self._island_bridges_z3[position.left][Direction.up()] == 1
                    if Direction.down() in self._island_bridges_z3[position.left]:
                        left_down_constraint = self._island_bridges_z3[position.left][Direction.down()] == 1
                    if Direction.up() in self._island_bridges_z3[position.right]:
                        right_up_constraint = self._island_bridges_z3[position.right][Direction.up()] == 1
                    if Direction.down() in self._island_bridges_z3[position.right]:
                        right_down_constraint = self._island_bridges_z3[position.right][Direction.down()] == 1
                    turn_constraint = self._solver.Or(left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint)
                    horizontal_constraint = self._solver.And(horizontal_constraint, turn_constraint)
                if position.up in self._island_bridges_z3 and position.down in self._island_bridges_z3:
                    vertical_constraint = self._solver.And(self._island_bridges_z3[position][Direction.up()] == 1, self._island_bridges_z3[position][Direction.down()] == 1)
                    left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint = False, False, False, False
                    if Direction.left() in self._island_bridges_z3[position.up]:
                        left_up_constraint = self._island_bridges_z3[position.up][Direction.left()] == 1
                    if Direction.right() in self._island_bridges_z3[position.up]:
                        left_down_constraint = self._island_bridges_z3[position.up][Direction.right()] == 1
                    if Direction.left() in self._island_bridges_z3[position.down]:
                        right_up_constraint = self._island_bridges_z3[position.down][Direction.left()] == 1
                    if Direction.right() in self._island_bridges_z3[position.down]:
                        right_down_constraint = self._island_bridges_z3[position.down][Direction.right()] == 1
                    turn_constraint = self._solver.Or(left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint)
                    vertical_constraint = self._solver.And(vertical_constraint, turn_constraint)
                self._solver.add(self._solver.Or(horizontal_constraint, vertical_constraint))
            if value == 'b':
                left_up_constraint, left_down_constraint, right_up_constraint, right_down_constraint = False, False, False, False
                if position.right in self._island_bridges_z3 and position.right.right in self._island_bridges_z3 and position.down in self._island_bridges_z3 and position.down.down in self._island_bridges_z3:
                    right_down_constraint = self._solver.And(
                        self._island_bridges_z3[position][Direction.right()] == 1, self._island_bridges_z3[position.right][Direction.right()] == 1,
                        self._island_bridges_z3[position][Direction.down()] == 1, self._island_bridges_z3[position.down][Direction.down()] == 1)
                if position.left in self._island_bridges_z3 and position.left.left in self._island_bridges_z3 and position.down in self._island_bridges_z3 and position.down.down in self._island_bridges_z3:
                    left_down_constraint = self._solver.And(
                        self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position.left][Direction.left()] == 1,
                        self._island_bridges_z3[position][Direction.down()] == 1, self._island_bridges_z3[position.down][Direction.down()] == 1)
                if position.right in self._island_bridges_z3 and position.right.right in self._island_bridges_z3 and position.up in self._island_bridges_z3 and position.up.up in self._island_bridges_z3:
                    right_up_constraint = self._solver.And(
                        self._island_bridges_z3[position][Direction.right()] == 1, self._island_bridges_z3[position.right][Direction.right()] == 1,
                        self._island_bridges_z3[position][Direction.up()] == 1, self._island_bridges_z3[position.up][Direction.up()] == 1)
                if position.left in self._island_bridges_z3 and position.left.left in self._island_bridges_z3 and position.up in self._island_bridges_z3 and position.up.up in self._island_bridges_z3:
                    left_up_constraint = self._solver.And(
                        self._island_bridges_z3[position][Direction.left()] == 1, self._island_bridges_z3[position.left][Direction.left()] == 1,
                        self._island_bridges_z3[position][Direction.up()] == 1, self._island_bridges_z3[position.up][Direction.up()] == 1)
                self._solver.add(self._solver.Or(right_down_constraint, left_down_constraint, right_up_constraint, left_up_constraint))
