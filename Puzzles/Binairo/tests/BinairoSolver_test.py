﻿import unittest
from unittest import TestCase

from Puzzles.Binairo.BinairoSolver import BinairoSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class BinairoSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_too_small(self):
        grid = Grid([
            [-1, -1, -1, -1, -1],
            [-1, -1, 0, -1, 0],
            [1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [0, 0, -1, -1, 0],
        ])

        with self.assertRaises(ValueError) as context:
            BinairoSolver(grid, self.get_solver_engine())

        self.assertEqual("Binairo grid must be at least 6x6", str(context.exception))

    def test_solution_not_even_size_column(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, 0, -1],
            [-1, -1, 0, -1, 0, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [0, 0, -1, -1, 0, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
        ])
        with self.assertRaises(ValueError) as context:
            BinairoSolver(grid, self.get_solver_engine())

        self.assertEqual("Binairo grid must have an even number of rows/columns", str(context.exception))

    def test_solution_not_even_size_row(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, 0],
            [-1, -1, 0, -1, 0, -1],
            [1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [0, 0, -1, -1, 0, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        with self.assertRaises(ValueError) as context:
            BinairoSolver(grid, self.get_solver_engine())

        self.assertEqual("Binairo grid must have an even number of rows/columns", str(context.exception))

    def test_solution_using_only_initial_constraint(self):
        grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
        ])
        expected_grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_using_initial_constraint_and_count(self):
        grid = Grid([
            [-1, 1, 1, 0, 0, -1],
            [0, -1, 1, 0, -1, 0],
            [1, 0, -1, -1, 1, 0],
            [1, 0, -1, -1, 0, 1],
            [0, -1, 0, 1, -1, 0],
            [-1, 0, 0, 1, 0, -1],
        ])
        expected_grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_using_initial_constraint_and_count_and_unique_row(self):
        grid = Grid([
            [-1, 1, 1, 0, 0, 1],
            [-1, 1, 1, 0, 0, 1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertTrue(solution.is_empty())

    def test_solution_using_initial_constraint_and_count_and_unique_column(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [0, 0, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
            [0, 0, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertTrue(solution.is_empty())

    def test_solution_using_initial_constraint_and_count_and_unique(self):
        grid = Grid([
            [1, 0, 1, 0, 1, -1],
            [0, 1, 0, 1, -1, 1],
            [-1, 0, 1, 0, -1, -1],
            [0, 1, -1, -1, 1, -1],
            [1, 0, -1, -1, 0, -1],
            [-1, -1, 0, 1, -1, -1],
        ])
        expected_grid = Grid([
            [1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_using_all_constraints_adjacent_row(self):
        grid = Grid([
            [0, 0, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertTrue(solution.is_empty())

    def test_solution_using_all_constraints_adjacent_column(self):
        grid = Grid([
            [0, -1, -1, -1, -1, -1],
            [0, -1, -1, -1, -1, -1],
            [0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertTrue(solution.is_empty())

    def test_solution_6x6(self):
        grid = Grid([
            [0, -1, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, 0, -1, 0, 0, -1],
            [0, -1, -1, -1, -1, -1],
            [-1, -1, 0, 0, -1, -1],
            [-1, -1, -1, -1, 1, -1],
        ])
        expected_grid = Grid([
            [0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, 1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 1, -1, 1, -1, 0],
            [1, -1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, 0, 0, -1, -1, -1],
            [-1, -1, 0, 0, -1, -1, 0, -1],
        ])
        expected_grid = Grid([
            [1, 0, 1, 1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 0, 1, 1, 0, 1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10(self):
        grid = Grid([
            [0, 0, 1, 0, 1, 0, 1, -1, -1, 1],
            [-1, -1, 0, 1, 0, 1, -1, -1, 1, 0],
            [-1, -1, 1, 0, 1, 0, 0, 1, 0, 1],
            [-1, -1, 0, 1, -1, -1, 1, 0, 1, 0],
            [1, -1, -1, 0, -1, -1, -1, -1, -1, 0],
            [-1, 0, -1, -1, 1, -1, -1, 1, 0, 1],
            [-1, -1, -1, -1, -1, 1, -1, 0, 1, 0],
            [-1, 1, -1, -1, -1, -1, -1, 0, 1, 0],
            [0, -1, -1, -1, -1, -1, -1, 1, 0, 1],
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, 1],
        ])
        expected_grid = Grid([
            [0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
        ])
        game_solver = BinairoSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
