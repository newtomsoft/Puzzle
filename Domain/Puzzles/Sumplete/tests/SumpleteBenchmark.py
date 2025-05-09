﻿# import timeit
# 
# from Puzzles.Sumplete.SumpleteSolver import SumpleteSolver
# from Puzzles.GameSolver import GameSolver
# from Ports.Ports import Ports
# from Utils.Board import Board
# 
# 
# class SumpleteBenchmark:
#     def __init__(self):
#         self.grids3x3 = [
#             [[3, 1, 6, 6], [6, 1, 2, 3], [1, 8, 2, 11], [1, 9, 10, 0]],
#             [[8, 6, 7, 13], [1, 3, 7, 8], [9, 8, 5, 5], [1, 6, 19, 0]],
#             [[5, 3, 1, 1], [1, 4, 7, 12], [8, 3, 8, 8], [1, 4, 16, 0]],
#             [[3, 1, 9, 4], [7, 2, 9, 2], [5, 1, 7, 13], [8, 4, 7, 0]]
#         ]
# 
#         self.grids4x4 = [
#             [[1, 6, 4, 6, 7], [7, 2, 8, 5, 8], [1, 1, 6, 1, 8], [6, 5, 6, 8, 14], [7, 7, 14, 9, 0]],
#             [[6, 6, 4, 5, 15], [9, 1, 7, 8, 17], [1, 6, 7, 8, 14], [3, 1, 6, 3, 1], [16, 8, 18, 5, 0]],
#             [[6, 7, 6, 8, 6], [2, 4, 1, 5, 12], [2, 4, 2, 8, 12], [1, 9, 4, 6, 20], [9, 17, 5, 19, 0]],
#             [[4, 9, 1, 6, 20], [4, 2, 5, 9, 11], [9, 8, 7, 1, 17], [2, 4, 6, 3, 7], [17, 23, 6, 9, 0]],
#         ]
# 
#         self.grids5x5 = [
#             [[4, 1, 2, 8, 4, 19], [2, 5, 7, 9, 4, 14], [1, 7, 9, 7, 4, 17], [4, 7, 2, 4, 4, 6], [2, 1, 8, 8, 4, 7], [9, 7, 20, 15, 12, 0]],
#             [[5, 3, 8, 2, 6, 7], [4, 4, 1, 6, 3, 18], [1, 2, 1, 2, 6, 4], [1, 4, 1, 4, 1, 4], [3, 5, 2, 6, 1, 3], [10, 6, 4, 12, 4, 0]],
#             [[2, 1, 9, 2, 3, 5], [4, 5, 4, 4, 2, 11], [7, 2, 2, 9, 4, 11], [7, 6, 8, 6, 6, 15], [1, 2, 9, 5, 1, 1], [12, 5, 10, 11, 5, 0]],
#             [[9, 2, 2, 3, 9, 16], [5, 5, 1, 8, 6, 5], [4, 7, 1, 3, 5, 19], [1, 2, 1, 6, 1, 1], [3, 5, 5, 9, 9, 17], [16, 19, 2, 6, 15, 0]],
#         ]
# 
#         self.grids6x6 = [
#             [[5, 4, 6, 7, 7, 8, 22], [5, 5, 8, 6, 9, 1, 28], [8, 7, 9, 9, 6, 3, 22], [7, 2, 3, 4, 3, 5, 12], [7, 8, 6, 1, 7, 2, 7], [8, 9, 7, 7, 1, 6, 9], [20, 9, 26, 14, 23, 8, 0]],
#             [[2, 8, 4, 6, 7, 4, 11], [9, 5, 3, 7, 5, 8, 29], [4, 6, 5, 6, 1, 6, 6], [9, 9, 7, 8, 6, 9, 17], [3, 2, 2, 6, 5, 9, 16], [1, 8, 8, 6, 5, 4, 12], [22, 5, 9, 27, 22, 6, 0]],
#             [[1, 4, 9, 9, 4, 4, 18], [2, 9, 3, 9, 6, 4, 11], [8, 7, 6, 8, 5, 4, 33], [9, 5, 6, 9, 8, 5, 29], [9, 5, 6, 1, 6, 5, 11], [8, 2, 4, 3, 3, 5, 13], [28, 19, 27, 26, 7, 8, 0]],
#             [[1, 2, 7, 5, 7, 4, 19], [7, 9, 7, 7, 3, 6, 23], [1, 2, 5, 4, 9, 5, 9], [2, 6, 1, 1, 8, 1, 16], [2, 9, 4, 7, 2, 1, 10], [8, 6, 3, 3, 9, 7, 12], [3, 8, 18, 19, 29, 12, 0]],
#         ]
# 
#         self.grids7x7 = [
#             [[1, 8, 7, 2, 3, 5, 6, 14], [4, 6, 1, 9, 1, 1, 3, 24], [4, 2, 2, 8, 6, 5, 1, 19], [4, 4, 4, 4, 4, 6, 2, 14], [6, 5, 6, 3, 2, 4, 2, 2], [2, 7, 6, 1, 1, 4, 6, 26], [7, 9, 2, 2, 1, 1, 5, 8], [22, 23, 7, 24, 10, 10, 11, 0]],
#             [[9, 8, 1, 9, 3, 2, 3, 9], [5, 7, 2, 9, 1, 6, 2, 20], [5, 5, 2, 6, 8, 3, 6, 8], [8, 4, 3, 4, 3, 7, 7, 14], [3, 7, 9, 1, 5, 2, 6, 16], [8, 6, 4, 4, 8, 9, 9, 30], [7, 6, 7, 5, 1, 9, 4, 13], [8, 7, 17, 29, 3, 18, 28, 0]],
#             [[1, 1, 4, 1, 5, 7, 7, 23], [7, 2, 7, 9, 3, 9, 5, 15], [4, 3, 7, 1, 8, 1, 1, 5], [5, 9, 4, 4, 4, 9, 7, 27], [4, 2, 4, 9, 4, 8, 2, 27], [7, 3, 5, 8, 3, 9, 2, 18], [1, 7, 2, 1, 3, 3, 5, 6], [23, 15, 15, 15, 11, 27, 15, 0]],
#             [[2, 2, 5, 6, 4, 8, 2, 15], [8, 9, 6, 5, 4, 4, 3, 24], [1, 1, 4, 1, 5, 8, 1, 6], [3, 3, 7, 6, 4, 6, 4, 10], [2, 9, 5, 5, 7, 5, 8, 26], [5, 1, 6, 2, 6, 5, 7, 25], [2, 5, 5, 2, 7, 1, 6, 27], [18, 14, 23, 14, 23, 22, 19, 0]],
#         ]
# 
#         self.grids8x8 = [
#             [[6, 5, 9, 3, 3, 4, 2, 3, 17], [6, 9, 3, 1, 8, 8, 8, 7, 14], [9, 1, 8, 6, 9, 4, 1, 2, 12], [1, 8, 7, 7, 9, 7, 1, 1, 25], [3, 7, 3, 7, 8, 2, 7, 9, 23], [3, 9, 7, 4, 2, 8, 7, 9, 19], [9, 4, 6, 5, 6, 8, 1, 6, 23], [9, 4, 5, 7, 8, 8, 9, 5, 20],
#              [9, 33, 30, 19, 28, 14, 15, 5, 0]],
#             [[8, 7, 8, 1, 8, 4, 8, 8, 23], [5, 1, 7, 8, 5, 9, 7, 3, 21], [5, 5, 2, 5, 5, 4, 6, 6, 10], [3, 9, 8, 4, 4, 4, 7, 6, 28], [1, 1, 7, 6, 7, 6, 6, 9, 23], [6, 4, 2, 8, 9, 1, 8, 6, 30], [1, 7, 9, 7, 7, 1, 2, 6, 15], [9, 4, 2, 4, 6, 7, 7, 1, 18],
#              [23, 29, 10, 16, 24, 4, 23, 39, 0]],
#             [[6, 9, 2, 9, 2, 4, 6, 6, 34], [5, 5, 5, 4, 1, 4, 4, 6, 23], [8, 4, 2, 4, 7, 3, 6, 6, 14], [2, 3, 3, 5, 3, 5, 6, 3, 19], [1, 5, 9, 3, 3, 7, 3, 2, 7], [4, 2, 5, 8, 9, 6, 5, 5, 26], [4, 4, 1, 3, 9, 2, 5, 6, 32], [8, 9, 9, 2, 1, 3, 4, 8, 30],
#              [33, 18, 22, 23, 24, 15, 19, 31, 0]],
#             [[4, 3, 5, 3, 4, 2, 8, 8, 10], [3, 7, 3, 1, 6, 8, 8, 2, 23], [9, 4, 1, 3, 4, 3, 9, 2, 5], [1, 4, 1, 2, 9, 9, 1, 2, 17], [8, 8, 7, 4, 7, 3, 5, 2, 22], [6, 5, 5, 2, 6, 3, 5, 2, 9], [6, 9, 8, 1, 8, 9, 2, 5, 19], [5, 4, 2, 6, 4, 3, 9, 8, 17],
#              [7, 28, 17, 14, 14, 25, 8, 9, 0]],
#         ]
# 
#         self.grids9x9 = [
#             [[2, 7, 7, 3, 9, 8, 3, 1, 1, 24], [9, 7, 6, 5, 3, 3, 1, 9, 8, 29], [4, 3, 1, 2, 6, 3, 1, 5, 8, 23], [8, 1, 3, 7, 8, 7, 6, 1, 8, 14], [9, 5, 5, 8, 5, 2, 8, 9, 7, 14], [7, 8, 2, 3, 1, 3, 9, 8, 5, 6], [7, 3, 8, 2, 8, 5, 6, 5, 9, 15],
#              [3, 3, 7, 9, 6, 1, 2, 8, 3, 19], [4, 4, 8, 3, 3, 8, 8, 2, 5, 22], [12, 16, 37, 7, 35, 15, 10, 21, 13, 0]],
#             [[3, 8, 5, 3, 7, 8, 7, 5, 8, 30], [6, 8, 8, 5, 1, 6, 6, 8, 2, 25], [3, 1, 5, 7, 5, 2, 5, 9, 4, 13], [5, 4, 6, 6, 1, 5, 4, 1, 7, 24], [7, 3, 1, 3, 7, 4, 5, 3, 2, 7], [4, 6, 4, 7, 6, 6, 8, 4, 9, 34], [6, 8, 1, 8, 3, 2, 6, 9, 1, 24],
#              [4, 2, 5, 5, 2, 5, 2, 5, 3, 16], [2, 1, 8, 8, 4, 9, 4, 5, 4, 39], [22, 31, 27, 14, 16, 28, 29, 39, 6, 0]],
#             [[2, 2, 3, 6, 4, 2, 2, 3, 4, 9], [2, 8, 9, 3, 6, 9, 1, 3, 3, 9], [9, 3, 1, 5, 3, 3, 1, 3, 4, 16], [9, 9, 8, 3, 7, 2, 4, 8, 2, 30], [6, 1, 2, 3, 1, 6, 7, 7, 3, 16], [2, 5, 7, 2, 4, 1, 2, 5, 1, 4], [3, 6, 3, 7, 6, 2, 3, 1, 3, 14],
#              [3, 9, 4, 9, 7, 2, 4, 7, 4, 43], [5, 1, 2, 6, 7, 7, 3, 6, 8, 18], [20, 21, 14, 19, 21, 15, 17, 10, 22, 0]],
#             [[3, 8, 1, 2, 2, 1, 3, 8, 4, 14], [1, 1, 5, 8, 9, 9, 4, 8, 4, 30], [4, 4, 8, 3, 3, 6, 4, 1, 3, 21], [1, 8, 9, 9, 8, 3, 6, 1, 5, 18], [7, 4, 1, 3, 7, 1, 2, 3, 6, 21], [5, 5, 3, 9, 7, 9, 4, 6, 1, 24], [8, 3, 2, 8, 9, 9, 7, 3, 9, 11],
#              [2, 3, 3, 4, 6, 8, 7, 7, 3, 16], [4, 1, 5, 6, 8, 8, 4, 2, 9, 34], [20, 11, 11, 19, 16, 36, 18, 33, 25, 0]],
#         ]
# 
#         self.grids_by_size = {
#             3: self.grids3x3,
#             4: self.grids4x4,
#             5: self.grids5x5,
#             6: self.grids6x6,
#             7: self.grids7x7,
#             8: self.grids8x8,
#             9: self.grids9x9,
#         }
# 
#     def loop_game_xxx(self, x: int | str):
#         grids = self.grids_by_size[x]
#         for grid in grids:
#             game_solver = SumpleteSolver(Board(grid))
#             solution = game_solver.get_solution()
#             assert solution is not None
# 
#     def benchmark(self, x, loops_count):
#         print(f"Starting benchmark for {x}x{x} grids")
#         grids = self.grids_by_size[x]
#         print(f"  runs {loops_count} loops of {len(grids)} boards")
#         execution_time = timeit.timeit(lambda: self.loop_game_xxx(x), number=loops_count)
#         print(f"  Average execution time : {execution_time / loops_count / len(grids):.3f} seconds")
#         print("Benchmark finished")
#         print("----------------------\n")
#         return execution_time
# 
#     def run_benchmarks(self):
#         size_loops_time = dict()
#         size_loops_time[3] = [10, self.benchmark(3, 10)]
#         size_loops_time[4] = [10, self.benchmark(4, 10)]
#         size_loops_time[5] = [10, self.benchmark(5, 10)]
#         size_loops_time[6] = [10, self.benchmark(6, 10)]
#         size_loops_time[7] = [10, self.benchmark(7, 10)]
#         size_loops_time[8] = [10, self.benchmark(8, 10)]
#         size_loops_time[9] = [10, self.benchmark(9, 10)]
# 
#         print()
#         print("----------------------")
#         total_executions_time = sum(loop_time[1] for loop_time in size_loops_time.values())
#         print(f"Total execution time: {total_executions_time:.3f} seconds")
#         print("Benchmark finished")
# 
# 
# if __name__ == '__main__':
#     benchmark = SumpleteBenchmark()
#     benchmark.run_benchmarks()
