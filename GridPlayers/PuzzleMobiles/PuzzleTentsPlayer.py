﻿from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleTentsPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.tents-cell-back > div:not(.print-helper)")
        for position, value in [(position, value) for (position, value) in solution if value]:
            index = position.r * solution.columns_number + position.c
            bounding_box = cells[index].bounding_box()
            x = bounding_box['x'] + bounding_box['width'] / 2
            y = bounding_box['y'] + bounding_box['height'] / 2
            page.mouse.move(x, y)
            page.mouse.down()
            page.mouse.up()

        self.submit_score(page)
        sleep(60)
