﻿from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleKakurasuGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.cell')
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        counters_side = soup.find('div', class_='side-counters')
        numbers_side = self._get_numbers(counters_side)
        counters_top = soup.find('div', class_='top-counters')
        numbers_top = self._get_numbers(counters_top)
        return {'side': numbers_side, 'top': numbers_top}

    @staticmethod
    def _get_numbers(counters) -> list[int]:
        numbers: list[int] = []
        for sc in counters.find_all('span', class_='sc2'):
            numbers.append(int(sc.get_text()))
        return numbers
