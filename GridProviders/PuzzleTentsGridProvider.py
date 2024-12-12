﻿from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Utils.Grid import Grid


class PuzzleTentsGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.new_page()
        page.goto(url)
        html_page = page.content()
        browser.close()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_=['cell'])
        grid_cell_divs = [cell_div for cell_div in cell_divs if 'task' not in cell_div.get('class', [])]
        rows_count = len([1 for cell in grid_cell_divs if 'left: 3px' in cell['style']])
        columns_count = len([1 for cell in grid_cell_divs if 'top: 3px' in cell['style']])
        cells_count = rows_count * columns_count
        trees = [-1 if 'tree-cell' in cell_div.get('class', []) else 0 for cell_div in grid_cell_divs]
        matrix = []
        for i in range(0, cells_count, columns_count):
            matrix.append(trees[i:i + columns_count])

        task_cells = [cell_div for cell_div in cell_divs if 'task' in cell_div.get('class', [])]
        tents_numbers = [int(cell_div.text) for cell_div in task_cells]
        tents_numbers_by_column_row = {'column': tents_numbers[:rows_count], 'row': tents_numbers[rows_count:]}
        return Grid(matrix), tents_numbers_by_column_row
