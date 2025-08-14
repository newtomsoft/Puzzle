from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridProvider import GridProvider
from GridProviders.GridPuzzle.GridPuzzleGridTagProvider import GridPuzzleGridTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleHakoiriGridProvider(GridProvider, PlaywrightGridProvider, GridPuzzleGridTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url, '.col-lg-12.col-md-12.col-12')
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        bounded_matrix = self.make_bounded_matrix(row_count, column_count, matrix_cells)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            div = cell.find('div')
            if div:
                div_classes = div.get('class', '')
                if div_classes:
                    div_class = div_classes[0]
                    if div_class == 'circle':
                        matrix[row][col] = 1
                    elif div_class == 'square':
                        matrix[row][col] = 2
                    elif div_class == 'triangle':
                        matrix[row][col] = 3
                    else:
                        matrix[row][col] = 0
            else:
                matrix[row][col] = 0

        return RegionsGrid(bounded_matrix), Grid(matrix)
