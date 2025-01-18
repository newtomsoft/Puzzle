import unittest
from unittest import TestCase

from Puzzles.Shingoki.ShingokiGame import ShingokiGame
from Utils.Grid import Grid


class ShingokiGameTests(TestCase):
    def test_solution_white_horizontal_w2(self):
        grid = Grid([
            [' ', 'w2', ' '],
            [' ', 'w2', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_w3(self):
        grid = Grid([
            [' ', ' ', 'w3', ' '],
            [' ', 'w3', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_w2(self):
        grid = Grid([
            [' ', ' '],
            ['w2', 'w2'],
            [' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_w3(self):
        grid = Grid([
            [' ', ' '],
            ['w3', ' '],
            [' ', 'w3'],
            [' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_0(self):
        grid = Grid([
            [' ', 'w2', ' '],
            ['w2', ' ', ' '],
            [' ', 'w2', ' ']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │     │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_1(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            ['w3', ' ', ' ', 'w2'],
            [' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', ' ']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │        │ \n'
            ' │     ┌──┘ \n'
            ' └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_2(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            ['w3', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' '],
            [' ', 'w2', ' ', ' ']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │     ┌──┘ \n'
            ' │     │    \n'
            ' └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_down_b2_4(self):
        grid = Grid([
            [' ', 'b2', ' '],
            ['b2', ' ', ' '],
            [' ', ' ', 'b4'],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '    ┌──┐ \n'
            ' ┌──┘  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_down_b3(self):
        grid = Grid([
            [' ', 'b3', ' ', ' '],
            ['b3', ' ', ' ', ' '],
            [' ', 'b3', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '    ┌─────┐ \n'
            ' ┌──┘     │ \n'
            ' │  ┌─────┘ \n'
            ' └──┘       '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_up_b2_4(self):
        grid = Grid([
            [' ', ' ', 'b4'],
            ['b2', ' ', ' '],
            [' ', 'b2', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            '    └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_up_b3(self):
        grid = Grid([
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['b3', ' ', 'b3', ' '],
            [' ', 'b3', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐    \n'
            ' │     │    \n'
            ' └──┐  └──┐ \n'
            '    └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_down_b2_4(self):
        grid = Grid([
            [' ', 'b2', ' '],
            [' ', ' ', 'b2'],
            ['b4', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐    \n'
            ' │  └──┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_down_b3(self):
        grid = Grid([
            [' ', ' ', 'b3', ' '],
            [' ', 'b3', ' ', 'b3'],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐    \n'
            ' └──┐  └──┐ \n'
            '    │     │ \n'
            '    └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_up_b2_4(self):
        grid = Grid([
            ['b4', ' ', ' '],
            [' ', ' ', 'b2'],
            [' ', 'b2', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ┌──┘ \n'
            ' └──┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_black(self):
        grid = Grid([
            [' ', 'w2', ' '],
            [' ', ' ', 'b2'],
            [' ', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ┌──┘ \n'
            ' └──┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_0(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' '],
            ['b5', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w4', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b6', ' ', 'b2'],
            [' ', 'w4', ' ', ' ', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '    ┌──┐  ┌──┐    \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  │     │  └──┐ \n'
            ' │  └─────┘  ┌──┘ \n'
            ' └───────────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_1(self):
        grid = Grid([
            ['b6', ' ', ' ', 'w5', ' ', ' '],
            [' ', ' ', 'b6', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b4'],
            [' ', 'b2', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', 'b5', ' ', ' '],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐ \n'
            ' └──┐  ┌─────┐  │ \n'
            ' ┌──┘  │  ┌──┘  │ \n'
            ' └──┐  │  │  ┌──┘ \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' └─────┘  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_2(self):
        grid = Grid([
            [' ', ' ', ' ', 'w3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', 'b3', 'b2', ' '],
            ['b4', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', 'b4', ' ', 'b3'],
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌────────┐ \n'
            ' │  │  └──┐  ┌──┘ \n'
            ' │  └─────┘  └──┐ \n'
            ' └──┐  ┌──┐  ┌──┘ \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' └─────┘  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_0(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' '],
            [' ', 'w3', ' ', ' ', ' ', 'b6', 'b4', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', 'b3', ' '],
            ['b4', 'b2', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '    ┌─────────────────┐ \n'
            '    │  ┌────────┐  ┌──┘ \n'
            '    │  │        │  │    \n'
            ' ┌──┘  └─────┐  │  │    \n'
            ' │  ┌─────┐  │  └──┘    \n'
            ' │  └──┐  │  └─────┐    \n'
            ' └──┐  │  └─────┐  └──┐ \n'
            '    └──┘        └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'w3'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b4', ' ', 'w4', 'w6', 'b4', ' ', ' '],
            ['w6', 'b2', ' ', ' ', ' ', ' ', ' ', 'w3'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '    ┌───────────┐  ┌──┐ \n'
            ' ┌──┘  ┌─────┐  └──┘  │ \n'
            ' │  ┌──┘     │  ┌──┐  │ \n'
            ' │  │  ┌──┐  │  │  └──┘ \n'
            ' │  │  │  │  │  │  ┌──┐ \n'
            ' │  └──┘  │  │  └──┘  │ \n'
            ' │  ┌──┐  │  │  ┌──┐  │ \n'
            ' └──┘  └──┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([
            ['b3', ' ', ' ', 'b2', ' ', ' ', 'b2', ' ', ' ', 'w2', ' '],
            [' ', ' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' '],
            ['b6', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', ' '],
            [' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', 'b4', ' '],
            [' ', 'w2', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'w5'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b2'],
            [' ', ' ', ' ', 'w4', ' ', 'b5', ' ', ' ', ' ', 'b5', ' ']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐     ┌──┐     ┌──┐  ┌─────┐ \n'
            ' │  └─────┘  └─────┘  │  │  ┌──┘ \n'
            ' └──┐  ┌──┐  ┌─────┐  │  │  └──┐ \n'
            '    └──┘  │  └──┐  │  │  └──┐  │ \n'
            ' ┌─────┐  └─────┘  │  └─────┘  │ \n'
            ' │  ┌──┘     ┌──┐  └────────┐  │ \n'
            ' │  │     ┌──┘  └──┐     ┌──┘  │ \n'
            ' │  └──┐  └─────┐  │  ┌──┘  ┌──┘ \n'
            ' └──┐  │  ┌─────┘  │  └──┐  └──┐ \n'
            ' ┌──┘  └──┘  ┌──┐  └─────┘  ┌──┘ \n'
            ' └───────────┘  └───────────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow')
    def test_solution_16x16(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'w2', ' ', 'w2', 'w2', ' ', ' ', ' ', 'w3'],
            [' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'w3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b5', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w4', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b3', ' ', 'w3', ' ', ' '],
            [' ', ' ', ' ', 'w3', 'w5', 'w4', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'b4', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'w2', ' '],
            ['w15', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w11', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b3', 'b2', ' ', ' ', ' ', ' ', 'b6'],
            [' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' '],
            [' ', ' ', ' ', ' ', 'b2', 'b5', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b2', 'b3'],
            [' ', 'w2', ' ', ' ', ' ', 'b2', ' ', ' ', 'b2', 'b3', ' ', ' ', ' ', 'b3', ' ', 'b2'],
            [' ', ' ', 'b2', ' ', 'b3', ' ', 'b2', ' ', ' ', ' ', ' ', 'b3', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w6', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌──┐     ┌──┐  ┌──┐  ┌─────┐  ┌──┐ \n'
            ' │  │  │  └──┘  └──┐  │  │  │  │  │  ┌──┘  │  │ \n'
            ' │  │  │  ┌──┐  ┌──┘  │  └──┘  └──┘  │  ┌──┘  │ \n'
            ' │  │  └──┘  │  └─────┘  ┌────────┐  └──┘  ┌──┘ \n'
            ' │  │  ┌──┐  │  ┌──┐  ┌──┘  ┌─────┘  ┌─────┘    \n'
            ' │  │  │  │  │  │  │  │     └─────┐  └────────┐ \n'
            ' │  │  │  │  │  │  │  │  ┌────────┘  ┌─────┐  │ \n'
            ' │  │  │  └──┘  │  └──┘  └──┐  ┌─────┘     │  │ \n'
            ' │  │  └──┐  ┌──┘  ┌─────┐  │  └──┐     ┌──┘  │ \n'
            ' │  │  ┌──┘  └──┐  └──┐  │  └──┐  └──┐  └─────┘ \n'
            ' │  │  └─────┐  └─────┘  └──┐  └──┐  └──┐  ┌──┐ \n'
            ' │  └──┐  ┌──┘  ┌───────────┘     └──┐  └──┘  │ \n'
            ' │  ┌──┘  └──┐  └──┐  ┌───────────┐  └──┐  ┌──┘ \n'
            ' │  │  ┌──┐  │  ┌──┘  └──┐  ┌──┐  └─────┘  └──┐ \n'
            ' │  └──┘  └──┘  └──┐  ┌──┘  │  │  ┌─────┐  ┌──┘ \n'
            ' └─────────────────┘  └─────┘  └──┘     └──┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow')
    def test_solution_21x21(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', 'b5', 'w2', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', 'b7', ' ', 'w5', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b4', 'b4', ' '],
            ['w4', ' ', 'b3', 'w7', ' ', 'b5', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', 'b4', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'w3', 'b2', ' ', ' ', 'b2', ' ', ' '],
            ['b4', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b5', 'b2', 'w4', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', 'b3', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'b2', 'b2', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b6', ' ', 'b2', ' ', ' ', ' ', 'b3', ' ', ' ', ' '],
            [' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', 'w2', 'w2', ' '],
            [' ', ' ', ' ', 'b2', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', 'b4', ' ', 'b6', 'w4', 'w3', ' ', ' ', ' ', 'b3', ' '],
            [' ', ' ', 'b3', 'w2', 'b6', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'b5', ' ', ' ', ' '],
            [' ', 'w5', 'b4', ' ', ' ', ' ', 'w3', 'b4', ' ', 'b4', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'w2', ' ', 'b4', ' ', 'w4', ' ', 'b4', ' ', 'b4', 'w2', ' ', ' '],
            [' ', 'b6', ' ', 'b3', ' ', ' ', ' ', 'b3', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', 'b2', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', 'w2', 'b5', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'w3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' '],
            [' ', ' ', ' ', 'b4', 'b2', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'b5']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌─────┐     ┌─────────────────┐  ┌──────────────┐ \n'
            ' │  │  │  │  │  ┌──┘     └──┐  ┌──┐  ┌──┐  └──┘  ┌─────┐  ┌──┘ \n'
            ' │  └──┘  │  │  └───────────┘  │  └──┘  └─────┐  │     │  │    \n'
            ' │  ┌──┐  │  └──┐  ┌───────────┘  ┌─────┐  ┌──┘  │  ┌──┘  │    \n'
            ' └──┘  │  │     │  │     ┌─────┐  │  ┌──┘  │  ┌──┘  └──┐  └──┐ \n'
            ' ┌──┐  │  │     │  └──┐  │  ┌──┘  │  │     │  └──┐     └─────┘ \n'
            ' │  └──┘  │     │  ┌──┘  │  │     │  │     └─────┘  ┌──┐       \n'
            ' │  ┌──┐  └─────┘  │     │  └──┐  │  └──┐  ┌──┐     │  └─────┐ \n'
            ' └──┘  └────────┐  │  ┌──┘  ┌──┘  └──┐  └──┘  └──┐  └──┐  ┌──┘ \n'
            '    ┌──┐     ┌──┘  │  │  ┌──┘  ┌─────┘  ┌─────┐  │  ┌──┘  └──┐ \n'
            ' ┌──┘  │     │  ┌──┘  │  └─────┘  ┌─────┘  ┌──┘  │  └──┐  ┌──┘ \n'
            ' └──┐  └──┐  │  │     └────────┐  │        │  ┌──┘     │  │    \n'
            '    │  ┌──┘  │  │              │  └─────┐  │  │  ┌─────┘  └──┐ \n'
            '    │  └─────┘  └─────┐  ┌─────┘  ┌──┐  │  │  │  │  ┌────────┘ \n'
            '    │  ┌──┐  ┌────────┘  │  ┌─────┘  │  │  └──┘  │  │          \n'
            '    │  │  └──┘  ┌──┐     │  │     ┌──┘  │  ┌──┐  │  └─────┐    \n'
            ' ┌──┘  │  ┌─────┘  └──┐  │  └──┐  │  ┌──┘  │  │  │  ┌──┐  └──┐ \n'
            ' └──┐  └──┘  ┌─────┐  │  └──┐  │  │  └──┐  │  │  └──┘  │  ┌──┘ \n'
            '    └──┐     └──┐  │  └─────┘  │  └──┐  │  │  └─────┐  │  │    \n'
            ' ┌─────┘  ┌──┐  │  │  ┌──┐  ┌──┘     │  └──┘  ┌──┐  └──┘  └──┐ \n'
            ' └────────┘  └──┘  └──┘  └──┘        └────────┘  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow')
    def test_solution_26x26(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w11', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', 'b2', 'b3', ' ', 'b2', ' ', ' ', ' ', 'b5', 'w3', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'b6', ' ', 'b5', 'b2', ' ', ' ', ' ', ' ', ' ', 'w2', 'b3', 'b5', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', 'w2', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b4', ' ', 'w5', ' ', ' ', 'w2', ' ', 'b2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', 'w2', ' ', ' ', 'b5'],
            ['b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', 'b4'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b6', 'w5', 'b3', ' ', ' ', 'b2', ' ', ' '],
            ['w4', ' ', ' ', 'w6', ' ', 'w2', ' ', 'w2', ' ', 'w4', 'b2', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'b3', 'w3', ' ', 'b2', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b8', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' '],
            ['w4', 'b2', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w6', ' ', ' ', 'w3', ' ', 'b5', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', 'b3', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b8', 'b3', 'b2'],
            [' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', ' ', 'b3', 'b3', ' ', ' ', ' ', ' ', 'w3', ' ', 'w2', ' ', 'b3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'w2', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' '],
            ['b3', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' '],
            ['b2', 'b4', ' ', ' ', ' ', 'b8', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w7', 'b4', 'b2'],
            [' ', ' ', 'b7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w7', ' ', 'w4', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b3', 'b3', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', 'b3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', 'b4', 'b5', ' ', 'w3', ' ', ' ', 'b4', ' ', ' ', ' ', 'b2', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b6', 'b5', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b8', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'w6', 'b5', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'w4', ' ', ' ', ' ', 'b5', 'b3', 'b5'],
            [' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', 'w2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b4', 'w2', ' ', ' ', 'b4', ' ', 'w3', ' ', ' '],
            ['b5', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', 'w2', 'b2', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'w2', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b10']
        ])
        game = ShingokiGame(grid)
        solution = game.get_solution()
        expected_solution_string = (
            '    ┌─────┐  ┌──┐  ┌────────────────────────────────┐  ┌────────┐  ┌──┐  ┌──┐ \n'
            '    └──┐  └──┘  │  └──┐  ┌────────┐  ┌──────────────┘  └──┐  ┌──┘  │  └──┘  │ \n'
            ' ┌──┐  │  ┌──┐  │  ┌──┘  │     ┌──┘  └─────┐  ┌─────┐  ┌──┘  └──┐  └─────┐  │ \n'
            ' │  └──┘  │  │  │  │  ┌──┘     └─────┐  ┌──┘  │  ┌──┘  │  ┌──┐  │     ┌──┘  │ \n'
            ' │  ┌──┐  │  │  │  │  │     ┌──┐     │  └──┐  │  │     │  │  │  └─────┘  ┌──┘ \n'
            ' └──┘  │  │  │  │  │  └─────┘  └──┐  └──┐  └──┘  └─────┘  │  └────────┐  └──┐ \n'
            ' ┌──┐  │  │  │  └──┘  ┌──┐  ┌──┐  └──┐  └──────────────┐  │  ┌─────┐  └──┐  │ \n'
            ' │  └──┘  │  └─────┐  │  │  │  └──┐  └────────┐  ┌─────┘  │  └──┐  │  ┌──┘  │ \n'
            ' │  ┌─────┘        └──┘  │  │     │  ┌─────┐  │  └────────┘     │  │  │  ┌──┘ \n'
            ' │  └──┐  ┌─────┐  ┌─────┘  │  ┌──┘  └──┐  │  │  ┌────────┐  ┌──┘  └──┘  │    \n'
            ' └──┐  └──┘  ┌──┘  └──┐  ┌──┘  └─────┐  │  │  │  │  ┌──┐  │  └──┐  ┌──┐  └──┐ \n'
            '    │  ┌─────┘        │  │  ┌──┐  ┌──┘  │  │  │  │  │  │  └──┐  │  │  │  ┌──┘ \n'
            '    └──┘           ┌──┘  │  │  │  │  ┌──┘  │  └──┘  │  └──┐  │  │  │  │  │    \n'
            ' ┌─────┐  ┌──┐     └──┐  │  │  └──┘  │     │  ┌─────┘     └──┘  │  │  │  │    \n'
            ' └──┐  └──┘  └──┐  ┌──┘  │  └──┐  ┌──┘     └──┘                 └──┘  │  └──┐ \n'
            '    │  ┌─────┐  │  │  ┌──┘     │  │     ┌──────────────┐  ┌──┐        │  ┌──┘ \n'
            '    │  │  ┌──┘  │  │  │  ┌──┐  │  └──┐  │  ┌──┐  ┌─────┘  │  │  ┌──┐  │  └──┐ \n'
            ' ┌──┘  │  └──┐  │  │  │  │  │  └──┐  └──┘  │  │  └─────┐  │  └──┘  └──┘  ┌──┘ \n'
            ' └──┐  │     │  │  │  │  │  └─────┘  ┌─────┘  └────────┘  │  ┌────────┐  └──┐ \n'
            ' ┌──┘  │  ┌──┘  │  └──┘  └──┐  ┌──┐  │     ┌──────────────┘  └──┐     │  ┌──┘ \n'
            ' │  ┌──┘  └──┐  │     ┌─────┘  │  └──┘     └────────────────────┘     │  │    \n'
            ' │  └─────┐  │  └──┐  │  ┌──┐  │  ┌──┐           ┌───────────┐  ┌─────┘  └──┐ \n'
            ' │  ┌──┐  │  │  ┌──┘  │  │  │  │  │  │     ┌──┐  │  ┌─────┐  │  └────────┐  │ \n'
            ' └──┘  │  │  │  │     └──┘  │  │  │  │     │  └──┘  │  ┌──┘  │     ┌──┐  │  │ \n'
            ' ┌─────┘  │  │  └───────────┘  │  │  └─────┘  ┌─────┘  └──┐  └─────┘  └──┘  │ \n'
            ' └────────┘  └─────────────────┘  └───────────┘           └─────────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()