import unittest
from unittest import TestCase

from SolverEngine.Z3SolverEngine import Z3SolverEngine

from Puzzles.Hashi.HashiSolver import HashiSolver
from Utils.Grid import Grid
from Utils.Island import Island
from Utils.IslandsGrid import IslandGrid
from Utils.Position import Position


class HashiSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_wrong_bridges(self):
        grid = Grid([
            [1, 2]
        ])
        game_solver = HashiSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(IslandGrid.empty(), solution)

    def test_solution_without_crossover(self):
        grid = Grid([
            [1, 4, 0, 3],
            [0, 0, 2, 0],
            [1, 0, 4, 4],
            [0, 2, 0, 0],
            [0, 0, 1, 0],
            [2, 0, 0, 2]
        ])
        game_solver = HashiSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()

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
        expected_island_0_0.set_bridge(Position(2, 0), 0)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(0, 3), 1)
        expected_island_0_1.set_bridge(Position(3, 1), 2)
        expected_island_0_3.set_bridge(Position(0, 1), 1)
        expected_island_0_3.set_bridge(Position(2, 3), 2)
        expected_island_1_2.set_bridge(Position(2, 2), 2)
        expected_island_2_0.set_bridge(Position(5, 0), 1)
        expected_island_2_0.set_bridge(Position(0, 0), 0)
        expected_island_2_0.set_bridge(Position(2, 2), 0)
        expected_island_2_2.set_bridge(Position(1, 2), 2)
        expected_island_2_2.set_bridge(Position(2, 3), 1)
        expected_island_2_2.set_bridge(Position(4, 2), 1)
        expected_island_2_2.set_bridge(Position(2, 0), 0)
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

        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_possible_crossover(self):
        grid = Grid([
            [0, 1, 2],
            [3, 0, 3],
            [3, 2, 0]
        ])
        game_solver = HashiSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()

        expected_island_0_1 = Island(Position(0, 1), 1)
        expected_island_0_2 = Island(Position(0, 2), 2)
        expected_island_1_0 = Island(Position(1, 0), 3)
        expected_island_1_2 = Island(Position(1, 2), 3)
        expected_island_2_0 = Island(Position(2, 0), 3)
        expected_island_2_1 = Island(Position(2, 1), 2)

        expected_island_0_1.set_bridge(Position(0, 2), 1)
        expected_island_0_1.set_bridge(Position(2, 1), 0)
        expected_island_0_2.set_bridge(Position(0, 1), 1)
        expected_island_0_2.set_bridge(Position(1, 2), 1)
        expected_island_1_0.set_bridge(Position(1, 2), 2)
        expected_island_1_0.set_bridge(Position(2, 0), 1)
        expected_island_1_2.set_bridge(Position(1, 0), 2)
        expected_island_1_2.set_bridge(Position(0, 2), 1)
        expected_island_2_0.set_bridge(Position(1, 0), 1)
        expected_island_2_0.set_bridge(Position(2, 1), 2)
        expected_island_2_1.set_bridge(Position(2, 0), 2)
        expected_island_2_1.set_bridge(Position(0, 1), 0)

        self.assertEqual(expected_island_0_1, solution[Position(0, 1)])
        self.assertEqual(expected_island_0_2, solution[Position(0, 2)])
        self.assertEqual(expected_island_1_0, solution[Position(1, 0)])
        self.assertEqual(expected_island_1_2, solution[Position(1, 2)])
        self.assertEqual(expected_island_2_0, solution[Position(2, 0)])
        self.assertEqual(expected_island_2_1, solution[Position(2, 1)])

        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_possible_isolated_islands(self):
        grid = Grid([
            [1, 2],
            [1, 2]
        ])
        game_solver = HashiSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()

        expected_island_0_0 = Island(Position(0, 0), 1)
        expected_island_0_1 = Island(Position(0, 1), 2)
        expected_island_1_0 = Island(Position(1, 0), 1)
        expected_island_1_1 = Island(Position(1, 1), 2)

        expected_island_0_0.set_bridge(Position(0, 1), 1)
        expected_island_0_0.set_bridge(Position(1, 0), 0)
        expected_island_0_1.set_bridge(Position(0, 0), 1)
        expected_island_0_1.set_bridge(Position(1, 1), 1)
        expected_island_1_0.set_bridge(Position(1, 1), 1)
        expected_island_1_0.set_bridge(Position(0, 0), 0)
        expected_island_1_1.set_bridge(Position(1, 0), 1)
        expected_island_1_1.set_bridge(Position(0, 1), 1)

        self.assertEqual(expected_island_0_0, solution[Position(0, 0)])
        self.assertEqual(expected_island_0_1, solution[Position(0, 1)])
        self.assertEqual(expected_island_1_0, solution[Position(1, 0)])
        self.assertEqual(expected_island_1_1, solution[Position(1, 1)])

        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_possible_isolated_islands_10x10(self):
        grid = Grid([
            [3, 0, 4, 0, 0, 3, 0, 0, 0, 3],
            [0, 0, 0, 0, 2, 0, 1, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 3],
            [3, 0, 0, 0, 0, 0, 1, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 4, 0, 4, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 4, 0, 0, 2, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 3]
        ])
        game_solver = HashiSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()

        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
