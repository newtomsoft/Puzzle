from typing import Dict

from z3 import Solver, sat, Int, And, Not, Sum, ArithRef, Implies

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class HashiGame:
    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._island_grid = None
        self.init_island_grid()
        self._solver: Solver | None = None
        self._island_bridges_z3: Dict[Position, Dict[Direction, ArithRef]] = {}
        self._last_solution: IslandGrid | None = None

    def init_island_grid(self):
        self._island_grid = IslandGrid(self._input_grid)

    def _init_solver(self):
        orthogonal_directions = [Direction.right(), Direction.down(), Direction.left(), Direction.up()]
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in orthogonal_directions} for island in self._island_grid.islands.values()}
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return IslandGrid.empty()
        model = self._solver.model()
        for position, direction_bridges in self._island_bridges_z3.items():
            for direction, bridges in direction_bridges.items():
                bridges_number = model.eval(bridges).as_long()
                if bridges_number > 0:
                    self._island_grid[position].set_bridge(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                if position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                    self._island_grid[position].direction_position_bridges.pop(direction)
        self._last_solution = self._island_grid
        if not self._island_grid.are_all_islands_connected():
            return self.get_other_solution()
        return self._island_grid

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._last_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self.init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_no_crossing_bridges_constraints()

    def _add_initial_constraints(self):
        for position, direction_bridges in self._island_bridges_z3.items():
            self._solver.add(Sum(list(direction_bridges.values())) == self._island_grid[position].bridges_count)
            for bridges in direction_bridges.values():
                self._solver.add(bridges >= 0, bridges <= 2)

        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is None:
                    self._solver.add((self._island_bridges_z3[island.position][direction] == 0))

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                opposite_direction = direction.opposite
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][opposite_direction])

    def _add_no_crossing_bridges_constraints(self):
        for possible_crossing_bridge in self._island_grid.possible_crossover_bridge:
            first_item, second_item = list(possible_crossing_bridge.items())[:2]
            first_position, first_direction = first_item
            second_position, second_direction = second_item
            self._solver.add(Implies(self._island_bridges_z3[first_position][first_direction] > 0, self._island_bridges_z3[second_position][second_direction] == 0))
            self._solver.add(Implies(self._island_bridges_z3[second_position][second_direction] > 0, self._island_bridges_z3[first_position][first_direction] == 0))
