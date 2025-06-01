
from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class MasyuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self.init_island_grid()
        self._model = cp_model.CpModel()
        self._island_bridges_vars: dict[Position, dict[Direction, cp_model.IntVar]] = {}
        self._previous_solution: IslandGrid | None = None
        self._constraints_added = False

    def init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_vars = {
            island.position: {direction: self._model.NewBoolVar(f"bridge_{island.position}_{direction}") for direction in Direction.orthogonals()} for island in self._island_grid.islands.values()
        }
        self._add_constraints()
        self._constraints_added = True

    def get_solution(self) -> IslandGrid:
        if not self._constraints_added:
            self._init_solver()

        solver = cp_model.CpSolver()
        solution, _ = self._ensure_all_islands_connected(solver)
        return solution

    def _ensure_all_islands_connected(self, solver: cp_model.CpSolver) -> (Grid, int):
        proposition_count = 0
        status = solver.Solve(self._model)
        while status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_vars.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_vars:
                        continue
                    bridges_number = solver.Value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()
            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            for positions in connected_positions:
                cell_constraints_vars = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        var = self._island_bridges_vars[position][direction]
                        if value == 1:
                            cell_constraints_vars.append(var)
                        else:
                            cell_constraints_vars.append(var.Not())
                self._model.AddBoolOr([v.Not() for v in cell_constraints_vars])
            self.init_island_grid()
            status = solver.Solve(self._model)

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_literals = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                var = self._island_bridges_vars[island.position][direction]
                if value == 1:
                    previous_solution_literals.append(var)
                else:
                    previous_solution_literals.append(var.Not())
        self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

        self.init_island_grid()
        # Create a new solver instance for the new solution attempt
        solver = cp_model.CpSolver()
        solution, _ = self._ensure_all_islands_connected(solver)
        return solution

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_constraints()

    def _add_initial_constraints(self):
        # This method becomes obsolete with NewBoolVar, as BoolVar can only be 0 or 1.
        # If NewIntVar(0, 1, ...) was used, it would also be intrinsic.
        pass

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._model.Add(self._island_bridges_vars[island.position][direction] == self._island_bridges_vars[island.direction_position_bridges[direction][0]][
                        direction.opposite])
                else:
                    # For BoolVar, constraint is var == False or Add(~var)
                    self._model.Add(self._island_bridges_vars[island.position][direction] == False)


    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            bridges_around_island = [self._island_bridges_vars[island.position][direction] for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]]
            s = sum(bridges_around_island)
            # The sum of bridges must be 0 or 2. This means s != 1 and s != 3 and s != 4.
            # Since bridges are BoolVar (0 or 1), max sum is 4.
            # Constraint: s == 0 OR s == 2

            # Option 1: Add(s != 1). This also allows s = 3, 4 which should be prevented by other constraints (e.g. opposite bridges)
            # self._model.Add(s != 1)
            # self._model.Add(s != 3)
            # self._model.Add(s != 4)

            # Option 2: Reify sum constraints
            is_zero = self._model.NewBoolVar(f"sum_zero_{island.position}")
            is_two = self._model.NewBoolVar(f"sum_two_{island.position}")

            self._model.Add(s == 0).OnlyEnforceIf(is_zero)
            self._model.Add(s != 0).OnlyEnforceIf(is_zero.Not()) # Important for consistency

            self._model.Add(s == 2).OnlyEnforceIf(is_two)
            self._model.Add(s != 2).OnlyEnforceIf(is_two.Not()) # Important for consistency

            self._model.Add(is_zero + is_two == 1)


    def _add_dots_constraints(self):
        for position, value in self.input_grid:
            if value == 'w':
                # For white dots: (line passes straight) AND (turns before or after)
                # Straight horizontally OR straight vertically

                # Horizontal case: bridge left AND bridge right
                # AND (turn up/down at left OR turn up/down at right)
                h_straight_possible = position.left in self._island_bridges_vars and position.right in self._island_bridges_vars
                b_h_straight = self._model.NewBoolVar(f"wh_straight_{position}")
                if h_straight_possible:
                    self._model.Add(self._island_bridges_vars[position][Direction.left()] == True).OnlyEnforceIf(b_h_straight)
                    self._model.Add(self._island_bridges_vars[position][Direction.right()] == True).OnlyEnforceIf(b_h_straight)

                    # Turns at ends of horizontal segment
                    h_turns_at_ends_literals = []
                    if Direction.up() in self._island_bridges_vars[position.left]:
                        h_turns_at_ends_literals.append(self._island_bridges_vars[position.left][Direction.up()])
                    if Direction.down() in self._island_bridges_vars[position.left]:
                        h_turns_at_ends_literals.append(self._island_bridges_vars[position.left][Direction.down()])
                    if Direction.up() in self._island_bridges_vars[position.right]:
                        h_turns_at_ends_literals.append(self._island_bridges_vars[position.right][Direction.up()])
                    if Direction.down() in self._island_bridges_vars[position.right]:
                        h_turns_at_ends_literals.append(self._island_bridges_vars[position.right][Direction.down()])

                    if h_turns_at_ends_literals:
                        b_h_turn = self._model.NewBoolVar(f"wh_turn_{position}")
                        self._model.AddBoolOr(h_turns_at_ends_literals).OnlyEnforceIf(b_h_turn)
                        self._model.AddImplication(b_h_straight, b_h_turn) # if straight, must turn
                    else: # No possible turns, so horizontal straight is not allowed
                         self._model.AddImplication(b_h_straight, self._model.NewConstant(False))
                else:
                    self._model.Add(b_h_straight == False)

                # Vertical case: bridge up AND bridge down
                # AND (turn left/right at up OR turn left/right at down)
                v_straight_possible = position.up in self._island_bridges_vars and position.down in self._island_bridges_vars
                b_v_straight = self._model.NewBoolVar(f"wv_straight_{position}")
                if v_straight_possible:
                    self._model.Add(self._island_bridges_vars[position][Direction.up()] == True).OnlyEnforceIf(b_v_straight)
                    self._model.Add(self._island_bridges_vars[position][Direction.down()] == True).OnlyEnforceIf(b_v_straight)

                    v_turns_at_ends_literals = []
                    if Direction.left() in self._island_bridges_vars[position.up]:
                        v_turns_at_ends_literals.append(self._island_bridges_vars[position.up][Direction.left()])
                    if Direction.right() in self._island_bridges_vars[position.up]:
                        v_turns_at_ends_literals.append(self._island_bridges_vars[position.up][Direction.right()])
                    if Direction.left() in self._island_bridges_vars[position.down]:
                        v_turns_at_ends_literals.append(self._island_bridges_vars[position.down][Direction.left()])
                    if Direction.right() in self._island_bridges_vars[position.down]:
                        v_turns_at_ends_literals.append(self._island_bridges_vars[position.down][Direction.right()])

                    if v_turns_at_ends_literals:
                        b_v_turn = self._model.NewBoolVar(f"wv_turn_{position}")
                        self._model.AddBoolOr(v_turns_at_ends_literals).OnlyEnforceIf(b_v_turn)
                        self._model.AddImplication(b_v_straight, b_v_turn) # if straight, must turn
                    else: # No possible turns, so vertical straight is not allowed
                        self._model.AddImplication(b_v_straight, self._model.NewConstant(False))
                else:
                    self._model.Add(b_v_straight == False)

                # White dot means: (horizontal straight AND horizontal turns) OR (vertical straight AND vertical turns)
                # The implication b_h_straight => b_h_turn is already added.
                # We need to ensure that if b_h_straight is true, its conditions are met.
                # And same for b_v_straight.
                # Then, one of b_h_straight or b_v_straight must be true.
                self._model.AddBoolOr([b_h_straight, b_v_straight])


            if value == 'b':
                # For black dots: (must turn at this dot) AND (must go straight over adjacent cells)
                # Four possible turns: RD, LD, RU, LU

                possible_turns_literals = []

                # Right-Down turn at `position`
                # Conditions: bridge right from `position`, bridge right from `position.right`
                # AND bridge down from `position`, bridge down from `position.down`
                if (position.right in self._island_bridges_vars and position.right.right in self._island_bridges_vars and
                        position.down in self._island_bridges_vars and position.down.down in self._island_bridges_vars):
                    b_rd_turn = self._model.NewBoolVar(f"b_rd_turn_{position}")
                    self._model.Add(self._island_bridges_vars[position][Direction.right()] == True).OnlyEnforceIf(b_rd_turn)
                    self._model.Add(self._island_bridges_vars[position.right][Direction.right()] == True).OnlyEnforceIf(b_rd_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.down()] == True).OnlyEnforceIf(b_rd_turn)
                    self._model.Add(self._island_bridges_vars[position.down][Direction.down()] == True).OnlyEnforceIf(b_rd_turn)
                    # Ensure no straight path through the turn
                    self._model.Add(self._island_bridges_vars[position][Direction.left()] == False).OnlyEnforceIf(b_rd_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.up()] == False).OnlyEnforceIf(b_rd_turn)
                    possible_turns_literals.append(b_rd_turn)

                # Left-Down turn at `position`
                if (position.left in self._island_bridges_vars and position.left.left in self._island_bridges_vars and
                        position.down in self._island_bridges_vars and position.down.down in self._island_bridges_vars):
                    b_ld_turn = self._model.NewBoolVar(f"b_ld_turn_{position}")
                    self._model.Add(self._island_bridges_vars[position][Direction.left()] == True).OnlyEnforceIf(b_ld_turn)
                    self._model.Add(self._island_bridges_vars[position.left][Direction.left()] == True).OnlyEnforceIf(b_ld_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.down()] == True).OnlyEnforceIf(b_ld_turn)
                    self._model.Add(self._island_bridges_vars[position.down][Direction.down()] == True).OnlyEnforceIf(b_ld_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.right()] == False).OnlyEnforceIf(b_ld_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.up()] == False).OnlyEnforceIf(b_ld_turn)
                    possible_turns_literals.append(b_ld_turn)

                # Right-Up turn at `position`
                if (position.right in self._island_bridges_vars and position.right.right in self._island_bridges_vars and
                        position.up in self._island_bridges_vars and position.up.up in self._island_bridges_vars):
                    b_ru_turn = self._model.NewBoolVar(f"b_ru_turn_{position}")
                    self._model.Add(self._island_bridges_vars[position][Direction.right()] == True).OnlyEnforceIf(b_ru_turn)
                    self._model.Add(self._island_bridges_vars[position.right][Direction.right()] == True).OnlyEnforceIf(b_ru_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.up()] == True).OnlyEnforceIf(b_ru_turn)
                    self._model.Add(self._island_bridges_vars[position.up][Direction.up()] == True).OnlyEnforceIf(b_ru_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.left()] == False).OnlyEnforceIf(b_ru_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.down()] == False).OnlyEnforceIf(b_ru_turn)
                    possible_turns_literals.append(b_ru_turn)

                # Left-Up turn at `position`
                if (position.left in self._island_bridges_vars and position.left.left in self._island_bridges_vars and
                        position.up in self._island_bridges_vars and position.up.up in self._island_bridges_vars):
                    b_lu_turn = self._model.NewBoolVar(f"b_lu_turn_{position}")
                    self._model.Add(self._island_bridges_vars[position][Direction.left()] == True).OnlyEnforceIf(b_lu_turn)
                    self._model.Add(self._island_bridges_vars[position.left][Direction.left()] == True).OnlyEnforceIf(b_lu_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.up()] == True).OnlyEnforceIf(b_lu_turn)
                    self._model.Add(self._island_bridges_vars[position.up][Direction.up()] == True).OnlyEnforceIf(b_lu_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.right()] == False).OnlyEnforceIf(b_lu_turn)
                    self._model.Add(self._island_bridges_vars[position][Direction.down()] == False).OnlyEnforceIf(b_lu_turn)
                    possible_turns_literals.append(b_lu_turn)

                if possible_turns_literals:
                    self._model.AddBoolOr(possible_turns_literals)
                else:
                    # This case should ideally not happen in a valid Masyu puzzle with a black dot.
                    # If it does, it means the black dot has no valid turn, making the puzzle unsolvable.
                    # Add a constraint that is always false to indicate unsolvability.
                    self._model.Add(self._model.NewConstant(False))
