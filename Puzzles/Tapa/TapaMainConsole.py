﻿# from GridProviders.PuzzleTapaGridProvider import PuzzleTapaGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Puzzles.Tapa.TapaSolver import TapaSolver
# from Puzzles.GameSolver import GameSolver
# from Ports.Ports import Ports
# from Utils.Grid import Grid
# 
# 
# class TapaMainConsole:
#     @staticmethod
#     def main():
#         grid = TapaMainConsole.get_grid()
#         TapaMainConsole.run(grid, self.solver_engine)
# 
# 
#     @staticmethod
#     def get_grid():
#         print("Tapa Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             r"https://www.puzzle-tapa.com": PuzzleTapaGridProvider,
#             r"https://fr.puzzle-tapa.com": PuzzleTapaGridProvider
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
#     def run(grid, self.solver_engine)
# :
#         game_solver = TapaSolver(grid, self.solver_engine)
# 
#         solution_grid = game_solver.get_solution()
#         if not solution_grid:
#             print(f"No solution found")
#             return 1
# 
#         print(f"Solution found:")
#         console_grid = game_solver.get_console_grid(solution_grid)
#         print(console_grid)
# 
#         # TapaMainConsole.generate_html(solution_grid)
#         print("Play ? (y/n)")
#         play = input()
#         if play.lower() == "y":
#             # todo interface refactoring
#             player = PuzzleTapaGridProvider()
#             player.play(solution_grid, "https://fr.puzzle-tapa.com/?size=10")
# 
#     @staticmethod
#     def generate_html(solution_grid: Grid):
#         with open("solution.html", "w") as file:
#             file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 20px; height: 20px; text-align: center;}</style></head><body><table>")
#             for r in range(solution_grid.rows_number):
#                 file.write("<tr>")
#                 for c in range(solution_grid.columns_number):
#                     file.write(f"<td style='background-color: white; color: black;'>{solution_grid.value(r, c)}</td>")
#                 file.write("</tr>")
#             file.write("</table></body></html>")
# 
# 
# if __name__ == '__main__':
#     TapaMainConsole.main()
