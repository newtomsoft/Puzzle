﻿import webbrowser

from Grid import Grid
from GridProviders.QueensGridProvider import QueensGridProvider
from GridProviders.StringGridProvider import StringGridProvider
from Puzzles.Queens.QueensGame import QueensGame


class QueensMainConsole:
    @staticmethod
    def main():
        grid = QueensMainConsole.get_grid()
        QueensMainConsole.run(grid)

    @staticmethod
    def get_grid():
        print("Queens Game")
        print("Enter url or grid")
        print("https://www.linkedin.com/games/queens/ ? (y if yes)")
        console_input = input()
        if console_input == "y":
            console_input = "https://www.linkedin.com/games/queens/"
        url_patterns = {
            r"https://www.linkedin.com/games/queens/": QueensGridProvider
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid: Grid):
        try:
            game = QueensGame(grid)
        except ValueError as e:
            print(f"Error: {e}")
            return
        solution_grid = game.get_solution()
        if solution_grid:
            print(f"Solution found")
            printable_grid = Grid([['*' if solution_grid.value(r, c) else ' ' for c in range(grid.columns_number)] for r in range(grid.rows_number)])
            police_color_grid = Grid([[16 for _ in range(grid.columns_number)] for _ in range(grid.rows_number)])
            printable_grid_string = printable_grid.to_console_string(police_color_grid, grid)
            print(printable_grid_string)
            QueensMainConsole.generate_html(grid, solution_grid)
        else:
            print(f"No solution found")

    @staticmethod
    def generate_html(grid: Grid, solution_grid: Grid):
        color_map = {
            0: "#bba3e2",
            1: "#ffc992",
            2: "#96beff",
            3: "#b3dfa0",
            4: "#dfdfdf",
            5: "#ff7b60",
            6: "#e6f388",
            7: "#b9b29e",
            8: "#dfa0bf",
            9: "#a3d2d8",
            10: "#62efea",
            11: "#ff93f3",
            12: "#8acc6d",
            13: "#729aec",
            14: "#c387e0",
            15: "#ffe04b",
        }

        file_path = "solution.html"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 40px; height: 40px; text-align: center;}</style></head><body><table>")
            for r in range(solution_grid.rows_number):
                file.write("<tr>")
                for c in range(solution_grid.columns_number):
                    inner_text = '♛' if solution_grid.value(r, c) is True else ''
                    background_color = color_map.get(grid.value(r, c))
                    file.write(f"<td style='background-color: {background_color};'>{inner_text}</td>")
                file.write("</tr>")
            file.write("</table></body></html>")
        webbrowser.open(file_path)


if __name__ == '__main__':
    QueensMainConsole.main()