﻿from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleStarBattlePlayer(PlaywrightPlayer):
    game_name = "starBattle"
    def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position_index in [position.r * solution.columns_number + position.c for position, value in solution if value]:
            cells[position_index].click(click_count=2)

        self.close()
        self._process_video(video, rectangle, 0)
