from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from playwright.sync_api import Page, BrowserContext

class GridPuzzleTentsPlayer(PlaywrightPlayer):
    def __init__(self, browser_context: BrowserContext):
        super().__init__(browser_context)
        self.page: Page = browser_context.pages[0]

    def play(self, solution: Grid):
        # solution is a boolean grid: True for tent, False for grass/empty.
        # Trees are part of the input grid to the solver, not part of the solution to play.

        # Attempt to find individual cell divs, similar to StarBattle
        cell_elements = self.page.query_selector_all("#g_canvas > div > div.g_cell") # Common pattern on gridpuzzle

        # If no g_cell found, try a slightly less specific selector if canvas contains rows of cells
        if not cell_elements:
            cell_elements = self.page.query_selector_all("#g_canvas > div > div > div") # e.g. canvas > row_container > cell_div

        rows = solution.rows_number
        cols = solution.columns_number

        if cell_elements and len(cell_elements) == rows * cols:
            print(f"Found {len(cell_elements)} 'g_cell' like elements. Proceeding with div-clicking strategy.")
            for r in range(rows):
                for c in range(cols):
                    if solution[Position(r, c)]: # If True, means it should be a Tent
                        cell_index = r * cols + c
                        try:
                            # TODO: Determine the correct click action for Tents.
                            # It might be a single click, double click, or right click.
                            # For some puzzles, one click = Tent, another click on tent = Grass.
                            # We assume one click places a tent if the cell is empty.
                            # If the puzzle cycles Tent -> Grass -> Empty, and we only want tents,
                            # this simple click is fine if the board is clear or if clicking a tent does nothing.
                            cell_elements[cell_index].click()
                            self.page.wait_for_timeout(50) # Small delay to allow UI to update if needed
                        except Exception as e:
                            print(f"Error clicking cell ({r},{c}): {e}")
            print("Finished clicking based on div cells.")

        else:
            print(f"Did not find expected 'g_cell' elements (found {len(cell_elements)}, expected {rows*cols}).")
            print("Falling back to canvas click strategy. This requires canvas dimensions and assumes clicks place tents.")

            # Fallback: Canvas clicking (less reliable without precise element inspection)
            # This assumes the board is a single canvas element.
            # The GridPuzzleTentsGridProvider used #g_canvas as a potential board_selector
            canvas_element = self.page.query_selector("#g_canvas") # Or the actual canvas selector
            if not canvas_element:
                print("ERROR: Canvas element not found with selector #g_canvas. Cannot play.")
                self.close()
                return

            bounding_box = canvas_element.bounding_box()
            if not bounding_box:
                print("ERROR: Canvas element has no bounding box. Cannot calculate click positions.")
                self.close()
                return

            canvas_x = bounding_box['x']
            canvas_y = bounding_box['y']
            canvas_width = bounding_box['width']
            canvas_height = bounding_box['height']

            # Assuming the grid cells are uniformly distributed within the canvas.
            # This might not be true if there are borders, padding, or clue numbers rendered within the same canvas.
            cell_width = canvas_width / cols
            cell_height = canvas_height / rows

            print(f"Canvas dimensions: w={canvas_width}, h={canvas_height}. Cell approx: w={cell_width}, h={cell_height}")

            for r in range(rows):
                for c in range(cols):
                    if solution[Position(r, c)]: # If True, means it should be a Tent
                        # Calculate center of the cell
                        click_x = canvas_x + (c + 0.5) * cell_width
                        click_y = canvas_y + (r + 0.5) * cell_height

                        try:
                            # TODO: Determine the correct click action for Tents on canvas.
                            # One click to place a tent? Or cycle through Tent/Grass?
                            self.page.mouse.click(click_x, click_y)
                            self.page.wait_for_timeout(100) # Wait a bit for the click to register and UI to update
                        except Exception as e:
                            print(f"Error clicking canvas at ({r},{c}) at coordinates ({click_x:.2f}, {click_y:.2f}): {e}")
            print("Finished clicking based on canvas strategy.")

        # video, rectangle = self._get_data_video_viewport(self.page) # If video recording is needed
        self.close()
        # self._process_video(video, "tents_gridpuzzle", rectangle, 0) # If video recording is needed
