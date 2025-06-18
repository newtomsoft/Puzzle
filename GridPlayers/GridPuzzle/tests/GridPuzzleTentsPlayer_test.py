import unittest
from unittest.mock import MagicMock, patch

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.GridPuzzleTentsPlayer import GridPuzzleTentsPlayer

class GridPuzzleTentsPlayerTest(unittest.TestCase):

    def setUp(self):
        self.mock_browser_context = MagicMock()
        self.mock_page = MagicMock()
        self.mock_browser_context.pages = [self.mock_page]
        self.player = GridPuzzleTentsPlayer(self.mock_browser_context)

    def test_play_with_div_cells_strategy(self):
        # Solution grid: 2x2, one tent at (0,1) and one at (1,0)
        solution_matrix = [[False, True], [True, False]]
        solution_grid = Grid(solution_matrix)

        # Mock page.query_selector_all to return 4 mock cell elements
        mock_cell_elements = [MagicMock() for _ in range(4)]
        self.mock_page.query_selector_all.return_value = mock_cell_elements

        # For verbose logging from player
        with patch('builtins.print') as mock_print:
            self.player.play(solution_grid)

            # Assert query_selector_all was called to find cells
            # It tries two selectors:
            self.mock_page.query_selector_all.assert_any_call("#g_canvas > div > div.g_cell")
            # If the first returned empty, it would try the second. We assume first call returns elements.

            # Expected clicks:
            # Cell at (0,1) is cell_index 1 (0*2 + 1)
            # Cell at (1,0) is cell_index 2 (1*2 + 0)
            mock_cell_elements[1].click.assert_called_once()
            mock_cell_elements[2].click.assert_called_once()

            # Ensure other cells were not clicked
            mock_cell_elements[0].click.assert_not_called()
            mock_cell_elements[3].click.assert_not_called()

            mock_print.assert_any_call("Found 4 'g_cell' like elements. Proceeding with div-clicking strategy.")


    def test_play_with_canvas_click_strategy(self):
        solution_matrix = [[True, False], [False, True]]
        solution_grid = Grid(solution_matrix) # Tents at (0,0) and (1,1)

        # Mock page.query_selector_all to return empty list (forcing canvas strategy)
        self.mock_page.query_selector_all.return_value = []

        # Mock canvas element and its bounding_box
        mock_canvas = MagicMock()
        mock_canvas.bounding_box.return_value = {'x': 0, 'y': 0, 'width': 200, 'height': 200}
        self.mock_page.query_selector.return_value = mock_canvas

        # For verbose logging from player
        with patch('builtins.print') as mock_print:
            self.player.play(solution_grid)

            self.mock_page.query_selector.assert_called_with("#g_canvas")

            # Expected clicks on canvas for a 2x2 grid:
            # Cell (0,0) center: (0 + 0.5) * (200/2) = 50, (0 + 0.5) * (200/2) = 50
            # Cell (1,1) center: (0 + 1.5) * (200/2) = 150, (0 + 1.5) * (200/2) = 150

            self.mock_page.mouse.click.assert_any_call(50.0, 50.0)
            self.mock_page.mouse.click.assert_any_call(150.0, 150.0)
            self.assertEqual(self.mock_page.mouse.click.call_count, 2)

            mock_print.assert_any_call("Did not find expected 'g_cell' elements (found 0, expected 4).")
            mock_print.assert_any_call("Falling back to canvas click strategy. This requires canvas dimensions and assumes clicks place tents.")

    def test_play_canvas_not_found(self):
        solution_matrix = [[True]]
        solution_grid = Grid(solution_matrix)

        self.mock_page.query_selector_all.return_value = [] # Force canvas strategy
        self.mock_page.query_selector.return_value = None # Canvas not found

        with patch('builtins.print') as mock_print:
            self.player.play(solution_grid)
            mock_print.assert_any_call("ERROR: Canvas element not found with selector #g_canvas. Cannot play.")
            self.player.close.assert_called_once() # Ensure player closes if it cannot proceed


if __name__ == '__main__':
    unittest.main()
