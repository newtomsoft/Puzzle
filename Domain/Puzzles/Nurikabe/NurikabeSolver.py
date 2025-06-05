from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


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
        self._river_size = self.rows_number * self.columns_number - sum(self.islands_size) # Corrected from rows_number * rows_number
        self._model = cp_model.CpModel()
        self._grid_z3 = Grid([[self._model.NewIntVar(0, self.islands_count, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution = None

    def get_solution(self) -> Grid:
        self._add_constraints()

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            self._previous_solution = Grid.empty()
            return self._previous_solution

        self._previous_solution = Grid([[1 if solver.Value(self._grid_z3[Position(i, j)]) == 0 else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def get_other_solution(self):
        if self._previous_solution is None or self._previous_solution.is_empty():
            # No solution found previously, or it was empty, so just try to find a first solution.
            return self.get_solution()

        # Get all cells that were river (value 0) in the previous solution
        previous_river_cells = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._previous_solution[r][c] == 1: # 1 means river in the output grid
                    previous_river_cells.append(self._grid_z3[r][c])

        if not previous_river_cells: # Should not happen if a solution was found
            return self.get_solution()

        # Add a constraint that not all of these cells can be river again
        # This means at least one of them must not be 0 (river)
        bool_vars_for_prev_solution = []
        for i, cell_var in enumerate(previous_river_cells):
            b = self._model.NewBoolVar(f'prev_sol_cell_{i}_not_river')
            self._model.Add(cell_var != 0).OnlyEnforceIf(b)
            self._model.Add(cell_var == 0).OnlyEnforceIf(b.Not()) # cell_var == 0 means it IS river
            bool_vars_for_prev_solution.append(b)

        if bool_vars_for_prev_solution: # Ensure list is not empty before adding constraint
            self._model.AddBoolOr(bool_vars_for_prev_solution)

        return self.get_solution()

    # def _recompute_river(self, grid): # Commenting out as it uses z3 specifics and complex logic not immediately translatable
    #     rivers = grid.get_all_shapes(1)
    #     biggest_river = max(rivers, key=len)
    #     rivers.remove(biggest_river)
    #     for river in rivers:
    #         not_all_cell_are_river = Not(And([self._grid_z3[position] == 0 for position in river]))
    #         around_river = ShapeGenerator.around_shape(river)
    #         around_river_are_not_all_island = Not(And([self._grid_z3[position] > 0 for position in around_river if position in self._grid]))
    #         constraint = Or(not_all_cell_are_river, around_river_are_not_all_island)
    #         self._model.add(constraint) # This would need proper translation

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
        # Bounds 0 to self.islands_count are set during NewIntVar creation.
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                # self._model.Add(self._grid_z3[r][c] >= 0) # Implicit
                # self._model.Add(self._grid_z3[r][c] <= self.islands_count) # Implicit
                pass

        for i, position in enumerate(self.islands_size_position):
            self._model.Add(self._grid_z3[position] == i + 1) # Island cells are marked with their 1-based index

    def _add_adjacent_1_is_river_constraint(self):
        for position in self.islands_size_position:
            if self._grid[position] == 1: # Island of size 1
                for neighbor in self._grid.neighbors_positions(position):
                    self._model.Add(self._grid_z3[neighbor] == 0) # Neighbors must be river

    def _add_no_square_river_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                # This original check seems to be on the initial grid, not the z3 variables.
                # If it's about the solution, it should apply to self._grid_z3 variables.
                # Assuming the intent is to prevent 2x2 river squares in the solution:
                pos_r_c = self._grid_z3[Position(r, c)]
                pos_r_c1 = self._grid_z3[Position(r, c + 1)]
                pos_r1_c = self._grid_z3[Position(r + 1, c)]
                pos_r1_c1 = self._grid_z3[Position(r + 1, c + 1)]

                # Not(And(g[0,0]==0, g[0,1]==0, g[1,0]==0, g[1,1]==0))
                # This means at least one of them is not 0.
                # Create boolean variables for each condition
                b0 = self._model.NewBoolVar(f'no_square_river_{r}_{c}_b0')
                b1 = self._model.NewBoolVar(f'no_square_river_{r}_{c}_b1')
                b2 = self._model.NewBoolVar(f'no_square_river_{r}_{c}_b2')
                b3 = self._model.NewBoolVar(f'no_square_river_{r}_{c}_b3')

                self._model.Add(pos_r_c != 0).OnlyEnforceIf(b0)
                self._model.Add(pos_r_c == 0).OnlyEnforceIf(b0.Not())

                self._model.Add(pos_r_c1 != 0).OnlyEnforceIf(b1)
                self._model.Add(pos_r_c1 == 0).OnlyEnforceIf(b1.Not())

                self._model.Add(pos_r1_c != 0).OnlyEnforceIf(b2)
                self._model.Add(pos_r1_c == 0).OnlyEnforceIf(b2.Not())

                self._model.Add(pos_r1_c1 != 0).OnlyEnforceIf(b3)
                self._model.Add(pos_r1_c1 == 0).OnlyEnforceIf(b3.Not())

                self._model.AddBoolOr([b0, b1, b2, b3])

    def add_connected_cells_in_region_constraints(self, step_vars, region_id, region_size):
        # Constraint: The number of cells in this region must match the expected size.
        cells_in_region_bools = []
        for r_idx in range(self.rows_number):
            for c_idx in range(self.columns_number):
                is_cell_region = self._model.NewBoolVar(f'is_cell_region_{region_id}_{r_idx}_{c_idx}')
                self._model.Add(self._grid_z3[r_idx][c_idx] == region_id).OnlyEnforceIf(is_cell_region)
                self._model.Add(self._grid_z3[r_idx][c_idx] != region_id).OnlyEnforceIf(is_cell_region.Not())
                cells_in_region_bools.append(is_cell_region)
        self._model.Add(sum(cells_in_region_bools) == region_size)

        # Constraint: Exactly one cell in the region must be marked as step 1 (the root).
        # step_vars are already NewIntVar(0, max_steps, ...)
        # max_steps can be region_size for islands or _river_size for river
        max_steps = region_size
        root_bool_vars = []
        for r_idx in range(self.rows_number):
            for c_idx in range(self.columns_number):
                # is_cell_region was defined above for the size constraint, but we need it linked to step_vars here.
                # Let's create specific bools for root condition.
                # Condition: cell is part of region AND step is 1
                is_cell_region_for_root = self._model.NewBoolVar(f'is_cell_region_for_root_{region_id}_{r_idx}_{c_idx}')
                self._model.Add(self._grid_z3[r_idx][c_idx] == region_id).OnlyEnforceIf(is_cell_region_for_root)
                self._model.Add(self._grid_z3[r_idx][c_idx] != region_id).OnlyEnforceIf(is_cell_region_for_root.Not())

                is_step_one = self._model.NewBoolVar(f'is_step_one_{region_id}_{r_idx}_{c_idx}')
                self._model.Add(step_vars[r_idx][c_idx] == 1).OnlyEnforceIf(is_step_one)
                self._model.Add(step_vars[r_idx][c_idx] != 1).OnlyEnforceIf(is_step_one.Not())

                is_root = self._model.NewBoolVar(f'is_root_{region_id}_{r_idx}_{c_idx}')
                self._model.AddBoolAnd([is_cell_region_for_root, is_step_one]).OnlyEnforceIf(is_root)
                self._model.AddBoolOr([is_cell_region_for_root.Not(), is_step_one.Not()]).OnlyEnforceIf(is_root.Not())
                root_bool_vars.append(is_root)
        self._model.Add(sum(root_bool_vars) == 1)


        for r_idx in range(self.rows_number):
            for c_idx in range(self.columns_number):
                current_cell_var = self._grid_z3[r_idx][c_idx]
                current_step_var = step_vars[r_idx][c_idx]

                # If a cell is part of the region, its step must be >= 1. Otherwise, step must be 0.
                is_cell_region_cond = self._model.NewBoolVar(f'is_cell_region_cond_{region_id}_{r_idx}_{c_idx}')
                self._model.Add(current_cell_var == region_id).OnlyEnforceIf(is_cell_region_cond)
                self._model.Add(current_cell_var != region_id).OnlyEnforceIf(is_cell_region_cond.Not())

                self._model.Add(current_step_var >= 1).OnlyEnforceIf(is_cell_region_cond)
                self._model.Add(current_step_var == 0).OnlyEnforceIf(is_cell_region_cond.Not())
                # Ensure step value does not exceed max_steps if it's part of the region
                self._model.Add(current_step_var <= max_steps).OnlyEnforceIf(is_cell_region_cond)


                # If cell is in region and step > 1, it must have a neighbor in region with step - 1
                is_current_step_gt_1 = self._model.NewBoolVar(f'is_step_gt_1_{region_id}_{r_idx}_{c_idx}')
                self._model.Add(current_step_var > 1).OnlyEnforceIf(is_current_step_gt_1)
                self._model.Add(current_step_var <= 1).OnlyEnforceIf(is_current_step_gt_1.Not())

                antecedent_is_true = self._model.NewBoolVar(f'antecedent_connectivity_{region_id}_{r_idx}_{c_idx}')
                self._model.AddBoolAnd([is_cell_region_cond, is_current_step_gt_1]).OnlyEnforceIf(antecedent_is_true)
                self._model.AddBoolOr([is_cell_region_cond.Not(), is_current_step_gt_1.Not()]).OnlyEnforceIf(antecedent_is_true.Not())

                adj_conditions = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r_idx + dr, c_idx + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        adj_cell_var = self._grid_z3[nr][nc]
                        adj_step_var = step_vars[nr][nc]

                        # Condition: adj_cell_var == region_id AND adj_step_var == current_step_var - 1
                        adj_cell_is_region = self._model.NewBoolVar(f'adj_is_region_{region_id}_{r_idx}_{c_idx}_{nr}_{nc}')
                        self._model.Add(adj_cell_var == region_id).OnlyEnforceIf(adj_cell_is_region)
                        self._model.Add(adj_cell_var != region_id).OnlyEnforceIf(adj_cell_is_region.Not())

                        adj_step_is_prev = self._model.NewBoolVar(f'adj_step_prev_{region_id}_{r_idx}_{c_idx}_{nr}_{nc}')
                        self._model.Add(adj_step_var == current_step_var - 1).OnlyEnforceIf(adj_step_is_prev)
                        # We need to be careful with domain of current_step_var - 1 if current_step_var is an Intvar.
                        # However, current_step_var > 1 is already part of the antecedent. So current_step_var-1 >= 1.

                        # For Add(A == B - C), B and C must be constants or variables. A must be a variable.
                        # Here, adj_step_var == current_step_var - 1 is a comparison, so it's fine.

                        adj_combined_cond = self._model.NewBoolVar(f'adj_comb_{region_id}_{r_idx}_{c_idx}_{nr}_{nc}')
                        self._model.AddBoolAnd([adj_cell_is_region, adj_step_is_prev]).OnlyEnforceIf(adj_combined_cond)
                        self._model.AddBoolOr([adj_cell_is_region.Not(), adj_step_is_prev.Not()]).OnlyEnforceIf(adj_combined_cond.Not())
                        adj_conditions.append(adj_combined_cond)

                if adj_conditions: # Only add if there are valid neighbors
                    self._model.AddBoolOr(adj_conditions).OnlyEnforceIf(antecedent_is_true)
                elif antecedent_is_true: # If antecedent is true but no valid neighbors (e.g. 1x1 grid and step > 1), then it's a contradiction.
                    # This case should ideally be prevented by other constraints (e.g. step cannot be > 1 if no valid prev step exists)
                    # For safety, we can state that antecedent cannot be true if no adj_conditions.
                    self._model.Add(antecedent_is_true == False)


    def _add_island_regions_constraints(self):
        max_island_size = max(self.islands_size) if self.islands_size else 0
        # Max step can be the size of the island
        steps_vars_per_island = [
            [[self._model.NewIntVar(0, max_island_size, f"step_island_{island_idx}_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
            for island_idx in range(self.islands_count)
        ]

        for island_idx in range(self.islands_count):
            region_id = island_idx + 1  # Island IDs are 1-based
            island_size = self.islands_size[island_idx]
            current_island_step_vars = steps_vars_per_island[island_idx]
            self.add_connected_cells_in_region_constraints(current_island_step_vars, region_id, island_size)

    def _add_river_if_2_island_area_diagonal_adjacent_constraint(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                # This constraint is based on the initial grid values, not the solution variables.
                # If cell (r,c) has an island number and (r+1,c+1) has an island number,
                # then (r+1,c) and (r,c+1) must be river (0) in the solution.
                if self._grid.value(r, c) > 0 and self._grid.value(r + 1, c + 1) > 0:
                    self._model.Add(self._grid_z3[Position(r + 1, c)] == 0)
                    self._model.Add(self._grid_z3[Position(r, c + 1)] == 0)

        for r in range(self.rows_number - 1):
            for c in range(1, self.columns_number):
                # Similar logic for the other diagonal
                if self._grid.value(r, c) > 0 and self._grid.value(r + 1, c - 1) > 0:
                    self._model.Add(self._grid_z3[Position(r + 1, c)] == 0)
                    self._model.Add(self._grid_z3[Position(r, c - 1)] == 0)

    def _add_river_between_2_island_area_constraint(self):
        for r in range(self.rows_number - 2):
            for c in range(self.columns_number - 2):
                position = Position(r, c)
                if self._grid[position] == 0: # If current cell in initial grid is not an island, skip
                    continue

                # Check down by 2
                pos_down_2 = position.after(Direction.down(), 2)
                if pos_down_2 in self._grid and self._grid[pos_down_2] > 0: # If cell (r+2,c) is an island
                    middle_position = position.after(Direction.down(), 1) # Cell (r+1,c)
                    self._model.Add(self._grid_z3[middle_position] == 0) # Must be river

                # Check right by 2
                pos_right_2 = position.after(Direction.right(), 2)
                if pos_right_2 in self._grid and self._grid[pos_right_2] > 0: # If cell (r,c+2) is an island
                    middle_position = position.after(Direction.right(), 1) # Cell (r,c+1)
                    self._model.Add(self._grid_z3[middle_position] == 0) # Must be river


    def _add_river_region_constraint(self):
        # River is region_id = 0
        region_id_river = 0

        # Max step can be the total number of river cells
        river_step_vars = [[self._model.NewIntVar(0, self._river_size if self._river_size > 0 else 1, f"step_river_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]

        # Constraint: The number of river cells must match self._river_size
        river_cells_bools = []
        for r_idx in range(self.rows_number):
            for c_idx in range(self.columns_number):
                is_cell_river = self._model.NewBoolVar(f'is_cell_river_{r_idx}_{c_idx}')
                self._model.Add(self._grid_z3[r_idx][c_idx] == region_id_river).OnlyEnforceIf(is_cell_river)
                self._model.Add(self._grid_z3[r_idx][c_idx] != region_id_river).OnlyEnforceIf(is_cell_river.Not())
                river_cells_bools.append(is_cell_river)

        if self._river_size > 0 : # Only add count constraint if river is expected
             self._model.Add(sum(river_cells_bools) == self._river_size)
        else: # No river cells expected
             self._model.Add(sum(river_cells_bools) == 0)
             # If no river cells, no need for further connectivity constraints for river
             return


        # Constraint: Exactly one river cell must be marked as step 1 (the root of the river).
        root_bool_vars = []
        for r_idx in range(self.rows_number):
            for c_idx in range(self.columns_number):
                is_cell_river_for_root = self._model.NewBoolVar(f'is_cell_river_for_root_{r_idx}_{c_idx}')
                self._model.Add(self._grid_z3[r_idx][c_idx] == region_id_river).OnlyEnforceIf(is_cell_river_for_root)
                self._model.Add(self._grid_z3[r_idx][c_idx] != region_id_river).OnlyEnforceIf(is_cell_river_for_root.Not())

                is_step_one = self._model.NewBoolVar(f'is_step_one_river_{r_idx}_{c_idx}')
                self._model.Add(river_step_vars[r_idx][c_idx] == 1).OnlyEnforceIf(is_step_one)
                self._model.Add(river_step_vars[r_idx][c_idx] != 1).OnlyEnforceIf(is_step_one.Not())

                is_root = self._model.NewBoolVar(f'is_root_river_{r_idx}_{c_idx}')
                self._model.AddBoolAnd([is_cell_river_for_root, is_step_one]).OnlyEnforceIf(is_root)
                self._model.AddBoolOr([is_cell_river_for_root.Not(), is_step_one.Not()]).OnlyEnforceIf(is_root.Not())
                root_bool_vars.append(is_root)
        self._model.Add(sum(root_bool_vars) == 1) # One root for the river path


        for r_idx in range(self.rows_number):
            for c_idx in range(self.columns_number):
                current_cell_var = self._grid_z3[r_idx][c_idx]
                current_step_var = river_step_vars[r_idx][c_idx]

                # If a cell is river, its step must be >= 1. Otherwise, step must be 0.
                is_cell_river_cond = self._model.NewBoolVar(f'is_cell_river_cond_path_{r_idx}_{c_idx}')
                self._model.Add(current_cell_var == region_id_river).OnlyEnforceIf(is_cell_river_cond)
                self._model.Add(current_cell_var != region_id_river).OnlyEnforceIf(is_cell_river_cond.Not())

                self._model.Add(current_step_var >= 1).OnlyEnforceIf(is_cell_river_cond)
                self._model.Add(current_step_var == 0).OnlyEnforceIf(is_cell_river_cond.Not())
                # Ensure step value does not exceed _river_size if it's part of the river
                self._model.Add(current_step_var <= self._river_size).OnlyEnforceIf(is_cell_river_cond)


                # If cell is river and step > 1, it must have a neighbor river cell with step - 1
                is_current_step_gt_1 = self._model.NewBoolVar(f'is_step_gt_1_river_{r_idx}_{c_idx}')
                self._model.Add(current_step_var > 1).OnlyEnforceIf(is_current_step_gt_1)
                self._model.Add(current_step_var <= 1).OnlyEnforceIf(is_current_step_gt_1.Not())

                antecedent_is_true = self._model.NewBoolVar(f'antecedent_connectivity_river_{r_idx}_{c_idx}')
                self._model.AddBoolAnd([is_cell_river_cond, is_current_step_gt_1]).OnlyEnforceIf(antecedent_is_true)
                self._model.AddBoolOr([is_cell_river_cond.Not(), is_current_step_gt_1.Not()]).OnlyEnforceIf(antecedent_is_true.Not())

                adj_conditions = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r_idx + dr, c_idx + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        adj_cell_var = self._grid_z3[nr][nc]
                        adj_step_var = river_step_vars[nr][nc]

                        adj_cell_is_river = self._model.NewBoolVar(f'adj_is_river_{r_idx}_{c_idx}_{nr}_{nc}')
                        self._model.Add(adj_cell_var == region_id_river).OnlyEnforceIf(adj_cell_is_river)
                        self._model.Add(adj_cell_var != region_id_river).OnlyEnforceIf(adj_cell_is_river.Not())

                        adj_step_is_prev = self._model.NewBoolVar(f'adj_step_prev_river_{r_idx}_{c_idx}_{nr}_{nc}')
                        self._model.Add(adj_step_var == current_step_var - 1).OnlyEnforceIf(adj_step_is_prev)

                        adj_combined_cond = self._model.NewBoolVar(f'adj_comb_river_{r_idx}_{c_idx}_{nr}_{nc}')
                        self._model.AddBoolAnd([adj_cell_is_river, adj_step_is_prev]).OnlyEnforceIf(adj_combined_cond)
                        self._model.AddBoolOr([adj_cell_is_river.Not(), adj_step_is_prev.Not()]).OnlyEnforceIf(adj_combined_cond.Not())
                        adj_conditions.append(adj_combined_cond)

                if adj_conditions:
                    self._model.AddBoolOr(adj_conditions).OnlyEnforceIf(antecedent_is_true)
                elif antecedent_is_true:
                    self._model.Add(antecedent_is_true == False) # Should not happen if step > 1

    def _is_adjacent_with_other_island_size(self, position: Position, position_origin: Position):
        return any([self._grid[adjacent_position] for adjacent_position in self._grid.neighbors_positions(position) if adjacent_position != position_origin]) > 0

    def _add_river_around_islands(self):
        for i, position in enumerate(self.islands_size_position):
            island_id = i + 1 # Island IDs are 1-based
            for adjacent_position in self._grid.neighbors_positions(position):
                # For each neighbor of an island cell, it must either be river (0) or part of the same island (island_id)
                var_adj = self._grid_z3[adjacent_position]

                # self._model.Add(Or(var_adj == 0, var_adj == island_id))
                # This can be translated to AddBoolOr with boolean variables for each condition
                b0 = self._model.NewBoolVar(f'adj_{adjacent_position.r}_{adjacent_position.c}_is_river_for_island_{island_id}')
                b1 = self._model.NewBoolVar(f'adj_{adjacent_position.r}_{adjacent_position.c}_is_part_of_island_{island_id}')

                self._model.Add(var_adj == 0).OnlyEnforceIf(b0)
                self._model.Add(var_adj != 0).OnlyEnforceIf(b0.Not())

                self._model.Add(var_adj == island_id).OnlyEnforceIf(b1)
                self._model.Add(var_adj != island_id).OnlyEnforceIf(b1.Not())

                self._model.AddBoolOr([b0, b1])
