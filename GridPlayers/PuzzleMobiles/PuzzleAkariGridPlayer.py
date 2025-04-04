﻿from time import sleep

from playwright.sync_api import BrowserContext

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleAkariGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
    @classmethod
    def play(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        cells = page.query_selector_all("div.cell, div.light-up-task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                cells[index].click()

        cls.submit_score(page)
        sleep(60)
