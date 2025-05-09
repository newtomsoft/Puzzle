﻿import math

from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider
from Domain.Board.RegionsGrid import RegionsGrid


class PuzzleStitchesGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page)
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        matrix_cells = [cell_div for cell_div in cell_divs if 'selectable' in cell_div.get('class', [])]
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        borders_dict = {'br': 'right', 'bl': 'left', 'bt': 'top', 'bb': 'bottom'}
        opens = {'right', 'left', 'top', 'bottom'}
        open_matrix = [[set() for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            cell_classes = cell.get('class', [])
            if row == 0:
                cell_classes.append('bt')
            if row == row_count - 1:
                cell_classes.append('bb')
            if col == 0:
                cell_classes.append('bl')
            if col == column_count - 1:
                cell_classes.append('br')
            cell_borders = {borders_dict[cls] for cls in cell_classes if cls in borders_dict.keys()}
            open_matrix[row][col] = opens - cell_borders

        regions_grid = RegionsGrid(open_matrix)

        task_cells = [cell_div for cell_div in cell_divs if 'task' in cell_div.get('class', [])]
        dots = [int(cell_div.text) for cell_div in task_cells]
        dots_by_column_row = {'column': dots[:row_count], 'row': dots[row_count:]}

        puzzle_info_text = self.get_puzzle_info_text(soup)
        puzzle_info_text_left = puzzle_info_text.split('÷')[0]
        if puzzle_info_text_left.isdigit():
            regions_connections = int(puzzle_info_text_left)
        elif '/' in puzzle_info_text_left:
            regions_connections = int(puzzle_info_text_left.split('/')[1])
        else:
            Warning(f"Can't parse regions connections from {puzzle_info_text_left} force to 1")
            regions_connections = 1

        return regions_grid, dots_by_column_row, regions_connections
