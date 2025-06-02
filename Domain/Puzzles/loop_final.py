from z3 import *


def solve_loop_puzzle(grid):
    n = len(grid)
    s = Solver()
    N = n * n  # Nombre maximal d'étapes pour la propagation

    # Création des variables booléennes pour les directions
    d = [[Bool(f'd_{i}_{j}') for j in range(n)] for i in range(n)]
    u = [[Bool(f'u_{i}_{j}') for j in range(n)] for i in range(n)]
    l = [[Bool(f'l_{i}_{j}') for j in range(n)] for i in range(n)]
    r = [[Bool(f'r_{i}_{j}') for j in range(n)] for i in range(n)]
    non_empty = [[Bool(f'ne_{i}_{j}') for j in range(n)] for i in range(n)]

    # Constraints for non_empty
    for i in range(n):
        for j in range(n):
            s.add(non_empty[i][j] == Or(u[i][j], d[i][j], l[i][j], r[i][j]))

    # Constraints from the input grid
    for i in range(n):
        for j in range(n):
            cell_type = grid[i][j]
            if cell_type == '__':
                s.add(non_empty[i][j] == False)
                # This implies u,d,l,r are all False due to the non_empty definition
            else:
                s.add(u[i][j] == ('u' in cell_type))
                s.add(d[i][j] == ('d' in cell_type))
                s.add(l[i][j] == ('l' in cell_type))
                s.add(r[i][j] == ('r' in cell_type))

    # Connectivity constraints
    for i in range(n):
        for j in range(n):
            # Up implies down from cell above
            if i > 0:
                s.add(Implies(u[i][j], d[i-1][j]))
            else: # Boundary condition: cannot go up from top row
                s.add(Not(u[i][j]))

            # Down implies up from cell below
            if i < n - 1:
                s.add(Implies(d[i][j], u[i+1][j]))
            else: # Boundary condition: cannot go down from bottom row
                s.add(Not(d[i][j]))

            # Left implies right from cell to the left
            if j > 0:
                s.add(Implies(l[i][j], r[i][j-1]))
            else: # Boundary condition: cannot go left from leftmost column
                s.add(Not(l[i][j]))

            # Right implies left from cell to the right
            if j < n - 1:
                s.add(Implies(r[i][j], l[i][j+1]))
            else: # Boundary condition: cannot go right from rightmost column
                s.add(Not(r[i][j]))

    # Two neighbors rule
    for i in range(n):
        for j in range(n):
            s.add(Implies(non_empty[i][j], Sum([
                If(u[i][j], 1, 0),
                If(d[i][j], 1, 0),
                If(l[i][j], 1, 0),
                If(r[i][j], 1, 0)
            ]) == 2))

    # Single loop constraint:
    # 1. Define root cell (first non_empty cell in row-major order)
    root = [[Bool(f'root_{i}_{j}') for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            preceding_cells_empty = []
            for prev_r in range(n):
                for prev_c in range(n):
                    if (prev_r < i) or (prev_r == i and prev_c < j):
                        preceding_cells_empty.append(Not(non_empty[prev_r][prev_c]))
            s.add(root[i][j] == And(non_empty[i][j], And(preceding_cells_empty)))

    # There must be exactly one root cell
    s.add(Sum([If(root[i][j], 1, 0) for i in range(n) for j in range(n)]) == 1)

    # 2. Visited cells propagation
    # visited[k][i][j] is true if cell (i,j) is visited within k steps from the root
    # N is max_steps, so k ranges from 0 to N. Visited array size is (N+1) x n x n.
    visited = [[[Bool(f'visited_{k}_{i}_{j}') for j in range(n)] for i in range(n)] for k in range(N + 1)]

    # Initial state (k=0): visited cells are the root cells
    for i in range(n):
        for j in range(n):
            s.add(visited[0][i][j] == root[i][j])

    # Propagation step (k to k+1)
    for k in range(N):  # k from 0 to N-1
        for i in range(n):
            for j in range(n):
                adj_visited_at_k = []
                # Check up: if u[i][j] is true, then (i-1,j) is a valid neighbor
                if i > 0: # Ensure we don't go out of bounds for visited array
                    adj_visited_at_k.append(And(u[i][j], visited[k][i-1][j]))
                else: # Cannot come from above if on first row
                    adj_visited_at_k.append(BoolVal(False))

                # Check down: if d[i][j] is true, then (i+1,j) is a valid neighbor
                if i < n - 1: # Ensure we don't go out of bounds for visited array
                    adj_visited_at_k.append(And(d[i][j], visited[k][i+1][j]))
                else: # Cannot come from below if on last row
                    adj_visited_at_k.append(BoolVal(False))
                
                # Check left: if l[i][j] is true, then (i,j-1) is a valid neighbor
                if j > 0: # Ensure we don't go out of bounds for visited array
                    adj_visited_at_k.append(And(l[i][j], visited[k][i][j-1]))
                else: # Cannot come from left if on first col
                    adj_visited_at_k.append(BoolVal(False))

                # Check right: if r[i][j] is true, then (i,j+1) is a valid neighbor
                if j < n - 1: # Ensure we don't go out of bounds for visited array
                    adj_visited_at_k.append(And(r[i][j], visited[k][i][j+1]))
                else: # Cannot come from right if on last col
                    adj_visited_at_k.append(BoolVal(False))
                
                s.add(visited[k+1][i][j] == Or(visited[k][i][j], And(non_empty[i][j], Or(adj_visited_at_k))))

    # Final state: all non_empty cells must be visited after N steps
    for i in range(n):
        for j in range(n):
            s.add(Implies(non_empty[i][j], visited[N][i][j]))

    # Check satisfiability and return result
    if s.check() == sat:
        # m = s.model()
        # print("Model:")
        # for i in range(n):
        #     for j in range(n):
        #         cell_str = ""
        #         if is_true(m.eval(u[i][j])): cell_str += "u"
        #         if is_true(m.eval(d[i][j])): cell_str += "d"
        #         if is_true(m.eval(l[i][j])): cell_str += "l"
        #         if is_true(m.eval(r[i][j])): cell_str += "r"
        #         if not cell_str: cell_str = "__"
        #         print(f"{cell_str:2}", end=" ")
        #     print()
        return True
    else:
        # print("No solution found.")
        # print(s.unsat_core()) # Optional: print unsat core for debugging
        return False


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple valide
    valid_grid = [
        ['dr', 'lr', 'dl', '__'],
        ['du', '__', 'ur', 'dl'],
        ['ur', 'lr', 'dl', 'ud'],
        ['__', '__', 'lr', 'ul']
    ]

    # Exemple invalide (contient 2 boucles)
    invalid_grid = [
        ['dr', 'lr', '__', '__'],
        ['du', 'ud', 'dr', 'lr'],
        ['ur', 'ul', 'du', 'ud'],
        ['__', '__', 'ur', 'ul']
    ]

    print("--- Running Tests ---")

    result_valid = solve_loop_puzzle(valid_grid)
    print(f"Raw result for valid_grid: {result_valid}")
    if result_valid == True:
        print("Valid grid test: PASS")
    else:
        print("Valid grid test: FAIL")
    print("-" * 20)

    result_invalid = solve_loop_puzzle(invalid_grid)
    print(f"Raw result for invalid_grid: {result_invalid}")
    if result_invalid == False:
        print("Invalid grid test: PASS")
    else:
        print("Invalid grid test: FAIL")
    print("--- Tests Finished ---")
