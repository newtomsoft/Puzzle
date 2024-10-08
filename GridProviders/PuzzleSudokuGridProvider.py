﻿import math

from playwright.sync_api import BrowserContext

from Grid import Grid
from GridProvider import GridProvider
from PlaywrightGridProvider import PlaywrightGridProvider


class PuzzleSudokuGridProvider(GridProvider, PlaywrightGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.new_page()
        page.goto(url)
        numbers_divs = page.query_selector_all('div.number')
        numbers_str = [inner_text if (inner_text := number_div.inner_text()) else -1 for number_div in numbers_divs]
        cells_count = len(numbers_str)
        side = int(math.sqrt(cells_count))
        conversion_base = side + 1
        numbers = [int(number, conversion_base) if number != -1 else -1 for number in numbers_str]
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(numbers[i:i + side])
        browser.close()
        return Grid(matrix)