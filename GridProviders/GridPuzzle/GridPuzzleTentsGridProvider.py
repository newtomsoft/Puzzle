import math
from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider

class GridPuzzleTentsGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridProvider):
    _tree_value = -1  # Value used by TentsSolver to identify trees

    def get_grid(self, url: str):
        # The TentsSolver expects a tuple: (Grid, dict[str, list[int]])
        # where the dict contains 'row' and 'column' clues.
        return self.with_playwright(self.scrap_grid_and_clues, url)

    def scrap_grid_and_clues(self, browser: BrowserContext, url: str) -> tuple[Grid, dict[str, list[int]]]:
        html_page = self.get_html(browser, url, board_selector="#g_canvas") # Assuming #g_canvas, might need adjustment
        soup = BeautifulSoup(html_page, 'html.parser')

        # --- Grid Dimensions and Trees ---
        # TODO: Developer needs to inspect gridpuzzle.com/tents to find the correct selectors
        # Example assumes grid cells are divs, and trees are marked with a specific class.

        game_area = soup.find('div', id='game_grid') # Placeholder ID
        if not game_area:
            pass

        row_count = 0
        col_count = 0

        grid_div = soup.select_one('#g_canvas > div') # Highly speculative selector

        if grid_div:
            style = grid_div.get('style', '')
            if 'grid-template-columns' in style:
                col_count = len(style.split('grid-template-columns:')[1].split('repeat(')[1].split(',')[0]) if 'repeat' in style else len(style.split('grid-template-columns:')[1].strip().split(' '))
                row_count = len(style.split('grid-template-rows:')[1].split('repeat(')[1].split(',')[0]) if 'repeat' in style else len(style.split('grid-template-rows:')[1].strip().split(' '))

        if row_count == 0 or col_count == 0:
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'var col' in script.string and 'var row' in script.string:
                    import re
                    match_cols = re.search(r'var C=(\d+);', script.string)
                    match_rows = re.search(r'var R=(\d+);', script.string)
                    if match_cols and match_rows:
                        col_count = int(match_cols.group(1))
                        row_count = int(match_rows.group(1))
                        break
            if row_count == 0 or col_count == 0:
                raise ValueError("Could not determine grid dimensions from HTML. Needs manual inspection and update of selectors.")

        matrix = [[0 for _ in range(col_count)] for _ in range(row_count)]

        tree_data_script = None
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'var d = [' in script.string:
                tree_data_script = script.string
                break

        if tree_data_script:
            import re
            match = re.search(r'var d = (\[[^\]]+\]);', tree_data_script)
            if match:
                data_str = match.group(1)
                try:
                    parsed_data = eval(data_str)
                    if len(parsed_data) == row_count:
                        for r_idx, row_str in enumerate(parsed_data):
                            if len(row_str) == col_count:
                                for c_idx, char_val in enumerate(row_str):
                                    if char_val.upper() == 'T':
                                        matrix[r_idx][c_idx] = self._tree_value
                            else:
                                print(f"Warning: Row {r_idx} data length mismatch.")
                    else:
                        print("Warning: Tree data row count mismatch with detected row_count.")
                except Exception as e:
                    print(f"Error parsing tree data from script: {e}")
            else:
                print("Warning: Could not parse 'var d' for tree data. Grid will not have trees.")
        else:
            print("Warning: No script found with 'var d' for tree data. Grid will not have trees.")

        row_clues = []
        col_clues = []

        if tree_data_script:
            import re
            match_row_clues = re.search(r'var row = (\[[\d,]+\]);', tree_data_script) # Fixed regex
            match_col_clues = re.search(r'var col = (\[[\d,]+\]);', tree_data_script) # Fixed regex

            if match_row_clues:
                try:
                    row_clues_str = match_row_clues.group(1)
                    row_clues = eval(row_clues_str)
                except Exception as e:
                    print(f"Error parsing row clues from script: {e}")
            if not row_clues or len(row_clues) != row_count:
                print(f"Warning: Row clues parsing failed or mismatch. Expected {row_count}, got {len(row_clues)}.")
                row_clues = [-1] * row_count

            if match_col_clues:
                try:
                    col_clues_str = match_col_clues.group(1)
                    col_clues = eval(col_clues_str)
                except Exception as e:
                    print(f"Error parsing column clues from script: {e}")
            if not col_clues or len(col_clues) != col_count:
                print(f"Warning: Col clues parsing failed or mismatch. Expected {col_count}, got {len(col_clues)}.")
                col_clues = [-1] * col_count

        else:
            print("Warning: No script found for row/column clues. Using placeholder clues.")
            row_clues = [-1] * row_count
            col_clues = [-1] * col_count

        if not matrix:
             raise ValueError("Failed to parse the grid matrix.")
        if not row_clues or not col_clues :
             raise ValueError("Failed to parse row or column clues.")
        if len(row_clues) != row_count:
            raise ValueError(f"Mismatch in row clue count. Expected {row_count}, got {len(row_clues)}")
        if len(col_clues) != col_count:
            raise ValueError(f"Mismatch in column clue count. Expected {col_count}, got {len(col_clues)}")

        grid_obj = Grid(matrix)
        tents_numbers = {"row": row_clues, "column": col_clues}

        return grid_obj, tents_numbers
