from typing import Dict, List

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class YajilinSolver(GameSolver):
    direction_map = {'R': Direction.right(),
                     'D': Direction.down(),
                     'L': Direction.left(),
                     'U': Direction.up()
                     }
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges_z3: Dict[Position, Dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])
        for position in [position for position, value in self.input_grid if value != '']:
            [self._island_grid[position].set_bridge(neighbor, 0) for neighbor in position.neighbors()]
            self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            for neighbor in position.neighbors():
                if neighbor not in self._island_grid:
                    continue
                self._island_grid[neighbor].set_bridge(position, 0)

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: self._model.NewIntVar(0, 1, f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in self._island_grid.islands.values() if island.bridges_count > 0}
        for position in [position for position, _ in self.input_grid if position not in self._island_bridges_z3]:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._model.Add(self._island_bridges_z3[neighbor][direction] == 0)

        self._black_cells_z3 = {position: self._model.NewBoolVar(f'p{position}') for position, _ in self.input_grid if position in self._island_bridges_z3}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._island_bridges_z3:
            self._init_solver()

        # The main solution seeking loop is within _ensure_all_islands_connected
        solution_grid, _ = self._ensure_all_islands_connected()
        return solution_grid

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        solver = cp_model.CpSolver()
        proposition_count = 0

        while True: # Loop until a fully connected solution is found or no solution
            status = solver.Solve(self._model)
            proposition_count += 1

            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                # Create a temporary grid to represent the current solution
                current_solution_grid = IslandGrid(
                    [[Island(Position(r, c), 0) for c in range(self.input_grid.columns_number)]
                     for r in range(self.input_grid.rows_number)]
                )

                # Populate bridges in current_solution_grid based on solver values
                for island_pos, dir_bridges_vars in self._island_bridges_z3.items():
                    for direction, bridge_var in dir_bridges_vars.items():
                        if solver.Value(bridge_var) == 1:
                            target_pos = island_pos.after(direction)
                            if target_pos in current_solution_grid: # Ensure target is valid
                                # Directly set bridge values; counts will be updated later
                                current_solution_grid[island_pos].set_bridge(current_solution_grid[target_pos], 1)

                # Update bridge counts for all islands in the current solution grid
                for r in range(current_solution_grid.rows_number):
                    for c in range(current_solution_grid.columns_number):
                        pos = Position(r,c)
                        if pos in current_solution_grid:
                           current_solution_grid[pos].set_bridges_count_according_to_directions_bridges()

                # Check connectivity
                connected_components = current_solution_grid.get_connected_positions(exclude_without_bridge=True)

                # Apply fixed values from input_grid (clues) to current_solution_grid
                for r_idx, row in enumerate(self.input_grid.grid):
                    for c_idx, cell_value in enumerate(row):
                        if cell_value != '':
                            current_solution_grid.set_value(Position(r_idx, c_idx), cell_value)

                if len(connected_components) == 1:
                    # Solution is fully connected
                    for p, black_cell_var in self._black_cells_z3.items():
                        if p in current_solution_grid and solver.Value(black_cell_var) == 1:
                            current_solution_grid.set_value(p, '■')

                    self._previous_solution = current_solution_grid
                    return current_solution_grid, proposition_count

                # If not fully connected, or no bridges were formed (empty connected_components)
                if not connected_components: # No bridges at all, or something went wrong
                    # This state means the current model (with prior no-goods) is infeasible for connected solutions
                    return IslandGrid.empty(), proposition_count

                # Add "no-good" constraints to break current set of disconnected components
                # For each component, forbid that exact set of bridge assignments forming it.
                for component in connected_components:
                    component_eq_vars: List[cp_model.BoolVar] = []
                    for island_pos_in_component in component:
                        if island_pos_in_component in self._island_bridges_z3: # Ensure this island has bridge variables
                            # Examine the bridges of this island in the current partial solution
                            # The state of bridges is in current_solution_grid or by querying solver.Value
                            actual_island_in_solution = current_solution_grid[island_pos_in_component]
                            for direction, (_, bridge_val_in_component) in actual_island_in_solution.direction_position_bridges.items():
                                if direction in self._island_bridges_z3[island_pos_in_component]:
                                    bridge_var = self._island_bridges_z3[island_pos_in_component][direction]

                                    # Was this bridge part of *this* component's definition?
                                    # Need to be careful: bridge_val_in_component is from current_solution_grid.
                                    # We need to check if solver.Value(bridge_var) matches bridge_val_in_component.
                                    # This ensures we only constrain variables that led to this specific component structure.

                                    current_solver_val_for_var = solver.Value(bridge_var)
                                    if current_solver_val_for_var == bridge_val_in_component: # Only if this var contributed
                                        eq_var = self._model.NewBoolVar(f"comp_{island_pos_in_component}_{direction}_{bridge_val_in_component}_{proposition_count}")
                                        self._model.Add(bridge_var == bridge_val_in_component).OnlyEnforceIf(eq_var)
                                        self._model.Add(bridge_var != bridge_val_in_component).OnlyEnforceIf(eq_var.Not())
                                        component_eq_vars.append(eq_var)

                    if component_eq_vars:
                        # Forbid this component: Not(And(all component_eq_vars are true))
                        # Which is Or(Not(var1), Not(var2), ...)
                        self._model.AddBoolOr([var.Not() for var in component_eq_vars])

                # self._init_island_grid() # Original z3 code reset a mutable grid. Here, current_solution_grid is fresh.
                                        # The model itself is what we are modifying with AddBoolOr.

            elif status == cp_model.INFEASIBLE:
                return IslandGrid.empty(), proposition_count # No solution found
            else: # UNKNOWN or other status
                return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        if self._previous_solution is None:
            # No first solution found or available, so just try to find one.
            # This might re-solve with existing constraints if called multiple times without success.
            return self.get_solution()

        prev_sol_negation_literals: List[cp_model.BoolVar] = []
        for island_pos, dir_bridge_vars in self._island_bridges_z3.items():
            if island_pos in self._previous_solution: # Ensure island exists in previous solution
                prev_island_state = self._previous_solution[island_pos]
                for direction, bridge_var in dir_bridge_vars.items():
                    # Get the value of this bridge in the previous solution
                    # prev_island_state.direction_position_bridges contains {direction: (Position, value)}
                    if direction in prev_island_state.direction_position_bridges:
                        _, prev_value = prev_island_state.direction_position_bridges[direction]

                        eq_var = self._model.NewBoolVar(f"prev_{island_pos}_{direction}_{prev_value}")
                        self._model.Add(bridge_var == prev_value).OnlyEnforceIf(eq_var)
                        self._model.Add(bridge_var != prev_value).OnlyEnforceIf(eq_var.Not())
                        prev_sol_negation_literals.append(eq_var.Not())

        # Also consider black cells from previous solution
        for p, black_cell_var in self._black_cells_z3.items():
            if p in self._previous_solution:
                is_black_in_prev = self._previous_solution.get_value(p) == '■' # Assuming '■' for black cells

                eq_black_var = self._model.NewBoolVar(f"prev_black_{p}_{is_black_in_prev}")
                # black_cell_var is true if cell is black.
                # if it was black (is_black_in_prev is True), then black_cell_var == 1
                # if it was not black (is_black_in_prev is False), then black_cell_var == 0
                self._model.Add(black_cell_var == (1 if is_black_in_prev else 0)).OnlyEnforceIf(eq_black_var)
                self._model.Add(black_cell_var != (1 if is_black_in_prev else 0)).OnlyEnforceIf(eq_black_var.Not())
                prev_sol_negation_literals.append(eq_black_var.Not())


        if prev_sol_negation_literals:
            self._model.AddBoolOr(prev_sol_negation_literals)
        else:
            # This case means previous solution had no bridges and no black cells or was empty.
            # Adding no constraint might lead to finding the same (empty) solution.
            # Or, if _previous_solution was from a non-Yajilin context, this is problematic.
            # For now, assume if list is empty, we can't make progress this way.
            return IslandGrid.empty(), 0 # Or perhaps raise error

        # self._init_island_grid() # Not needed, model is modified.
        return self.get_solution() # Re-solve with the new constraint

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_walls_around_digit_constraints()
        self._add_black_cell_constraints()
        self._add_no_adjacent_black_constraint()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()

    def _add_initial_constraints(self):
        # The constraint Or(direction_bridges == 0, direction_bridges == 1) is implicit with NewIntVar(0, 1, ...)
        # self._model.Add(constraints) # Removed
        constraints_border_up = [self._island_bridges_z3[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number) if Position(0, c) in self._island_bridges_z3]
        constraints_border_down = [self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in range(self._island_grid.columns_number) if Position(self._island_grid.rows_number - 1, c) in self._island_bridges_z3]
        constraints_border_right = [self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in range(self._island_grid.rows_number) if Position(r, self._island_grid.columns_number - 1) in self._island_bridges_z3]
        constraints_border_left = [self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number) if Position(r, 0) in self._island_bridges_z3]
        for constraint_list in [constraints_border_down, constraints_border_up, constraints_border_right, constraints_border_left]:
            for constraint in constraint_list: # Add constraints individually
                self._model.Add(constraint)


    def _add_opposite_bridges_constraints(self):
        for island in [island for island in self._island_grid.islands.values() if island.position in self._island_bridges_z3]:
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                position_bridges = island.direction_position_bridges.get(direction)
                if position_bridges is not None:
                    other_position, _ = position_bridges
                    if other_position not in self._island_bridges_z3:
                        continue
                    self._model.Add(self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[other_position][direction.opposite])
                else:
                    self._model.Add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_black_cell_constraints(self):
        for position, blacks_count_direction in [(position, value) for position, value in self.input_grid if value != '']:
            blacks_count = int(blacks_count_direction[0])
            direction = YajilinSolver.direction_map[blacks_count_direction[1]]
            concerned_positions = self.input_grid.all_positions_at(position, direction)
            self._model.Add(sum([self._black_cells_z3[concerned_position] for concerned_position in concerned_positions if concerned_position in self._island_bridges_z3.keys()]) == blacks_count)

    def _add_bridges_sum_constraints(self):
        for position in [position for position, value in self.input_grid if value == '']:
            bridges_sum_expr = sum([self._island_bridges_z3[position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]])
            black_cell = self._black_cells_z3[position]
            # Implies(black_cell, bridges_count_0)
            self._model.Add(bridges_sum_expr == 0).OnlyEnforceIf(black_cell)
            # Implies(path_cell, bridges_count_2)
            self._model.Add(bridges_sum_expr == 2).OnlyEnforceIf(black_cell.Not())

    def _add_no_adjacent_black_constraint(self):
        for position in [position for position, value in self.input_grid if value == '']:
            for neighbor_position in self.input_grid.neighbors_positions(position):
                if neighbor_position not in self._island_bridges_z3:
                    continue
                # Implies(self._black_cells_z3[position], Not(self._black_cells_z3[neighbor_position]))
                self._model.AddImplication(self._black_cells_z3[position], self._black_cells_z3[neighbor_position].Not())

    def _add_walls_around_digit_constraints(self):
        for position in [position for position, value in self.input_grid if value != '']:
            neighbors = self.input_grid.neighbors_positions(position)
            for neighbor in [neighbor for neighbor in neighbors if neighbor in self._island_bridges_z3]:
                direction = neighbor.direction_to(position)
                self._model.Add(self._island_bridges_z3[neighbor][direction] == 0)
