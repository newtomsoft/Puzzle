﻿from z3 import Solver, Bool, Not, And, unsat, Or, Implies, is_true

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class AquariumSolver(GameSolver):
    def __init__(self, grid: Grid, numbers: list[int]):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        self._aquariums = self._grid.get_regions()
        if len(self._aquariums) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._numbers = numbers
        self.columns_water_numbers = numbers[:grid.rows_number]
        self.rows_water_numbers = numbers[grid.rows_number:]
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3[Position(i, j)])) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_sum_constraints()
        self._add_aquariums_constraints()

    def _add_sum_constraints(self):
        for i, row in enumerate(self._grid_z3.matrix):
            self._solver.add(sum(row) == self.rows_water_numbers[i])
        for i, column in enumerate(zip(*self._grid_z3.matrix)):
            self._solver.add(sum(column) == self.columns_water_numbers[i])

    def _add_aquariums_constraints(self):
        for positions in self._aquariums.values():
            cells_by_row_index = {}
            for position in positions:
                r, c = position
                if r not in cells_by_row_index:
                    cells_by_row_index[r] = []
                cells_by_row_index[r].append(position)
            for aquarium_row_cells in cells_by_row_index.values():
                if len(positions) > 1:
                    all_cells_full = And([self._grid_z3[position] for position in aquarium_row_cells])
                    all_cells_empty = And([Not(self._grid_z3[position]) for position in aquarium_row_cells])
                    self._solver.add(Or(all_cells_full, all_cells_empty))

                row = aquarium_row_cells[0][0]
                column = aquarium_row_cells[0][1]
                z3_down_cells_full = [self._grid_z3[position] for position in [position for position in positions if position[0] > row]]
                z3_cell_full = self._grid_z3[row][column]
                if len(z3_down_cells_full) > 0:
                    full_implies_down_full = Implies(z3_cell_full, And(z3_down_cells_full))
                    self._solver.add(full_implies_down_full)
                z3_up_cells_empty = [Not(self._grid_z3[position]) for position in [position for position in positions if position[0] < row]]
                if len(z3_up_cells_empty) > 0:
                    empty_implies_up_empty = Implies(Not(z3_cell_full), And(z3_up_cells_empty))
                    self._solver.add(empty_implies_up_empty)
