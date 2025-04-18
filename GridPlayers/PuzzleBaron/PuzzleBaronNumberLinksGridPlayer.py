﻿from time import sleep

from playwright.sync_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class PuzzleBaronNumberLinksGridPlayer(PlaywrightGridPlayer):
    @classmethod
    def play(cls, solution: Grid, browser: BrowserContext):
        page = browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')
        numbers = [int(inner_text) if (inner_text := number_div.inner_text()) else -1 for number_div in grid_box_divs]

        numbers_processed = set()
        for start_position, start_value in solution:
            if numbers[solution.get_index_from_position(start_position)] == -1 or start_value in numbers_processed:
                continue
            numbers_processed.add(start_value)
            positions_processed = {start_position}
            cls.mouse_move(page.mouse, solution, start_position, grid_box_divs)
            cls.mouse_down(page.mouse)
            next_position = cls._next_position(solution, start_position, start_value, positions_processed)
            while next_position:
                positions_processed.add(next_position)
                cls.mouse_move(page.mouse, solution, next_position, grid_box_divs)
                next_position = cls._next_position(solution, next_position, start_value, positions_processed)
        cls.mouse_up(page.mouse)
        sleep(20)

    @classmethod
    def _next_position(cls, solution: Grid[int], start_position: Position, start_value: int, positions_processed: set[Position]) -> Position:
        return next((neighbor_position for neighbor_position in solution.neighbors_positions(start_position) if neighbor_position not in positions_processed and solution[neighbor_position] == start_value), None)
