import unittest
from unittest.mock import patch, MagicMock

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleTentsGridProvider import GridPuzzleTentsGridProvider

class GridPuzzleTentsGridProviderTest(unittest.TestCase):

    def test_scrap_grid_and_clues_basic_parsing(self):
        # This test uses a simplified mock HTML focusing on the JavaScript variable parsing.
        # A developer should replace this with more realistic HTML from gridpuzzle.com/tents.
        mock_html_content = """
        <html>
            <head>
                <script>
                    var R=2; // Rows
                    var C=2; // Columns
                    var row=[1,1]; // Clues for rows
                    var col=[1,1]; // Clues for columns
                    var d=["T.",".T"]; // Grid data: T=Tree, .=Empty
                </script>
            </head>
            <body>
                <div id="g_canvas">
                    <div>
                        <!-- Cells would normally be here if not pure canvas -->
                    </div>
                </div>
            </body>
        </html>
        """

        # Mock the GridPuzzleGridProvider's get_html method to return our sample HTML
        # Also mock 'with_playwright' which is part of the call chain
        with patch.object(GridPuzzleTentsGridProvider, 'get_html', return_value=mock_html_content) as mock_get_html:
            provider = GridPuzzleTentsGridProvider()

            # Mock the browser context that would normally be passed by with_playwright
            mock_browser_context = MagicMock()

            # Call scrap_grid_and_clues directly for testing, bypassing with_playwright's browser management
            grid_obj, tents_numbers = provider.scrap_grid_and_clues(mock_browser_context, "http://dummyurl.com/tents")

            mock_get_html.assert_called_once_with(mock_browser_context, "http://dummyurl.com/tents", board_selector="#g_canvas")

            # Expected Grid: Trees (-1) and empty cells (0)
            # d=["T.",".T"] translates to:
            # T .  => -1  0
            # . T  =>  0 -1
            expected_matrix = [
                [GridPuzzleTentsGridProvider._tree_value, 0],
                [0, GridPuzzleTentsGridProvider._tree_value]
            ]
            expected_grid = Grid(expected_matrix)
            self.assertEqual(expected_grid.matrix, grid_obj.matrix, "Grid matrix did not match expected.")

            # Expected clues
            expected_clues = {
                "row": [1, 1],
                "column": [1, 1]
            }
            self.assertEqual(expected_clues, tents_numbers, "Tent numbers (clues) did not match expected.")

    def test_scrap_grid_and_clues_missing_data(self):
        # Test with HTML where script variables might be missing or malformed
        mock_html_content_missing = """
        <html>
            <head>
                <script>
                    // R, C, row, col, d are missing
                </script>
            </head>
            <body>
                <div id="g_canvas"></div>
            </body>
        </html>
        """
        with patch.object(GridPuzzleTentsGridProvider, 'get_html', return_value=mock_html_content_missing):
            provider = GridPuzzleTentsGridProvider()
            mock_browser_context = MagicMock()
            with self.assertRaises(ValueError) as context:
                provider.scrap_grid_and_clues(mock_browser_context, "http://dummyurl.com/tents_missing")

            self.assertTrue("Could not determine grid dimensions" in str(context.exception) or "Failed to parse" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
