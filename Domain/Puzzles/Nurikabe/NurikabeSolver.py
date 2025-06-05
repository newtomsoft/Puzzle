from z3 import Solver, Not, And, Or, Implies, sat, If, Sum, Int

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NurikabeSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 5 or self.columns_number < 5:
            raise ValueError("The grid must be at least 5x5")
        self.islands_size = [self._grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if self._grid.value(r, c) > 0]
        self.islands_size_position = [Position(r, c) for r in range(self.rows_number) for c in range(self.columns_number) if self._grid.value(r, c) > 0]
        self.islands_count = len(self.islands_size)
        self._river_size = self.rows_number * self.rows_number - sum(self.islands_size)
        self._solver = Solver()
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution = None

    def get_solution(self) -> Grid:
        self._add_constraints()

        if self._solver.check() != sat:
            self._previous_solution = Grid.empty()
            return self._previous_solution

        model = self._solver.model()
        self._previous_solution = Grid([[1 if (model.eval(self._grid_z3[Position(i, j)])).as_long() == 0 else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def get_other_solution(self):
        rivers_cells = self._previous_solution.get_all_shapes(1)
        self._solver.add(Not(And([self._grid_z3[river_cell] == 0 for river_cells in rivers_cells for river_cell in river_cells])))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_island_regions_constraints()
        self._add_river_region_constraint()
        self._add_no_square_river_constraint()
        self._add_river_around_islands()
        self._add_adjacent_1_is_river_constraint()
        self._add_river_between_2_island_area_constraint()
        self._add_river_if_2_island_area_diagonal_adjacent_constraint()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._solver.add(self._grid_z3[r][c] >= 0)
                self._solver.add(self._grid_z3[r][c] <= self.islands_count)

        constraints = [self._grid_z3[position] == i + 1 for i, position in enumerate(self.islands_size_position)]
        self._solver.add(constraints)

    def _add_adjacent_1_is_river_constraint(self):
        for position in self.islands_size_position:
            if self._grid[position] == 1:
                for neighbor in self._grid.neighbors_positions(position):
                    self._solver.add(self._grid_z3[neighbor] == 0)

    def _add_no_square_river_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) == 0 and self._grid.value(r + 1, c) == 0 and self._grid.value(r, c + 1) == 0 and self._grid.value(r + 1, c + 1) == 0:
                    pos_r_c = Position(r, c)
                    pos_r_c1 = Position(r, c + 1)
                    pos_r1_c = Position(r + 1, c)
                    pos_r1_c1 = Position(r + 1, c + 1)
                    self._solver.add(Not(And(self._grid_z3[pos_r_c] == 0, self._grid_z3[pos_r_c1] == 0, self._grid_z3[pos_r1_c] == 0, self._grid_z3[pos_r1_c1] == 0)))

    def add_connected_cells_in_region_constraints(self, step, region_id):
        self._solver.add(Sum([self._grid_z3[i][j] == region_id for i in range(self.rows_number) for j in range(self.columns_number)]) == self.islands_size[region_id - 1])

        roots = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                roots.append(And(self._grid_z3[r][c] == region_id, step[r][c] == 1))
        self._solver.add(Or(roots))

        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                self._solver.add(Not(And(roots[i], roots[j])))

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                current_step = step[r][c]
                self._solver.add(If(self._grid_z3[r][c] == region_id, current_step >= 1, current_step == 0))
                adjacents = []
                if r > 0:
                    adjacents.append(And(self._grid_z3[r - 1][c] == region_id, step[r - 1][c] == current_step - 1))
                if r < self.rows_number - 1:
                    adjacents.append(And(self._grid_z3[r + 1][c] == region_id, step[r + 1][c] == current_step - 1))
                if c > 0:
                    adjacents.append(And(self._grid_z3[r][c - 1] == region_id, step[r][c - 1] == current_step - 1))
                if c < self.columns_number - 1:
                    adjacents.append(And(self._grid_z3[r][c + 1] == region_id, step[r][c + 1] == current_step - 1))

                self._solver.add(Implies(And(self._grid_z3[r][c] == region_id, current_step > 1), Or(adjacents)))

    def _add_island_regions_constraints(self):
        steps = [[[Int(f"step_{i}_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)] for i in range(self.islands_count)]
        for index, step in enumerate(steps):
            region_id = index + 1
            self.add_connected_cells_in_region_constraints(step, region_id)

    def _add_river_if_2_island_area_diagonal_adjacent_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                if self._grid.value(r, c) > 0 and self._grid.value(r + 1, c + 1) > 0:
                    self._solver.add(self._grid_z3[Position(r + 1, c)] == 0)
                    self._solver.add(self._grid_z3[Position(r, c + 1)] == 0)

        for r in range(self.rows_number - 1):
            for c in range(1, self.columns_number):
                if self._grid.value(r, c) > 0 and self._grid.value(r + 1, c - 1) > 0:
                    self._solver.add(self._grid_z3[Position(r + 1, c)] == 0)
                    self._solver.add(self._grid_z3[Position(r, c - 1)] == 0)

    def _add_river_between_2_island_area_constraint(self):
        for r in range(self.rows_number - 2):
            for c in range(self.columns_number - 2):
                position = Position(r, c)
                if self._grid[position] == 0:
                    continue
                neighbors = [position.after(Direction.down(), 2), position.after(Direction.right(), 2)]
                for neighbor_position in neighbors:
                    if neighbor_position in self._grid and self._grid[neighbor_position] > 0:
                        middle_position = (neighbor_position + position) // 2
                        self._solver.add(self._grid_z3[middle_position] == 0)

    def _add_river_region_constraint(self):
        step = [[Int(f'step_river_{i}_{j}') for j in range(self.columns_number)] for i in range(self.rows_number)]
        self._solver.add(Sum([self._grid_z3[i][j] == 0 for i in range(self.rows_number) for j in range(self.columns_number)]) == self._river_size)

        roots = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                roots.append(And(self._grid_z3[r][c] == 0, step[r][c] == 1))
        self._solver.add(Or(roots))

        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                self._solver.add(Not(And(roots[i], roots[j])))

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                current_step = step[r][c]
                self._solver.add(If(self._grid_z3[r][c] == 0, current_step >= 1, current_step == 0))
                adjacents = []
                if r > 0:
                    adjacents.append(And(self._grid_z3[r - 1][c] == 0, step[r - 1][c] == current_step - 1))
                if r < self.rows_number - 1:
                    adjacents.append(And(self._grid_z3[r + 1][c] == 0, step[r + 1][c] == current_step - 1))
                if c > 0:
                    adjacents.append(And(self._grid_z3[r][c - 1] == 0, step[r][c - 1] == current_step - 1))
                if c < self.columns_number - 1:
                    adjacents.append(And(self._grid_z3[r][c + 1] == 0, step[r][c + 1] == current_step - 1))

                self._solver.add(Implies(And(self._grid_z3[r][c] == 0, current_step > 1), Or(adjacents)))

    def _is_adjacent_with_other_island_size(self, position: Position, position_origin: Position):
        return any([self._grid[adjacent_position] for adjacent_position in self._grid.neighbors_positions(position) if adjacent_position != position_origin]) > 0

    def _add_river_around_islands(self):
        for i, position in enumerate(self.islands_size_position):
            island_id = i + 1
            adjacent_positions = self._grid.neighbors_positions(position)
            for adjacent_position in adjacent_positions:
                self._solver.add(Or(self._grid_z3[adjacent_position] == 0, self._grid_z3[adjacent_position] == island_id))
