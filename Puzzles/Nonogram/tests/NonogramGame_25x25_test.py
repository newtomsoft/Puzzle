﻿import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Nonogram.NonogramGame import NonogramGame


class NonogramGameTests(TestCase):
    def test_solution_25x25(self):
        numbers_by_top_left = {
            'top': [[4, 2, 4], [3, 8, 1], [3, 3, 1, 2], [4, 4, 2], [4, 2], [5, 2, 2], [1, 1, 1, 5, 2, 1], [1, 1, 7, 1, 2, 2], [3, 7, 3, 3], [2, 9, 5, 2], [2, 8, 3, 2], [4, 6, 1, 2], [2, 1, 9, 4], [1, 3, 3, 4], [8, 5], [7], [9, 2], [1, 1, 2, 8], [6, 7, 3], [4, 5, 1, 3],
                    [4, 1, 1, 1, 1], [8, 3, 2], [7, 1, 6], [19], [3, 14]],
            'left': [[12], [6, 4, 1], [9, 2, 5], [1, 3, 3, 6], [1, 3, 7], [1, 1, 1, 8], [2, 4, 1, 4], [2, 5, 3, 1, 4], [1, 1, 6, 3, 3], [4, 6, 3, 2, 2], [4, 5, 1, 1, 4, 2], [4, 3, 1, 1, 5, 2], [1, 6, 1, 1, 2, 2], [4, 1, 4, 3], [4, 1, 3, 2], [1, 3, 5, 2],
                     [3, 1, 1, 3, 2], [3, 1, 1, 3, 2], [2, 3, 3, 3], [3, 2, 3, 4], [4, 4, 11], [8, 5, 2, 4], [1, 3, 3], [6, 2], [5, 2]],
        }
        expected_grid = Grid([
            [True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [True, True, True, True, True, True, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False],
            [True, True, True, True, True, True, True, True, True, False, False, True, True, False, False, False, False, False, True, True, True, True, True, False, False],
            [True, False, False, True, True, True, False, False, False, False, False, True, True, True, False, False, False, True, True, True, True, True, True, False, False],
            [False, True, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True],
            [False, True, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, True, True, True, True, True, True, True, True],
            [True, True, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, True, False, False, True, True, True, True],
            [True, True, False, False, False, False, True, True, True, True, True, False, True, True, True, False, False, False, True, False, True, True, True, True, False],
            [False, True, False, True, False, True, True, True, True, True, True, False, True, True, True, False, False, False, False, False, False, True, True, True, False],
            [True, True, True, True, False, True, True, True, True, True, True, False, True, True, True, False, False, False, True, True, False, False, False, True, True],
            [True, True, True, True, False, False, True, True, True, True, True, False, True, False, True, False, True, True, True, True, False, False, False, True, True],
            [True, True, True, True, False, False, False, False, True, True, True, False, True, False, True, False, True, True, True, True, True, False, False, True, True],
            [True, False, False, False, False, False, False, True, True, True, True, True, True, False, True, False, True, False, True, True, False, False, False, True, True],
            [False, False, False, False, False, False, False, False, False, True, True, True, True, False, True, False, True, True, True, True, False, False, True, True, True],
            [False, False, False, False, False, False, False, False, False, True, True, True, True, False, True, False, True, True, True, False, False, False, False, True, True],
            [False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, True, True, True, True, True, False, False, False, True, True],
            [False, False, False, False, False, False, True, True, True, False, False, True, False, True, False, True, True, True, False, False, False, False, False, True, True],
            [False, False, False, False, False, False, False, True, True, True, False, True, False, True, False, True, True, True, False, False, False, False, False, True, True],
            [False, True, True, False, False, False, False, False, True, True, True, False, False, False, False, True, True, True, False, False, False, False, True, True, True],
            [False, False, False, False, False, False, False, False, False, True, True, True, False, False, True, True, False, True, True, True, False, True, True, True, True],
            [False, False, True, True, True, True, False, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True],
            [False, False, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, False, True, True, False, True, True, True, True],
            [False, False, False, False, False, False, False, False, True, False, False, False, True, True, True, False, False, False, False, False, False, False, True, True, True],
            [False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, True, True, False, False],
            [False, False, False, False, False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, True, True, False, False, False],
        ])
        game = NonogramGame(numbers_by_top_left)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()