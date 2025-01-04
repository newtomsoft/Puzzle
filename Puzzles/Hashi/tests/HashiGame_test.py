import unittest
from unittest import TestCase

from Puzzles.Hashi.HashiGame import HashiGame
from Puzzles.Hashi.Island import Island
from Utils.Direction import Direction
from Utils.Position import Position


class HashiGameTests(TestCase):
    def setUp(self):
        Island._islands = {}

    def test_wrong_bridges(self):
        island_0_0 = Island(Position(0, 0), 1)
        island_0_1 = Island(Position(0, 1), 2)
        islands = {island_0_0.position: island_0_0, island_0_1.position: island_0_1}
        game = HashiGame(islands)
        solution = game.get_solution()
        self.assertEqual({}, solution)

    def test_solution_without_crossover(self):
        island_0_0 = Island(Position(0, 0), 1)
        island_0_1 = Island(Position(0, 1), 4)
        island_0_3 = Island(Position(0, 3), 3)
        island_1_2 = Island(Position(1, 2), 2)
        island_2_0 = Island(Position(2, 0), 1)
        island_2_2 = Island(Position(2, 2), 4)
        island_2_3 = Island(Position(2, 3), 4)
        island_3_1 = Island(Position(3, 1), 2)
        island_4_2 = Island(Position(4, 2), 1)
        island_5_0 = Island(Position(5, 0), 2)
        island_5_3 = Island(Position(5, 3), 2)
        islands = {
            island_0_0.position: island_0_0, island_0_1.position: island_0_1, island_0_3.position: island_0_3, island_1_2.position: island_1_2, island_2_0.position: island_2_0,
            island_2_2.position: island_2_2, island_2_3.position: island_2_3, island_3_1.position: island_3_1, island_4_2.position: island_4_2, island_5_0.position: island_5_0,
            island_5_3.position: island_5_3
        }

        game = HashiGame(islands)
        solution = game.get_solution()

        Island._islands = {}
        expected_island_0_0 = Island(Position(0, 0), 1)
        expected_island_0_1 = Island(Position(0, 1), 4)
        expected_island_0_3 = Island(Position(0, 3), 3)
        expected_island_1_2 = Island(Position(1, 2), 2)
        expected_island_2_0 = Island(Position(2, 0), 1)
        expected_island_2_2 = Island(Position(2, 2), 4)
        expected_island_2_3 = Island(Position(2, 3), 4)
        expected_island_3_1 = Island(Position(3, 1), 2)
        expected_island_4_2 = Island(Position(4, 2), 1)
        expected_island_5_0 = Island(Position(5, 0), 2)
        expected_island_5_3 = Island(Position(5, 3), 2)
        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 3), 1)
        expected_island_0_1.set_bridge(Position(3, 1), 2)
        expected_island_0_3.set_bridge(Position(0, 1), 1)
        expected_island_0_3.set_bridge(Position(2, 3), 2)
        expected_island_1_2.set_bridge(Position(2, 2), 2)
        expected_island_2_0.set_bridge(Position(5, 0), 1)
        expected_island_2_2.set_bridge(Position(1, 2), 2)
        expected_island_2_2.set_bridge(Position(2, 3), 1)
        expected_island_2_2.set_bridge(Position(4, 2), 1)
        expected_island_2_3.set_bridge(Position(0, 3), 2)
        expected_island_2_3.set_bridge(Position(2, 2), 1)
        expected_island_2_3.set_bridge(Position(5, 3), 1)
        expected_island_3_1.set_bridge(Position(0, 1), 2)
        expected_island_4_2.set_bridge(Position(2, 2), 1)
        expected_island_5_0.set_bridge(Position(2, 0), 1)
        expected_island_5_0.set_bridge(Position(5, 3), 1)
        expected_island_5_3.set_bridge(Position(2, 3), 1)
        expected_island_5_3.set_bridge(Position(5, 0), 1)

        self.assertEqual(expected_island_0_0, solution[Position(0, 0)])
        self.assertEqual(expected_island_0_1, solution[Position(0, 1)])
        self.assertEqual(expected_island_0_3, solution[Position(0, 3)])
        self.assertEqual(expected_island_1_2, solution[Position(1, 2)])
        self.assertEqual(expected_island_2_0, solution[Position(2, 0)])
        self.assertEqual(expected_island_2_2, solution[Position(2, 2)])
        self.assertEqual(expected_island_2_3, solution[Position(2, 3)])
        self.assertEqual(expected_island_3_1, solution[Position(3, 1)])
        self.assertEqual(expected_island_4_2, solution[Position(4, 2)])
        self.assertEqual(expected_island_5_0, solution[Position(5, 0)])
        self.assertEqual(expected_island_5_3, solution[Position(5, 3)])

        other_solution = game.get_other_solution()
        self.assertEqual({}, other_solution)

    def test_solution_with_possible_crossover(self):
        island_0_1 = Island(Position(0, 1), 1)
        island_0_2 = Island(Position(0, 2), 2)
        island_1_0 = Island(Position(1, 0), 3)
        island_1_2 = Island(Position(1, 2), 3)
        island_2_0 = Island(Position(2, 0), 3)
        island_2_1 = Island(Position(2, 1), 2)
        islands = {
            island_0_1.position: island_0_1, island_0_2.position: island_0_2, island_1_0.position: island_1_0, island_1_2.position: island_1_2,
            island_2_0.position: island_2_0, island_2_1.position: island_2_1
        }

        game = HashiGame(islands)
        solution = game.get_solution()

        Island._islands = {}

        not_expected_island_0_1 = Island(Position(0, 1), 1)
        not_expected_island_0_2 = Island(Position(0, 2), 2)
        not_expected_island_1_0 = Island(Position(1, 0), 3)
        not_expected_island_1_2 = Island(Position(1, 2), 3)
        not_expected_island_2_0 = Island(Position(2, 0), 3)
        not_expected_island_2_1 = Island(Position(2, 1), 2)

        not_expected_island_0_1.set_bridge(Position(2, 1), 1)
        not_expected_island_0_2.set_bridge(Position(1, 2), 2)
        not_expected_island_1_0.set_bridge(Position(1, 2), 1)
        not_expected_island_1_0.set_bridge(Position(2, 0), 2)
        not_expected_island_1_2.set_bridge(Position(0, 2), 2)
        not_expected_island_2_0.set_bridge(Position(1, 0), 2)
        not_expected_island_2_0.set_bridge(Position(2, 1), 1)
        not_expected_island_2_1.set_bridge(Position(0, 1), 1)

        self.assertEqual(not_expected_island_0_1, solution[Position(0, 1)])
        self.assertEqual(not_expected_island_0_2, solution[Position(0, 2)])
        self.assertEqual(not_expected_island_1_0, solution[Position(1, 0)])
        self.assertEqual(not_expected_island_1_2, solution[Position(1, 2)])
        self.assertEqual(not_expected_island_2_0, solution[Position(2, 0)])
        self.assertEqual(not_expected_island_2_1, solution[Position(2, 1)])

        other_solution = game.get_other_solution()

        Island._islands = {}
        expected_island_0_1 = Island(Position(0, 1), 1)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_1_0 = Island(Position(1, 0), 3)
        expected_island_1_2 = Island(Position(1, 2), 3)
        expected_island_2_0 = Island(Position(2, 0), 3)
        expected_island_2_1 = Island(Position(2, 1), 2)

        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_0_2.set_bridge(Position(1, 2), 1)
        expected_island_1_0.set_bridge(Position(1, 2), 2)
        expected_island_1_0.set_bridge(Position(2, 0), 1)
        expected_island_1_2.set_bridge(Position(1, 0), 2)
        expected_island_1_2.set_bridge(Position(0, 2), 1)
        expected_island_2_0.set_bridge(Position(1, 0), 1)
        expected_island_2_0.set_bridge(Position(2, 1), 2)
        expected_island_2_1.set_bridge(Position(2, 0), 2)

        self.assertEqual(expected_island_0_1, other_solution[Position(0, 1)])
        self.assertEqual(expected_island_0_2, other_solution[Position(0, 2)])
        self.assertEqual(expected_island_1_0, other_solution[Position(1, 0)])
        self.assertEqual(expected_island_1_2, other_solution[Position(1, 2)])
        self.assertEqual(expected_island_2_0, other_solution[Position(2, 0)])
        self.assertEqual(expected_island_2_1, other_solution[Position(2, 1)])






if __name__ == '__main__':
    unittest.main()