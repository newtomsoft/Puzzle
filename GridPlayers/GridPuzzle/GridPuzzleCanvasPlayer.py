﻿from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position


class GridPuzzleCanvasPlayer:
    def _draw_loop(self, cell_height, cell_width, page, solution, x0, y0):
        connected_positions = self._get_connected_positions(solution, True)
        for index, position in enumerate(connected_positions[:-1]):
            next_position = connected_positions[index + 1]
            direction = position.direction_to(next_position)
            self._trace_direction_from_position(direction, position, page, cell_width, cell_height, x0, y0)

    @staticmethod
    def _get_connected_positions(island_grid: IslandGrid, end_with_first: bool = False) -> list[Position]:
        connected_positions = island_grid.follow_path()
        if end_with_first:
            connected_positions.append(connected_positions[0])
        return connected_positions

    @staticmethod
    def _get_connected_positions_from_position(island_grid: IslandGrid, position: Position, end_with_first: bool = False) -> list[Position]:
        connected_positions = island_grid.follow_path(position)
        if end_with_first:
            connected_positions.append(connected_positions[0])
        return connected_positions

    @staticmethod
    def _trace_direction_from_position(direction, position, page, cell_width, cell_height, x0, y0):
        if direction == Direction.right():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + (position.c + 1) * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.up()
            return
        if direction == Direction.down():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + (position.r + 1) * cell_height)
            page.mouse.up()
            return
        if direction == Direction.left():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + (position.c - 1) * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.up()
            return
        if direction == Direction.up():
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            page.mouse.down()
            page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + (position.r - 1) * cell_height)
            page.mouse.up()
            return
