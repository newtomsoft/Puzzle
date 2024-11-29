﻿from z3 import Solver, Not, And, sat, Sum, Implies, Or, Int, If

from Direction import Direction
from Utils.Grid import Grid


class StitchesGame:
    def __init__(self, grid: Grid, dots_by_column_row: dict[str, list[int]], regions_connections_count: int):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 5:
            raise ValueError("The grid must be at least 5x5")
        self._regions = self._grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self.regions_connections = regions_connections_count
        if regions_connections_count < 1:
            raise ValueError("The grid must require at least 1 connection between regions")
        self._dots_by_column = dots_by_column_row['column']
        self._dots_by_row = dots_by_column_row['row']
        if len(self._dots_by_column) != self.columns_number or len(self._dots_by_row) != self.rows_number:
            raise ValueError("The dots count must have the same size as the columns")
        self._solver = None
        self._matrix_z3 = None
        self._matrix_connexion_z3 = None
        self._last_solution_grid = None

    def _init_solver(self):
        self._matrix_connexion_z3 = [[Int(f"connexion_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid | None:
        if self._solver is None:
            self._init_solver()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[model.eval(self._matrix_connexion_z3[i][j]).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._last_solution_grid = grid
        return grid

    def get_other_solution(self):
        self._exclude_solution(self._last_solution_grid)
        solution = self.get_solution()
        return solution

    def _exclude_solution(self, solution_grid: Grid):
        exclude_constraint = Not(And([self._matrix_connexion_z3[r][c] == solution_grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if solution_grid.value(r, c)]))
        self._solver.add(exclude_constraint)

    def _add_constraints(self):
        self._add_constraint_dots_in_rows_and_columns()
        self._add_constraint_2_dots_crossing_2_regions()
        self._add_constraint_dots_between_regions()

    def _add_constraint_dots_between_regions(self):
        for region_number in self._regions.keys():
            region_positions = self._regions[region_number]
            current_region_with_others_regions = {}
            for position in region_positions:
                neighbors_positions = self._grid.neighbors_positions(position)
                for neighbor_position in neighbors_positions:
                    if (other_region_number := self._grid.value(*neighbor_position)) != region_number:
                        if other_region_number in current_region_with_others_regions.keys():
                            current_region_with_others_regions[other_region_number].add((position, neighbor_position))
                        else:
                            current_region_with_others_regions[other_region_number] = {(position, neighbor_position)}

            all_regions_possible_dot_positions = set()
            for positions in current_region_with_others_regions.values():
                self._add_constraint_dots_between_regions_at(positions)
                all_regions_possible_dot_positions.update(positions0[0] for positions0 in positions)
            if len(all_regions_possible_dot_positions) == 0:
                continue
            constraint_dots_count_for_this_region = Sum([If(self._matrix_connexion_z3[r][c] > 0, 1, 0) for (r, c) in all_regions_possible_dot_positions]) == len(current_region_with_others_regions) * self.regions_connections
            self._solver.add(constraint_dots_count_for_this_region)

    def _add_constraint_dots_between_regions_at(self, positions):
        constraint_connection_region0_to_region1 = Sum([If(self._matrix_connexion_z3[r0][c0] == self._grid.direction_between((r0, c0), (r1, c1)).value, 1, 0) for (r0, c0), (r1, c1) in positions]) == self.regions_connections
        self._solver.add(constraint_connection_region0_to_region1)
        constraint_connection_number_region1_to_region0 = Sum([If(self._matrix_connexion_z3[r1][c1] == self._grid.direction_between((r1, c1), (r0, c0)).value, 1, 0) for (r0, c0), (r1, c1) in positions]) == self.regions_connections
        self._solver.add(constraint_connection_number_region1_to_region0)

    def _add_constraint_dots_in_rows_and_columns(self):
        constraints = []
        for r, row in enumerate(self._matrix_connexion_z3):
            constraints.append(Sum([If(cell > 0, 1, 0) for cell in row]) == self._dots_by_row[r])
        for i, column in enumerate(zip(*self._matrix_connexion_z3)):
            constraints.append(Sum([If(cell > 0, 1, 0) for cell in column]) == self._dots_by_column[i])
        self._solver.add(constraints)

    def _add_constraint_2_dots_crossing_2_regions(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._add_constraint_2_dots_crossing_2_regions_at((r, c))

    def _add_constraint_2_dots_crossing_2_regions_at(self, position):
        r, c = position
        region = self._grid.value(r, c)
        neighbors_positions = self._grid.neighbors_positions(position)
        other_region_positions = []
        for neighbor_position in neighbors_positions:
            if self._grid.value(*neighbor_position) != region:
                other_region_positions.append(neighbor_position)

        self._add_constraint_other_region_dot_positions(position, other_region_positions)

    def _add_constraint_other_region_dot_positions(self, position, other_region_dot_positions):
        r, c = position
        if len(other_region_dot_positions) == 0:
            constraint = self._matrix_connexion_z3[r][c] == 0
            self._solver.add(constraint)
            return

        or_constraints = [self._matrix_connexion_z3[r][c] == Direction.NONE]
        for other_region_dot_position in other_region_dot_positions:
            r_possible, c_possible = other_region_dot_position
            direction = self._grid.direction_between(position, other_region_dot_position)
            or_constraints.append(self._matrix_connexion_z3[r][c] == direction.value)
            constraint_implies = Implies(self._matrix_connexion_z3[r][c] == direction.value, self._matrix_connexion_z3[r_possible][c_possible] == direction.opposite.value)
            self._solver.add(constraint_implies)
        self._solver.add(Or(or_constraints))
