from z3 import *


def matrix_loop(n):
    g = [[Bool(f'g_{i}_{j}') for j in range(n)] for i in range(n)]
    solver = Solver()

    for i in range(n):
        for j in range(n):
            neighbors = []
            if i > 0: neighbors.append(g[i - 1][j])
            if j > 0: neighbors.append(g[i][j - 1])
            if i < n - 1: neighbors.append(g[i + 1][j])
            if j < n - 1: neighbors.append(g[i][j + 1])

            nb_neighbors = Sum([If(cond, 1, 0) for cond in neighbors])
            solver.add(If(g[i][j], nb_neighbors == 2, True))

    N = n * n
    root = [[Bool(f'root_{i}_{j}') for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            before = []
            for i2 in range(n):
                for j2 in range(n):
                    if (i2 < i) or (i2 == i and j2 < j):
                        before.append(Not(g[i2][j2]))
            solver.add(root[i][j] == And(g[i][j], And(before) if before else True))

    visited = [[[Bool(f'visited_{k}_{i}_{j}') for j in range(n)] for i in range(n)] for k in range(N + 1)]

    for i in range(n):
        for j in range(n):
            solver.add(visited[0][i][j] == root[i][j])

    for k in range(N):
        for i in range(n):
            for j in range(n):
                adj_visited = False
                if i > 0:
                    adj_visited = Or(adj_visited, And(g[i - 1][j], visited[k][i - 1][j]))
                if j > 0:
                    adj_visited = Or(adj_visited, And(g[i][j - 1], visited[k][i][j - 1]))
                if i < n - 1:
                    adj_visited = Or(adj_visited, And(g[i + 1][j], visited[k][i + 1][j]))
                if j < n - 1:
                    adj_visited = Or(adj_visited, And(g[i][j + 1], visited[k][i][j + 1]))

                solver.add(visited[k + 1][i][j] == Or(visited[k][i][j], And(g[i][j], adj_visited)))

    for i in range(n):
        for j in range(n):
            solver.add(Implies(g[i][j], visited[N][i][j]))

    return solver, g


if __name__ == "__main__":
    n = 9
    solver, matrix_z3 = matrix_loop(n)

    partial_matrix = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
    ]
    for i in range(n):
        for j in range(n):
            if partial_matrix[i][j]:
                solver.add(matrix_z3[i][j])

    if solver.check() == sat:
        model = solver.model()

        print("\nStatistiques du solveur Z3 :")
        stats = solver.statistics()
        print(stats)

        for i in range(n):
            for j in range(n):
                print('x' if is_true(model.eval(matrix_z3[i][j])) else '_', end=" ")
            print()
        print("Matrice valide : SAT")
    else:
        print("Matrice valide : UNSAT")
