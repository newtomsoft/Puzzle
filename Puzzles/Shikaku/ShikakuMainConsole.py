﻿# import time
# 
# from GridProviders.PuzzleShikakuGridProvider import PuzzleShikakuGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Puzzles.Shikaku.ShikakuSolver import ShikakuSolver
# from Utils.Grid import Grid
# 
# 
# class ShikakuMainConsole:
#     @staticmethod
#     def main():
#         grid = ShikakuMainConsole.get_grid()
#         ShikakuMainConsole.run(grid, self.solver_engine)
# 
# 
#     @staticmethod
#     def get_grid():
#         print("Shikaku Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             "https://www.puzzle-shikaku.com": PuzzleShikakuGridProvider,
#             "https://fr.puzzle-shikaku.com": PuzzleShikakuGridProvider,
#         }
# 
#         for pattern, provider_class in url_patterns.items():
#             if pattern in console_input:
#                 provider = provider_class()
#                 return provider.get_grid(console_input)
# 
#         return StringGridProvider().get_grid(console_input)
# 
#     @staticmethod
#     def run(grid: Grid):
#         game_solver = ShikakuSolver(grid, self.solver_engine)
# 
#         start_time = time.time()
#         solution_grid = game_solver.get_solution()
#         execution_time = time.time() - start_time
#         if solution_grid != Grid.empty():
#             print(f"Solution found in {execution_time:.2f} seconds")
#             printable_grid = Grid([[' ' for _ in range(grid.columns_number)] for _ in range(grid.rows_number)])
#             police_color_grid = Grid([[16 for _ in range(grid.columns_number)] for _ in range(grid.rows_number)])
#             printable_grid_string = printable_grid.to_console_string(police_color_grid, solution_grid)
#             print(printable_grid_string)
#         else:
#             print(f"No solution found")
# 
# 
# if __name__ == '__main__':
#     ShikakuMainConsole.main()
