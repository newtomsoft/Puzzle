import math
import re

from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridTagProvider import GridPuzzleGridTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleYajikabeGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        direction_map = {
            'r': '→',
            'd': '↓',
            'l': '←',
            'u': '↑',
        }
        html_page = self.get_html(browser, url, "#puzzle-main")
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            text = cell.get_text().strip()
            if text:
                arrow_div = cell.find('div', class_=re.compile(r'\barrow_[rdlu]\b'))
                classes = arrow_div.get('class', '')
                dir_match = next((re.fullmatch(r'arrow_([rdlu])', cls) for cls in classes if cls.startswith('arrow_')), None)
                matrix[row][col] = f"{text}{direction_map[dir_match.group(1)]}"
            else:
                matrix[row][col] = ''

        return Grid(matrix)


    @staticmethod
    def _get_grid_data(html_page: str) -> tuple[BeautifulSoup, int, int, list[list], ResultSet[PageElement | Tag | NavigableString]]:
        soup = BeautifulSoup(html_page, 'html.parser')
        matrix_cells = soup.find_all('div', class_='cell')
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [['' for _ in range(column_count)] for _ in range(row_count)]
        return soup, row_count, column_count, matrix, matrix_cells