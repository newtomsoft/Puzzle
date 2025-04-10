﻿# import webbrowser
# 
# from GridProviders.KakuroConquestGridProvider import KakuroConquestGridProvider
# from GridProviders.KakuroOnlineGridProvider import KakuroOnlineGridProvider
# from GridProviders.PuzzleKakuroGridProvider import PuzzleKakuroGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Puzzles.Kakuro.KakuroSolver import KakuroSolver
# from Utils.Board import Board
# from Utils.Position import Position
# 
# 
# class KakuroMainConsole:
#     @staticmethod
#     def main():
#         grid = KakuroMainConsole.get_grid()
#         KakuroMainConsole.run(grid, self.solver_engine)
# 
# 
#     @staticmethod
#     def get_grid():
#         print("Kakuro Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             r"https://fr.puzzle-kakuro.com/": PuzzleKakuroGridProvider,
#             r"https://fr.kakuroconquest.com/": KakuroConquestGridProvider,
#             r"https://www.kakuro-online.com/": KakuroOnlineGridProvider,
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
#     def run(grid: Board):
#         try:
#             game_solver = KakuroSolver(grid, self.solver_engine)
# 
#         except ValueError as e:
#             print(f"Error: {e}")
#             return
#         solution_grid = game_solver.get_solution()
#         if solution_grid != Board.empty():
#             print(f"Solution found")
#             printable_grid = Board([[solution_grid.value(r, c) if solution_grid.value(r, c) != 0 else '•' for c in range(grid.columns_number)] for r in range(grid.rows_number)])
#             print(printable_grid.to_console_string())
#             for r in range(grid.rows_number):
#                 for c in range(grid.columns_number):
#                     if grid.value(r, c) == 0:
#                         grid.set_value(Position(r, c), solution_grid.value(r, c))
#             KakuroMainConsole.generate_html(grid, self.solver_engine)
# 
#         else:
#             print(f"No solution found")
# 
#     @staticmethod
#     def generate_html(grid: Board):
#         file_path = "solution.html"
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write("<html><head><style>")
#             file.write("table {border-collapse: collapse;} ")
#             file.write("td.number-cell, td.sum-cell {border: 1px solid black; width: 50px; height: 50px; text-align: center;} ")
#             file.write(".sum-cell {background-color: lightgray;  position: relative;}")
#             file.write("td.sum-cell span.row {position: absolute; top: 8%; left: 18%; width: 100%; text-align: center;}")
#             file.write("td.sum-cell span.column {position: absolute; bottom: 8%; right: 18%; width: 100%; text-align: center;}")
#             file.write(".number-cell {background-color: white;} ")
#             file.write('.line {position: absolute;top: 0;left: 0; width: 100%;height: 100%;}')
#             file.write("</style></head>\n<body><table>")
#             for r in range(grid.rows_number):
#                 file.write("<tr>\n")
#                 for c in range(grid.columns_number):
#                     if isinstance(grid.value(r, c), list):
#                         sum_row = grid.value(r, c)[0]
#                         sum_column = grid.value(r, c)[1]
#                         file.write(f"<td class='sum-cell'>")
#                         file.write(f"<span class='row'>{sum_row if sum_row != 0 else ''}</span>")
#                         file.write(f"<span class='column'>{sum_column if sum_column != 0 else ''}</span>")
#                         if sum_row != 0 or sum_column != 0:
#                             file.write('<svg class="line">')
#                             file.write('<line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/>')
#                             file.write('</svg>')
#                         file.write("</td>")
#                         pass
#                     else:
#                         file.write(f"<td class='number-cell'>{grid.value(r, c)}</td>")
#                 file.write("</tr>\n")
#             file.write("</table></body></html>")
#         webbrowser.open(file_path)
# 
# 
# if __name__ == '__main__':
#     KakuroMainConsole.main()
