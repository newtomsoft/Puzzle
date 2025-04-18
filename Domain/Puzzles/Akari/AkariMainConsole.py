﻿# import time
# 
# from AkariSolver import AkariSolver
# from GridProviders.PuzzleAkariGridProvider import PuzzleAkariGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Utils.Board import Board
# 
# 
# class AkariMainConsole:
#     @staticmethod
#     def main():
#         data_game = AkariMainConsole.get_grid()
#         AkariMainConsole.run(data_game)
# 
#     @staticmethod
#     def get_grid():
#         print("Akari Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             "https://www.puzzle-light-up.com": PuzzleAkariGridProvider,
#             "https://fr.puzzle-light-up.com": PuzzleAkariGridProvider,
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
#     def run(data_game):
#         game_solver = AkariSolver(data_game)
#         start_time = time.time()
#         solution_grid = game_solver.get_solution()
#         end_time = time.time()
#         execution_time = end_time - start_time
#         if not solution_grid.is_empty():
#             print(f"Solution found in {execution_time:.2f} seconds")
#             print(solution_grid.to_console_string())
#             # AkariMainConsole.generate_html(solution_grid)
#         else:
#             print(f"No solution found")
# 
#     @staticmethod
#     def generate_html(solution_grid: Board):
#         with open("solution.html", "w") as file:
#             file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 20px; height: 20px; text-align: center;}</style></head><body><table>")
#             for r in range(solution_grid.rows_number):
#                 file.write("<tr>")
#                 for c in range(solution_grid.columns_number):
#                     file.write(f"<td style='background-color: white; color: black;'>{AkariMainConsole.int_to_base26(solution_grid.value(r, c)())}</td>")
#                 file.write("</tr>")
#             file.write("</table></body></html>")
# 
# 
# if __name__ == '__main__':
#     AkariMainConsole.main()
