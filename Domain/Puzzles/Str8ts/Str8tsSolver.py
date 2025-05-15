from z3 import Solver, Not, And, unsat, Int, Distinct, If

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class Str8tsSolver:
    def __init__(self, numbers_grid: Grid[int], blacks_grid: Grid[bool]):
        self._numbers_grid = numbers_grid
        self._blacks_grid = blacks_grid
        self._rows_number = self._numbers_grid.rows_number
        self._columns_number = self._numbers_grid.columns_number
        if self._rows_number != self._columns_number:
            raise ValueError("Str8ts has to be a square")
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self._blank_grid = self._get_blank_grid()

    def _get_blank_grid(self):
        blank_grid = Grid([[False for c in range(self._columns_number)] for r in range(self._rows_number)])
        for position, value in [(position, value) for position, value in self._numbers_grid if value == 0 and self._blacks_grid[position] == False]:
            blank_grid.set_value(position, True)
        return blank_grid

    def get_solution(self) -> (Grid, Grid):
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution, self._blank_grid

    def get_other_solution(self) -> (Grid, Grid):
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution if value > 0])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution, self._blank_grid

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        solution_with_black_negative = Grid([[(model.eval(self._grid_z3.value(i, j))).as_long() for j in range(self._columns_number)] for i in range(self._rows_number)])
        solution = Grid([[max(0, solution_with_black_negative.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_distinct_constraints()
        self._add_consecutive_constraints()

    def _add_initial_constraints(self):
        for position, value in [(position, value) for position, value in self._numbers_grid if value > 0]:
            self._solver.add(self._grid_z3[position] == value)

        black_count = 0
        for position, is_black in self._blacks_grid:
            if is_black and self._numbers_grid[position] == 0:
                black_count += 1
                self._solver.add(self._grid_z3[position] == -black_count)
            else:
                self._solver.add(self._grid_z3[position] > 0)
                self._solver.add(self._grid_z3[position] <= self._rows_number)

    def _add_distinct_constraints(self):
        for index, row in enumerate(self._grid_z3.matrix):
            self._solver.add(Distinct(row))

        for index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            self._solver.add(Distinct(column))

    def _add_consecutive_constraints(self):
        for column_index, row in enumerate(self._grid_z3.matrix):
            groups = self._build_groups(column_index, row, "row")
            self.add_consecutive_for_groups_constraints(groups)

        for row_index, column_tuple in enumerate(zip(*self._grid_z3.matrix)):
            column = list(column_tuple)
            groups = self._build_groups(row_index, column, "column")
            self.add_consecutive_for_groups_constraints(groups)

    def _build_groups(self, line_index: int, line: list, type_line: str = "column"):
        groups = []
        current_group = []
        for other_line_type_index, cell in enumerate(line):
            position = Position(other_line_type_index, line_index) if type_line == "column" else Position(line_index, other_line_type_index)
            if self._blacks_grid[position]:
                if current_group:
                    groups.append(current_group)
                    current_group = []
            else:
                current_group.append(cell)
        if current_group:
            groups.append(current_group)
        return groups

    def add_consecutive_for_groups_constraints(self, groups: list[list]):
        for cells in groups:
            if len(cells) < 2:
                continue
            self.add_consecutive_constraint(cells)

    def add_consecutive_constraint(self, cells: list):
        min_val = cells[0]
        max_val = cells[0]
        for i in range(1, len(cells)):
            min_val = If(cells[i] < min_val, cells[i], min_val)
            max_val = If(cells[i] > max_val, cells[i], max_val)

        self._solver.add(max_val - min_val == len(cells) - 1)

