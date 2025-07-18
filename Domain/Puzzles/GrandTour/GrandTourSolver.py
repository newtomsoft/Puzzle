﻿from z3 import Solver, Not, And, Int, sat

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class GrandTourSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._init_island_grid()
        self._solver = Solver()
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._input_grid.columns_number)] for r in range(self._input_grid.rows_number)]
        )

    def _init_solver(self):
        self._island_bridges_z3 = {
            island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()}
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = model.eval(bridges).as_long()
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(
                            self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[
                        position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            not_loop_constraints = []
            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        cell_constraints.append(self._island_bridges_z3[position][direction] == value)
                not_loop_constraints.append(Not(And(cell_constraints)))
            self._solver.add(And(not_loop_constraints))
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_all_cells_crossed_constraints()
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()

    def _add_all_cells_crossed_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            for bridges in direction_bridges.values():
                self._solver.add(And(bridges >= 0, bridges <= 1))
            self._solver.add(sum(direction_bridges.values()) == 2)

    def _add_initial_constraints(self):
        for position, island in [(position, island) for position, island in self._input_grid if isinstance(island, Island)]:
            if island.bridges_number(Direction.right()) > 0:
                self._solver.add(self._island_bridges_z3[position][Direction.right()] == island.bridges_number(Direction.right()))
            if island.bridges_number(Direction.down()) > 0:
                self._solver.add(self._island_bridges_z3[position][Direction.down()] == island.bridges_number(Direction.down()))
            if island.bridges_number(Direction.left()) > 0:
                self._solver.add(self._island_bridges_z3[position][Direction.left()] == island.bridges_number(Direction.left()))
            if island.bridges_number(Direction.up()) > 0:
                self._solver.add(self._island_bridges_z3[position][Direction.up()] == island.bridges_number(Direction.up()))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] ==
                                     self._island_bridges_z3[island.direction_position_bridges[direction][0]][direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)
