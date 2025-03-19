﻿import unittest
from unittest import TestCase

from Pipes.Pipe import Pipe, PipeString
from Pipes.PipesSolver import PipesSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class PipesSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_grid1x2(self):
        matrix: list[list[PipeString]] = [
            ['E1', 'E1'],
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶──╴ '
        )

        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid1x3(self):
        matrix: list[list[PipeString]] = [
            ['E1', 'I1', 'E1']
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶─────╴ '
        )

        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid2x2(self):
        matrix: list[list[PipeString]] = [
            ['E1', 'L1'],
            ['E1', 'L1'],
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶──┐ \n'
            ' ╶──┘ '
        )

        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid4x4(self):
        matrix: list[list[PipeString]] = [
            ['E3', 'I2', 'L1', 'E0'],
            ['E2', 'T1', 'T0', 'I3'],
            ['E1', 'L0', 'T3', 'L2'],
            ['E0', 'I3', 'T2', 'E1'],
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶─────┐  ╷ \n'
            ' ╶──┬──┤  │ \n'
            ' ╶──┘  ├──┘ \n'
            ' ╶─────┴──╴ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid5x5(self):
        matrix: list[list[PipeString]] = [
            ['E1', 'L1', 'E1', 'L1', 'E1'],
            ['I1', 'I1', 'E1', 'T1', 'E1'],
            ['L1', 'T1', 'T1', 'T1', 'T1'],
            ['E1', 'E1', 'I1', 'E1', 'T1'],
            ['L1', 'T1', 'T1', 'E1', 'E1'],
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╷  ┌──╴  ┌──╴ \n'
            ' │  │  ╶──┤  ╷ \n'
            ' └──┴──┬──┴──┤ \n'
            ' ╷  ╷  │  ╶──┤ \n'
            ' └──┴──┴──╴  ╵ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid7x7(self):
        matrix: list[list[PipeString]] = [
            ['E1', 'E1', 'E1', 'L1', 'L1', 'I1', 'E1'],
            ['I1', 'I1', 'L1', 'L1', 'T1', 'I1', 'L1'],
            ['T1', 'T1', 'T1', 'T1', 'T1', 'E1', 'E1'],
            ['L1', 'E1', 'L1', 'L1', 'L1', 'T1', 'E1'],
            ['E1', 'I1', 'T1', 'E1', 'E1', 'E1', 'E1'],
            ['E1', 'L1', 'T1', 'T1', 'T1', 'T1', 'T1'],
            ['E1', 'T1', 'T1', 'I1', 'I1', 'E1', 'E1'],
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╷  ╷  ╶──┐  ┌─────╴ \n'
            ' │  │  ┌──┘  ├─────┐ \n'
            ' ├──┴──┴──┬──┤  ╷  ╵ \n'
            ' └──╴  ┌──┘  └──┴──╴ \n'
            ' ╶─────┤  ╷  ╷  ╷  ╷ \n'
            ' ╶──┐  ├──┴──┴──┴──┤ \n'
            ' ╶──┴──┴────────╴  ╵ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid7x7_2(self):
        # loop and some isolated cells
        matrix: list[list[PipeString]] = [
            ['E1', 'E1', 'I1', 'I1', 'I1', 'T1', 'L1'],
            ['T1', 'T1', 'E1', 'E1', 'I1', 'T1', 'E1'],
            ['E1', 'I1', 'E1', 'L1', 'E1', 'T1', 'L1'],
            ['E1', 'T1', 'T1', 'T1', 'T1', 'T1', 'E1'],
            ['E1', 'T1', 'I1', 'T1', 'L1', 'L1', 'E1'],
            ['E1', 'L1', 'L1', 'T1', 'T1', 'I1', 'L1'],
            ['E1', 'I1', 'L1', 'E1', 'T1', 'E1', 'E1'],
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╷  ╶───────────┬──┐ \n'
            ' ├──┬──╴  ╶─────┤  ╵ \n'
            ' ╵  │  ╷  ┌──╴  ├──┐ \n'
            ' ╶──┴──┴──┴──┬──┤  ╵ \n'
            ' ╶──┬─────┬──┘  └──╴ \n'
            ' ╶──┘  ┌──┴──┬─────┐ \n'
            ' ╶─────┘  ╶──┴──╴  ╵ '
        )

        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid10x10(self):
        matrix: list[list[PipeString]] = [
            ['E0', 'I0', 'I1', 'I1', 'I1', 'L1', 'E1', 'E2', 'E2', 'E2'],
            ['E0', 'E3', 'L0', 'L0', 'E0', 'I0', 'I0', 'T3', 'L0', 'I1'],
            ['I0', 'E3', 'I1', 'I1', 'L3', 'L0', 'I0', 'L1', 'T1', 'T3'],
            ['I1', 'L1', 'T1', 'T1', 'T0', 'E0', 'T0', 'E2', 'T1', 'E3'],
            ['T0', 'E3', 'E1', 'E3', 'T2', 'T3', 'L1', 'E2', 'T2', 'E1'],
            ['I0', 'E3', 'T0', 'E0', 'E1', 'T1', 'I0', 'I0', 'T1', 'I1'],
            ['T1', 'E3', 'T1', 'L1', 'L1', 'T0', 'L0', 'E2', 'T0', 'L1'],
            ['L3', 'T3', 'T2', 'T1', 'T0', 'T0', 'T1', 'T2', 'L2', 'L2'],
            ['E1', 'T1', 'E2', 'I1', 'I1', 'E0', 'L2', 'T1', 'L0', 'E2'],
            ['E1', 'L0', 'L1', 'L1', 'L2', 'E3', 'E3', 'E0', 'T1', 'E1']
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶──────────────┐  ╷  ╷  ╷  ╷ \n'
            ' ╷  ╶──┐  ┌──╴  │  │  ├──┘  │ \n'
            ' │  ╷  │  │  ┌──┘  │  └──┬──┤ \n'
            ' │  └──┴──┴──┤  ╶──┤  ╶──┤  ╵ \n'
            ' ├──╴  ╷  ╶──┴──┬──┘  ╶──┤  ╷ \n'
            ' │  ╶──┤  ╷  ╷  ├────────┤  │ \n'
            ' ├──╴  ├──┘  └──┴──┐  ╷  ├──┘ \n'
            ' └──┬──┴──┬──┬──┬──┴──┤  └──┐ \n'
            ' ╶──┤  ╷  │  │  ╵  ┌──┴──┐  ╵ \n'
            ' ╶──┘  └──┘  └──╴  ╵  ╶──┴──╴ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid15x15(self):
        matrix: list[list[PipeString]] = [
            ['E2', 'L3', 'T3', 'T2', 'I0', 'T0', 'L2', 'E3', 'L3', 'E2', 'L2', 'L0', 'I1', 'E1', 'E0'],
            ['T2', 'T0', 'I1', 'T2', 'E0', 'E2', 'I1', 'L3', 'L1', 'E0', 'I1', 'I0', 'E1', 'L1', 'L0'],
            ['E1', 'E2', 'E0', 'I0', 'E1', 'E2', 'I0', 'T3', 'I0', 'L0', 'T2', 'T2', 'T1', 'T1', 'E3'],
            ['E1', 'E1', 'E0', 'T0', 'L1', 'L2', 'T1', 'L3', 'I1', 'L3', 'T3', 'E1', 'E2', 'T2', 'I1'],
            ['L3', 'T3', 'I0', 'I1', 'I0', 'L3', 'L2', 'T3', 'E2', 'L2', 'T1', 'E2', 'I1', 'T1', 'L3'],
            ['L1', 'T1', 'E2', 'E2', 'E2', 'I1', 'E2', 'T0', 'L2', 'L0', 'T3', 'T3', 'T0', 'T1', 'E1'],
            ['E0', 'I1', 'E1', 'T1', 'L3', 'T1', 'E1', 'T0', 'T3', 'T3', 'E0', 'L2', 'E0', 'L1', 'E0'],
            ['E1', 'T1', 'T1', 'T1', 'E1', 'T0', 'T2', 'T0', 'L1', 'L1', 'E0', 'E3', 'L2', 'E0', 'E0'],
            ['E3', 'I0', 'L3', 'T1', 'L0', 'E1', 'T0', 'L1', 'E0', 'E1', 'T3', 'T1', 'T3', 'L0', 'L1'],
            ['E0', 'E1', 'L3', 'T1', 'E0', 'L2', 'T1', 'T1', 'I1', 'I1', 'T1', 'L1', 'T2', 'T3', 'L2'],
            ['L2', 'I1', 'T1', 'T1', 'T1', 'L2', 'I0', 'T3', 'I1', 'I1', 'E3', 'E3', 'E3', 'E2', 'L3'],
            ['E0', 'T3', 'T0', 'T3', 'T3', 'L1', 'L1', 'T1', 'T3', 'I0', 'I0', 'T2', 'I1', 'I1', 'E1'],
            ['E0', 'T2', 'I0', 'I1', 'E2', 'L3', 'L1', 'I1', 'L3', 'I1', 'E3', 'I1', 'L1', 'E0', 'E0'],
            ['L2', 'L1', 'I0', 'T0', 'E3', 'L3', 'T3', 'L1', 'E2', 'E2', 'E2', 'T0', 'T2', 'L0', 'L3'],
            ['E2', 'E0', 'L1', 'L1', 'E2', 'E0', 'L1', 'I1', 'I0', 'T0', 'E1', 'E2', 'T2', 'T2', 'E2']
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╷  ┌──┬──┬─────┬──┐  ╶──┐  ╶──┐  ┌─────╴  ╷ \n'
            ' ├──┤  │  ├──╴  ╵  │  ┌──┘  ╷  │  │  ╷  ┌──┘ \n'
            ' ╵  ╵  ╵  │  ╷  ╷  │  ├─────┘  ├──┴──┴──┤  ╷ \n'
            ' ╷  ╷  ╶──┴──┘  └──┤  └─────┐  ├──╴  ╶──┤  │ \n'
            ' └──┴───────────┐  └──┬──╴  └──┤  ╶─────┴──┘ \n'
            ' ┌──┬──╴  ╷  ╷  │  ╶──┴──┐  ┌──┴──┬──┬──┬──╴ \n'
            ' ╵  │  ╶──┤  └──┤  ╶──┬──┴──┤  ╶──┘  ╵  └──╴ \n'
            ' ╶──┴──┬──┤  ╷  ├──┬──┴──┐  └──╴  ╷  ┌──╴  ╷ \n'
            ' ╶─────┘  ├──┘  ╵  ├──┐  ╵  ╶──┬──┴──┤  ┌──┘ \n'
            ' ╷  ╶──┐  ├──╴  ┌──┤  ├────────┴──┐  ├──┴──┐ \n'
            ' └─────┴──┴──┬──┘  │  ├────────╴  ╵  ╵  ╶──┘ \n'
            ' ╶──┬──┬──┬──┤  ┌──┘  ├──┬────────┬────────╴ \n'
            ' ╶──┤  │  │  ╵  └──┐  │  └─────╴  │  ┌──╴  ╷ \n'
            ' ┌──┘  │  ├──╴  ┌──┤  └──╴  ╷  ╶──┴──┤  ┌──┘ \n'
            ' ╵  ╶──┘  └──╴  ╵  └────────┴──╴  ╶──┴──┴──╴ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid15x15_from_repr(self):
        matrix = [
            [' ╷ ', ' ├─', '─┘ ', ' ┌─', '─┴─', ' ╷ ', ' ╶─', ' ╵ ', ' ╷ ', ' ├─', ' ╶─', ' └─', ' ├─', ' │ ', '─╴ '],
            [' ╵ ', '─╴ ', '─┬─', ' └─', ' ╷ ', '─╴ ', '─┘ ', '─┬─', '─┤ ', '─┴─', ' ╶─', '───', ' └─', ' │ ', ' └─'],
            ['─┘ ', '─┤ ', ' ├─', '───', '─┴─', '─┐ ', ' ╵ ', ' ╶─', '─┐ ', ' │ ', '─┘ ', ' │ ', ' ╶─', ' └─', ' ╵ '],
            [' └─', ' ├─', ' ╶─', ' ┌─', '───', ' ╷ ', '─┤ ', '─┬─', ' ╵ ', '─┴─', '─┬─', '─┤ ', '─╴ ', '───', ' ╵ '],
            ['─╴ ', ' ┌─', ' ╵ ', ' ┌─', '─┤ ', '───', ' ╷ ', '─┤ ', ' ╶─', '─┤ ', '─┬─', ' ├─', ' │ ', '─┘ ', '───'],
            [' └─', ' │ ', '─┬─', '───', '─┤ ', '─┬─', '─╴ ', '─┤ ', ' ╷ ', '───', ' │ ', '─┴─', '─┤ ', '───', '─┬─'],
            [' ╶─', ' ╵ ', '─┤ ', ' ╵ ', '───', ' ├─', '───', ' ├─', '───', '─┬─', ' ╷ ', ' │ ', ' └─', '─┘ ', '───'],
            [' ╷ ', '───', '─┘ ', ' ╷ ', '─╴ ', '─┤ ', '─┴─', '─┤ ', ' ╷ ', '─┘ ', ' ╷ ', ' │ ', '─┐ ', ' ├─', '─╴ '],
            [' ╷ ', ' ╷ ', '─┬─', ' ├─', '─┴─', '─┴─', '─┬─', '───', '─┘ ', '─┘ ', ' └─', ' ╷ ', ' ╶─', '─┴─', ' └─'],
            ['───', '─╴ ', ' ╷ ', '─┘ ', '─┬─', '─┴─', ' ┌─', ' └─', '─┤ ', '─┤ ', ' ╵ ', ' ╷ ', ' ╷ ', ' │ ', ' ╶─'],
            [' └─', '─┤ ', ' │ ', ' ┌─', ' ╵ ', '─┤ ', '─╴ ', '───', ' │ ', '─┤ ', ' │ ', '─┤ ', ' │ ', '─┤ ', '─╴ '],
            ['─┐ ', '─┐ ', '─╴ ', '─┬─', '─┴─', '─┤ ', '─┬─', '─╴ ', '─╴ ', '───', ' ╶─', ' ├─', ' ├─', ' └─', '─╴ '],
            [' ╷ ', '─┴─', '─┘ ', '───', '─┤ ', '─┐ ', '─┬─', ' ├─', '─╴ ', ' │ ', '───', ' ╶─', ' ╵ ', ' └─', ' ╷ '],
            [' ╶─', '─┐ ', ' ├─', '─┬─', ' ╷ ', '───', ' ╵ ', '─┬─', '─┘ ', ' │ ', '─┴─', '───', ' ├─', '─┬─', ' ╷ '],
            [' ╵ ', '───', '─┐ ', ' ╶─', ' ╶─', '─┬─', ' ╷ ', ' ╵ ', '─╴ ', ' ┌─', '─┐ ', '─╴ ', ' └─', ' ┌─', '─┐ '],

        ]
        grid = Grid([[Pipe.from_repr(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶──┬──┐  ┌──┬──╴  ╷  ╷  ╶──┬──╴  ┌──┬─────╴ \n'
            ' ╷  ╵  ├──┘  ╵  ╷  └──┴──┬──┴──╴  │  └─────┐ \n'
            ' └──┬──┴─────┬──┘  ╷  ╷  └─────┐  │  ╶──┐  ╵ \n'
            ' ┌──┤  ╶──┐  │  ╷  ├──┤  ╶──┬──┴──┴──╴  │  ╷ \n'
            ' ╵  └──╴  └──┤  │  ╵  ├──╴  ├──┬──┬─────┘  │ \n'
            ' ┌─────┬─────┴──┤  ╷  ├──╴  │  │  ├──┬─────┤ \n'
            ' ╵  ╶──┤  ╶─────┤  │  ├─────┤  ╵  │  └──┐  │ \n'
            ' ╶─────┘  ╷  ╷  ├──┴──┴──╴  └──╴  │  ┌──┤  ╵ \n'
            ' ╷  ╶──┬──┴──┤  ├──┬─────┐  ┌──┐  ╵  ╵  ├──┐ \n'
            ' │  ╷  ╵  ┌──┴──┤  └──┐  ├──┤  ╵  ╷  ╷  │  ╵ \n'
            ' └──┴─────┘  ╶──┤  ╷  │  │  ├─────┤  │  ├──╴ \n'
            ' ┌──┐  ╶──┬──┬──┴──┤  ╵  ╵  │  ╷  ├──┤  └──╴ \n'
            ' ╵  ├──┐  │  ├──┐  ├──┬──╴  │  │  ╵  ╵  ┌──╴ \n'
            ' ╶──┘  ├──┤  ╵  │  ╵  ├──┐  │  ├─────┬──┤  ╷ \n'
            ' ╶─────┘  ╵  ╶──┴──╴  ╵  ╵  └──┘  ╶──┘  └──┘ ')
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid20x20(self):
        matrix: list[list[PipeString]] = [
            ['E3', 'E0', 'E3', 'T3', 'E2', 'E2', 'E1', 'E1', 'L1', 'E0', 'L1', 'T1', 'I0', 'E2', 'E3', 'T3', 'E1', 'L2', 'T2', 'E3'],
            ['T3', 'L1', 'E3', 'T0', 'I1', 'L0', 'L1', 'T2', 'I0', 'E3', 'E3', 'T3', 'T0', 'T3', 'E1', 'T1', 'I1', 'T1', 'E0', 'E0'],
            ['I1', 'E0', 'T3', 'T3', 'E3', 'E2', 'E0', 'T1', 'L0', 'T1', 'T1', 'L2', 'E2', 'E2', 'E0', 'I1', 'E1', 'L2', 'E2', 'I1'],
            ['L1', 'L3', 'E2', 'T3', 'L1', 'L1', 'T1', 'T3', 'T0', 'I0', 'L2', 'E0', 'L2', 'T1', 'T3', 'L1', 'T2', 'T0', 'I0', 'T1'],
            ['L2', 'T2', 'I0', 'T3', 'E3', 'E1', 'E2', 'E2', 'T0', 'L2', 'E0', 'I0', 'E1', 'I1', 'L1', 'E0', 'I1', 'E2', 'E2', 'E2'],
            ['I0', 'L1', 'T3', 'L3', 'T1', 'L1', 'E2', 'E3', 'I1', 'L3', 'L0', 'T2', 'E3', 'T3', 'L3', 'E2', 'T3', 'I0', 'L1', 'E3'],
            ['E0', 'E3', 'T0', 'L3', 'I0', 'L1', 'L0', 'I0', 'L2', 'T3', 'L2', 'T2', 'E0', 'T3', 'E0', 'T3', 'L2', 'E1', 'T0', 'T1'],
            ['L1', 'I1', 'T3', 'T0', 'T3', 'T3', 'E3', 'T1', 'I1', 'T2', 'T0', 'L1', 'E0', 'L2', 'L3', 'I1', 'E2', 'L3', 'I0', 'E0'],
            ['L2', 'E0', 'E1', 'L3', 'T0', 'T0', 'T3', 'I0', 'I1', 'L3', 'T0', 'E2', 'T2', 'L1', 'T2', 'L1', 'E2', 'T2', 'T3', 'E3'],
            ['E1', 'I1', 'I1', 'L2', 'E3', 'E1', 'T3', 'E2', 'E3', 'L1', 'T2', 'E2', 'T1', 'E3', 'T0', 'L0', 'T0', 'L0', 'L2', 'E0'],
            ['E0', 'L3', 'E3', 'L1', 'T1', 'L3', 'E2', 'E1', 'T1', 'T2', 'T0', 'L3', 'T1', 'T0', 'T2', 'L3', 'T1', 'I0', 'T3', 'L3'],
            ['E1', 'T0', 'T3', 'L2', 'I0', 'T0', 'T0', 'L3', 'L0', 'I0', 'I0', 'T3', 'E3', 'I1', 'L0', 'T2', 'I1', 'T0', 'E2', 'I1'],
            ['T2', 'T3', 'L1', 'E0', 'L2', 'I0', 'L3', 'I1', 'T0', 'T2', 'T2', 'T0', 'L1', 'T0', 'E0', 'L3', 'L1', 'L2', 'L3', 'I1'],
            ['E1', 'E0', 'L2', 'E3', 'L1', 'T2', 'L3', 'I1', 'T0', 'I1', 'T0', 'L1', 'E2', 'L2', 'E1', 'E2', 'L1', 'E3', 'I1', 'I1'],
            ['E3', 'T0', 'L0', 'I1', 'L1', 'E2', 'E2', 'L0', 'T0', 'E3', 'I1', 'T2', 'I1', 'I0', 'T3', 'L2', 'L0', 'L0', 'I0', 'E3'],
            ['L1', 'T2', 'L0', 'E0', 'I0', 'I1', 'I0', 'T1', 'L0', 'L3', 'E0', 'L3', 'L2', 'E2', 'L3', 'T2', 'T3', 'E1', 'L3', 'L3'],
            ['E3', 'L3', 'T1', 'I1', 'L3', 'L0', 'T1', 'L1', 'L2', 'T0', 'T1', 'L2', 'I1', 'T3', 'L0', 'E0', 'L2', 'T1', 'L3', 'I1'],
            ['E1', 'L0', 'I0', 'L0', 'T3', 'T0', 'L2', 'E2', 'T2', 'E1', 'E2', 'E3', 'L3', 'T0', 'L2', 'T1', 'L0', 'E0', 'E0', 'I1'],
            ['E1', 'T2', 'L1', 'T0', 'L3', 'T0', 'L3', 'E3', 'T2', 'T0', 'T2', 'T3', 'E1', 'T3', 'E2', 'I1', 'T0', 'I1', 'L2', 'E3'],
            ['E3', 'L3', 'E1', 'L3', 'E1', 'E3', 'E1', 'L1', 'L0', 'E2', 'E0', 'L3', 'E1', 'L1', 'E3', 'E3', 'L3', 'E1', 'L2', 'E1']
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╷  ╷  ╶──┬──╴  ╷  ╷  ╷  ┌──╴  ┌──┬─────╴  ╶──┬──╴  ┌──┬──╴ \n'
            ' ├──┘  ╷  ├─────┘  └──┤  │  ╷  ╵  ├──┬──┬──╴  ├─────┤  ╵  ╷ \n'
            ' │  ╶──┴──┤  ╷  ╷  ╶──┤  └──┴──┬──┘  ╵  ╵  ╷  │  ╷  └──╴  │ \n'
            ' └──┐  ╷  ├──┘  └──┬──┴──┬─────┘  ╷  ┌──┬──┴──┘  ├──┬─────┤ \n'
            ' ┌──┤  │  ├──╴  ╷  ╵  ╶──┤  ┌──╴  │  ╵  │  ┌──╴  │  ╵  ╷  ╵ \n'
            ' │  └──┤  └──┬──┘  ╷  ╷  │  └──┐  ├──╴  ├──┘  ╷  ├─────┘  ╷ \n'
            ' ╵  ╶──┴──┐  │  ┌──┘  │  └──┬──┘  ├──╴  ├──╴  ├──┘  ╶──┬──┤ \n'
            ' ┌─────┬──┴──┴──┤  ╶──┴─────┴──┬──┘  ╷  └──┐  │  ╶──┐  │  ╵ \n'
            ' └──╴  ╵  ┌──┬──┴──┬────────┐  ├──╴  ├──┐  ├──┘  ╷  ├──┴──╴ \n'
            ' ╶────────┘  ╵  ╶──┴──╴  ╷  └──┤  ╶──┤  ╵  ├──┐  ├──┘  ┌──╴ \n'
            ' ╶──┐  ╷  ┌──┬──┐  ╷  ╷  ├──┬──┤  ┌──┴──┬──┤  └──┴─────┴──┐ \n'
            ' ╷  ├──┴──┘  │  ├──┤  └──┘  │  │  ├──╴  │  └──┬─────┬──╴  │ \n'
            ' ├──┴──┐  ╶──┘  │  └─────┬──┤  ├──┴──┐  ├──╴  └──┐  └──┐  │ \n'
            ' ╵  ╷  └──╴  ┌──┤  ┌─────┤  │  ├──┐  ╵  └──╴  ╷  └──╴  │  │ \n'
            ' ╶──┤  ┌─────┘  ╵  ╵  ┌──┤  ╵  │  ├────────┬──┘  ┌──┐  │  ╵ \n'
            ' ┌──┴──┘  ╶───────────┤  └──┐  ╵  └──┐  ╷  └──┬──┤  ╵  └──┐ \n'
            ' ╵  ┌──┬─────┐  ┌──┬──┘  ┌──┴──┬──┐  │  ├──┐  ╵  └──┬──┐  │ \n'
            ' ╶──┘  │  ┌──┴──┤  └──╴  ├──╴  ╵  ╵  └──┤  └──┬──┐  ╵  ╵  │ \n'
            ' ╶──┬──┘  ├──┐  ├──┐  ╷  ├──┬──┬──┬──╴  ├──╴  │  ├─────┐  ╵ \n'
            ' ╶──┘  ╶──┘  ╵  ╵  ╵  └──┘  ╵  ╵  └──╴  └──╴  ╵  └──╴  └──╴ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid25x25(self):
        matrix: list[list[PipeString]] = [
            ['E2', 'L3', 'E0', 'E0', 'L2', 'E0', 'E0', 'I1', 'L2', 'E1', 'T1', 'E2', 'E1', 'L1', 'E3', 'E3', 'T0', 'E0', 'L2', 'I0', 'E1', 'E2', 'E0', 'E1', 'E3'],
            ['T2', 'L2', 'E3', 'E2', 'T2', 'L2', 'T2', 'T2', 'T0', 'E1', 'T0', 'E2', 'T3', 'T1', 'E1', 'E0', 'T3', 'E3', 'I0', 'E0', 'E2', 'T0', 'I1', 'T0', 'L3'],
            ['T1', 'E0', 'T2', 'E1', 'T1', 'I0', 'L3', 'E2', 'T3', 'L1', 'T1', 'E2', 'E2', 'T1', 'T2', 'E3', 'T1', 'T2', 'T3', 'I0', 'E2', 'T2', 'T0', 'L3', 'E2'],
            ['L1', 'T1', 'L2', 'E3', 'L0', 'E1', 'T1', 'E2', 'E3', 'I1', 'I1', 'E2', 'E1', 'I1', 'T1', 'T1', 'I0', 'E2', 'L3', 'T3', 'L3', 'I0', 'E1', 'E3', 'I1'],
            ['E1', 'T0', 'T0', 'I1', 'T1', 'E2', 'T1', 'E2', 'E0', 'T3', 'T3', 'L3', 'L3', 'E1', 'T1', 'T1', 'T0', 'T1', 'E0', 'L1', 'E1', 'T3', 'L1', 'T1', 'L0'],
            ['E1', 'E1', 'E3', 'L1', 'L3', 'E2', 'T1', 'E2', 'E0', 'L0', 'L3', 'T2', 'T0', 'E0', 'T3', 'L3', 'E1', 'I0', 'I0', 'L1', 'T2', 'T0', 'T1', 'T0', 'E1'],
            ['L2', 'T3', 'I1', 'T0', 'L0', 'I0', 'I1', 'E1', 'E1', 'T0', 'E1', 'T0', 'E0', 'E1', 'T2', 'E0', 'I1', 'T2', 'T1', 'L3', 'T1', 'E3', 'L2', 'I0', 'L3'],
            ['E3', 'E0', 'E0', 'E3', 'T3', 'L1', 'T1', 'T1', 'I0', 'T3', 'T3', 'T0', 'E0', 'L1', 'T3', 'E2', 'I0', 'E2', 'E0', 'I0', 'L1', 'T1', 'L2', 'E3', 'E0'],
            ['I0', 'L1', 'T2', 'T3', 'T1', 'I1', 'I0', 'L3', 'L3', 'E1', 'L2', 'T1', 'E3', 'T1', 'T2', 'T2', 'L2', 'L2', 'I0', 'T2', 'E1', 'I0', 'I1', 'E3', 'E3'],
            ['T1', 'E1', 'E2', 'T2', 'E3', 'E0', 'I0', 'T1', 'T0', 'L3', 'L1', 'T3', 'E3', 'T0', 'E0', 'L3', 'E2', 'T0', 'E0', 'T0', 'L1', 'L2', 'T0', 'T0', 'L3'],
            ['I0', 'E3', 'L2', 'E0', 'I1', 'T2', 'I0', 'I1', 'T1', 'T2', 'I0', 'T2', 'E0', 'T0', 'L2', 'T1', 'I0', 'T3', 'L0', 'L1', 'T2', 'I0', 'I0', 'I1', 'E1'],
            ['L0', 'T2', 'L0', 'E0', 'L0', 'L2', 'E3', 'I1', 'L2', 'E0', 'I0', 'T3', 'L2', 'L1', 'T2', 'T1', 'L1', 'E1', 'E3', 'E2', 'I0', 'E1', 'E3', 'E1', 'E3'],
            ['L0', 'T0', 'L0', 'I1', 'E1', 'E2', 'L0', 'E1', 'I1', 'I0', 'I1', 'I0', 'T1', 'T1', 'T1', 'E2', 'E3', 'T0', 'T1', 'L2', 'L2', 'L3', 'I0', 'L0', 'T2'],
            ['E0', 'E1', 'T1', 'T0', 'I1', 'L2', 'L2', 'T3', 'T1', 'L3', 'E0', 'I0', 'I0', 'T2', 'L0', 'T0', 'I0', 'T1', 'E3', 'E3', 'L3', 'T0', 'T1', 'T1', 'T3'],
            ['E2', 'T2', 'L1', 'E1', 'E3', 'L2', 'I0', 'L0', 'I0', 'T1', 'I0', 'L0', 'E3', 'L2', 'L0', 'I1', 'E1', 'T1', 'I1', 'T3', 'T3', 'L3', 'E2', 'I1', 'E3'],
            ['E0', 'L3', 'E1', 'L0', 'T0', 'T2', 'T0', 'I1', 'T0', 'T3', 'L2', 'T3', 'T3', 'L2', 'T3', 'E2', 'I0', 'T2', 'T3', 'E3', 'L0', 'I1', 'L0', 'T1', 'E0'],
            ['E0', 'T2', 'I1', 'L1', 'T2', 'L3', 'E2', 'E1', 'L1', 'E2', 'E0', 'E1', 'T0', 'T2', 'E0', 'L0', 'T3', 'E2', 'E2', 'L3', 'E1', 'E0', 'T1', 'E3', 'E0'],
            ['E3', 'T1', 'T3', 'T0', 'I0', 'L1', 'E3', 'E2', 'T0', 'T0', 'T0', 'L0', 'I1', 'T2', 'L1', 'E1', 'L3', 'I1', 'I0', 'T2', 'T1', 'I1', 'T0', 'T3', 'T2'],
            ['L0', 'L2', 'L2', 'T2', 'I1', 'T2', 'T1', 'L1', 'I0', 'I1', 'I0', 'T2', 'L1', 'I0', 'L1', 'T1', 'T1', 'E2', 'L0', 'L1', 'T1', 'T3', 'L0', 'E3', 'I0'],
            ['E3', 'L0', 'T2', 'I0', 'I0', 'I1', 'E3', 'T0', 'T1', 'E1', 'E3', 'T2', 'E2', 'L2', 'L0', 'I0', 'T3', 'I0', 'T1', 'I0', 'E0', 'E1', 'I1', 'L3', 'T2'],
            ['T0', 'T0', 'I1', 'E2', 'E3', 'E3', 'E3', 'I1', 'E0', 'L0', 'I1', 'T0', 'T2', 'L0', 'E1', 'I0', 'I1', 'E0', 'T3', 'L2', 'L3', 'E1', 'T3', 'E2', 'I0'],
            ['I0', 'E2', 'T3', 'E2', 'E3', 'I1', 'T2', 'T0', 'L2', 'E1', 'L3', 'T3', 'L2', 'T3', 'E2', 'I0', 'I1', 'L0', 'T2', 'E0', 'T3', 'E2', 'E0', 'L0', 'T3'],
            ['T3', 'L0', 'L1', 'T0', 'T0', 'E1', 'E2', 'I1', 'L2', 'E3', 'T0', 'T2', 'E2', 'T2', 'L0', 'E1', 'I1', 'I0', 'I0', 'L0', 'E2', 'L0', 'E2', 'E3', 'E0'],
            ['I1', 'I0', 'E1', 'T0', 'E0', 'E1', 'T1', 'T2', 'I0', 'L2', 'E2', 'T1', 'E3', 'E2', 'E3', 'E2', 'I1', 'E0', 'E2', 'I1', 'L0', 'T0', 'I1', 'E3', 'E3'],
            ['E0', 'E2', 'E2', 'T0', 'E0', 'E2', 'L3', 'E0', 'E0', 'T0', 'I0', 'T0', 'I0', 'E1', 'E3', 'T1', 'T2', 'I1', 'I0', 'T3', 'T0', 'I0', 'I0', 'I0', 'L1']
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╷  ┌──╴  ╶──┐  ╷  ╶─────┐  ╶──┬──╴  ╷  ┌──╴  ╶──┬──╴  ┌─────╴  ╷  ╷  ╷  ╷ \n'
            ' ├──┘  ╷  ╶──┤  └──┬──┬──┤  ╶──┤  ╶──┴──┤  ╷  ╶──┤  ╷  │  ╷  ╶──┤  │  ├──┘ \n'
            ' ├──╴  ├──╴  ├─────┘  ╵  ├──┐  ├──╴  ╶──┴──┤  ╷  ├──┴──┤  │  ╷  ├──┴──┘  ╷ \n'
            ' └──┬──┘  ╶──┘  ╶──┬──╴  ╵  │  │  ╷  ╶─────┴──┤  │  ╷  └──┴──┘  │  ╷  ╷  │ \n'
            ' ╶──┴──┬─────┬──╴  ├──╴  ╶──┴──┤  └──┐  ╶──┬──┴──┴──┤  ╷  ┌──╴  ├──┘  ├──┘ \n'
            ' ╷  ╷  ╵  ┌──┘  ╷  ├──╴  ╶──┐  └──┬──┴──╴  ├──┐  ╷  │  │  └──┬──┴──┬──┴──╴ \n'
            ' └──┴─────┴──┐  │  │  ╷  ╶──┤  ╷  ├──╴  ╶──┤  ╵  │  ├──┤  ┌──┤  ╷  └─────┐ \n'
            ' ╷  ╷  ╷  ╶──┤  └──┴──┴─────┴──┴──┤  ╶──┐  ├──╴  │  ╵  ╵  │  └──┤  ┌──╴  ╵ \n'
            ' │  └──┴──┬──┴────────┐  ┌──╴  ┌──┴──╴  ├──┴──┬──┘  ┌─────┤  ╷  │  │  ╷  ╷ \n'
            ' ├──╴  ╶──┴──╴  ╶─────┴──┴──┐  └──┬──╴  ├──╴  └──╴  ├──╴  ├──┘  └──┴──┴──┘ \n'
            ' │  ╶──┐  ╶─────┬────────┬──┴─────┤  ╶──┤  ┌──┬─────┴──┐  └──┬───────────╴ \n'
            ' └──┬──┘  ╷  ┌──┘  ╶─────┘  ╶─────┴──┐  └──┤  ├──┐  ╷  ╵  ╷  │  ╷  ╷  ╷  ╷ \n'
            ' ┌──┴──┐  │  ╵  ╶──┐  ╶──────────────┴──┬──┤  ╵  ╵  ├──┬──┘  └──┘  │  └──┤ \n'
            ' ╵  ╷  ├──┴─────┐  └──┬──┬──┐  ╶────────┤  └──┬─────┤  ╵  ╷  ┌──┬──┴──┬──┤ \n'
            ' ╶──┴──┘  ╷  ╷  └─────┘  │  ├─────┐  ╷  └──┐  │  ╷  ├─────┴──┤  └──╴  │  ╵ \n'
            ' ╶──┐  ╷  └──┴──┬──┬─────┤  ├──┐  ├──┤  ┌──┤  ╵  │  ├──┬──╴  └─────┐  ├──╴ \n'
            ' ╶──┤  │  ┌──┬──┘  ╵  ╶──┘  ╵  ╵  ╵  ├──┤  ╵  ┌──┤  ╵  ╵  ┌──╴  ╶──┤  ╵  ╷ \n'
            ' ╷  ├──┴──┤  │  ┌──╴  ╶──┬──┬──┬──┐  │  ├──┐  ╵  └────────┴──┬─────┴──┬──┤ \n'
            ' └──┘  ┌──┤  │  ├──┬──┐  │  │  │  ├──┘  │  └──┬──┬──╴  ┌──┐  ├──┬──┐  ╵  │ \n'
            ' ╷  ┌──┤  │  │  │  ╵  ├──┤  ╵  ╵  ├──╴  └──┐  │  ├─────┤  │  ╵  ╵  │  ┌──┤ \n'
            ' ├──┤  │  ╵  ╵  ╵  ╷  │  ╵  ┌─────┴──┬──┐  ╵  │  │  ╶──┤  └──┐  ╶──┤  ╵  │ \n'
            ' │  ╵  ├──╴  ╶─────┴──┴──┐  ╵  ┌──┬──┘  ├──╴  │  │  ┌──┤  ╶──┴──╴  ╵  ┌──┤ \n'
            ' ├──┐  └──┬──┬──╴  ╶─────┘  ╶──┤  ├──╴  ├──┐  ╵  │  │  │  ┌──╴  ┌──╴  ╵  ╵ \n'
            ' │  │  ╶──┤  ╵  ╶──┬──┬─────┐  ╵  ├──╴  ╵  ╵  ╷  │  ╵  ╵  │  ┌──┴─────╴  ╷ \n'
            ' ╵  ╵  ╶──┴──╴  ╶──┘  ╵  ╶──┴─────┴─────╴  ╶──┴──┴────────┴──┴───────────┘ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_grid30x30(self):
        matrix: list[list[PipeString]] = [
            ['E2', 'L3', 'E0', 'E3', 'L3', 'E0', 'L0', 'T0', 'E0', 'E2', 'E0', 'E2', 'L1', 'T3', 'L2', 'E3', 'E2', 'E3', 'L3', 'E1', 'E1', 'E3', 'L1', 'I0', 'I1', 'I0', 'E1', 'L3', 'E1', 'E2'],
            ['E3', 'L3', 'T1', 'E2', 'T2', 'T1', 'E3', 'L0', 'T0', 'L1', 'I1', 'I0', 'E3', 'E2', 'I1', 'I1', 'T0', 'L0', 'L2', 'T1', 'T3', 'L2', 'I0', 'E1', 'E3', 'T2', 'E3', 'L3', 'T0', 'T0'],
            ['I1', 'E0', 'T2', 'E2', 'E3', 'T2', 'I1', 'L3', 'T0', 'L2', 'I1', 'T1', 'E2', 'E1', 'T0', 'T2', 'T0', 'L3', 'E0', 'T1', 'T1', 'E1', 'I0', 'T0', 'L3', 'I1', 'E0', 'I1', 'T0', 'E3'],
            ['L2', 'L0', 'I1', 'L3', 'T2', 'T3', 'T0', 'L2', 'I1', 'E2', 'T1', 'T0', 'E2', 'I0', 'E1', 'E1', 'T3', 'I0', 'L0', 'L2', 'I1', 'T2', 'T3', 'L0', 'T3', 'T0', 'T2', 'I0', 'T2', 'L0'],
            ['L3', 'T2', 'L0', 'E0', 'L1', 'E2', 'I1', 'E1', 'I1', 'E2', 'T0', 'L0', 'E3', 'I1', 'E3', 'L3', 'E0', 'I1', 'T2', 'E2', 'T3', 'T3', 'E2', 'T1', 'T3', 'E2', 'E2', 'E1', 'L1', 'E3'],
            ['I0', 'L0', 'I0', 'E0', 'E3', 'I1', 'T2', 'T1', 'T2', 'T0', 'T0', 'T2', 'E0', 'T2', 'E3', 'I0', 'E0', 'L3', 'I0', 'E3', 'T3', 'L1', 'E3', 'I1', 'E3', 'I0', 'E0', 'E3', 'T3', 'L1'],
            ['L3', 'T3', 'L3', 'E1', 'I0', 'I1', 'L0', 'L2', 'E0', 'I1', 'E0', 'I0', 'T1', 'L3', 'E3', 'T2', 'E3', 'T0', 'L3', 'E0', 'I1', 'E3', 'L0', 'T2', 'E1', 'I0', 'I1', 'L1', 'T2', 'I1'],
            ['E0', 'L2', 'L0', 'E0', 'L1', 'E0', 'I0', 'L0', 'L2', 'L2', 'L2', 'E1', 'I1', 'E1', 'I0', 'I1', 'E3', 'T2', 'E0', 'I0', 'I1', 'E1', 'I0', 'I1', 'E1', 'L1', 'T1', 'L1', 'T1', 'E1'],
            ['L1', 'T2', 'E3', 'L1', 'L0', 'T0', 'L1', 'I1', 'T0', 'I0', 'T3', 'T0', 'L2', 'T0', 'T1', 'L2', 'L0', 'I0', 'I1', 'I0', 'I1', 'T1', 'T0', 'L2', 'T1', 'E1', 'T3', 'T1', 'E0', 'E0'],
            ['E1', 'T0', 'E3', 'I0', 'E0', 'T1', 'E0', 'E2', 'L1', 'E3', 'I0', 'L3', 'T0', 'L3', 'E0', 'L1', 'T2', 'L1', 'T1', 'L0', 'I0', 'I0', 'L2', 'I0', 'L1', 'E3', 'T3', 'I1', 'L1', 'L0'],
            ['I0', 'T3', 'T1', 'T1', 'I0', 'T3', 'T3', 'T0', 'T2', 'I0', 'T2', 'L1', 'T0', 'T1', 'E0', 'L1', 'I1', 'L2', 'T3', 'T1', 'L1', 'T3', 'T1', 'I0', 'E2', 'L3', 'T2', 'L1', 'T0', 'E0'],
            ['I1', 'I1', 'E3', 'E2', 'E1', 'I1', 'I1', 'L0', 'E3', 'I1', 'T3', 'E0', 'E0', 'T1', 'E1', 'E3', 'I1', 'T1', 'I0', 'L0', 'E2', 'I0', 'E0', 'E2', 'E1', 'I0', 'L1', 'E0', 'L0', 'L1'],
            ['T1', 'T1', 'E2', 'T2', 'I1', 'I1', 'L0', 'L2', 'T1', 'I1', 'T0', 'L1', 'I0', 'I0', 'E1', 'T2', 'E3', 'T0', 'T0', 'T2', 'E2', 'I1', 'I0', 'T1', 'L3', 'I0', 'E1', 'L1', 'I0', 'E2'],
            ['E2', 'L0', 'L1', 'E3', 'E1', 'E0', 'T3', 'I1', 'L2', 'E0', 'T3', 'T3', 'T2', 'L0', 'L3', 'L1', 'T1', 'L1', 'E3', 'L3', 'E1', 'T3', 'T2', 'T1', 'E2', 'T3', 'L0', 'I0', 'L1', 'E0'],
            ['E3', 'L3', 'L2', 'T2', 'T3', 'T3', 'T3', 'L1', 'I1', 'I1', 'L0', 'E0', 'T2', 'I0', 'T3', 'E0', 'T1', 'L0', 'T2', 'E3', 'L2', 'T3', 'L1', 'E1', 'L2', 'T1', 'E1', 'T0', 'L2', 'E0'],
            ['E1', 'E3', 'I0', 'L2', 'T1', 'L3', 'E2', 'L0', 'E2', 'E2', 'I0', 'T1', 'T2', 'E1', 'T2', 'T3', 'L2', 'I0', 'L3', 'E1', 'E3', 'L1', 'T3', 'T1', 'T0', 'T2', 'T0', 'T2', 'L3', 'L3'],
            ['L2', 'L0', 'E3', 'E1', 'L0', 'E2', 'L0', 'E1', 'E0', 'I1', 'L0', 'E0', 'E1', 'E0', 'I1', 'T2', 'E1', 'T2', 'T2', 'L3', 'L1', 'T2', 'E0', 'L2', 'E3', 'I1', 'E0', 'L0', 'T0', 'L2'],
            ['E2', 'T3', 'T1', 'I0', 'L2', 'E3', 'T2', 'L1', 'L2', 'E1', 'T3', 'T3', 'I1', 'I0', 'I0', 'T0', 'T1', 'T1', 'E1', 'L3', 'T3', 'T1', 'I0', 'E3', 'E3', 'T0', 'T3', 'I0', 'L0', 'E2'],
            ['E1', 'T2', 'L3', 'E1', 'L3', 'T2', 'T0', 'T3', 'T3', 'I0', 'I1', 'I0', 'T1', 'T3', 'I1', 'T2', 'I1', 'T0', 'L0', 'I1', 'L2', 'T1', 'I0', 'T1', 'I0', 'E1', 'T1', 'E1', 'T2', 'L2'],
            ['L3', 'I0', 'E1', 'T2', 'I0', 'T2', 'E2', 'T0', 'E0', 'E2', 'I1', 'I1', 'T3', 'T2', 'E2', 'E3', 'L3', 'T1', 'T2', 'T1', 'L1', 'L1', 'E2', 'L2', 'I1', 'L2', 'T1', 'E1', 'E0', 'E3'],
            ['L2', 'I1', 'T2', 'T3', 'E0', 'E3', 'E1', 'T0', 'I0', 'E3', 'T3', 'T0', 'T0', 'L2', 'L0', 'E0', 'T1', 'L2', 'T1', 'I0', 'T0', 'E0', 'L0', 'T0', 'E0', 'I0', 'L2', 'I0', 'I1', 'E2'],
            ['L2', 'I1', 'T1', 'L2', 'L2', 'E1', 'I0', 'T3', 'I0', 'E3', 'I0', 'E1', 'E1', 'E2', 'E0', 'L2', 'T3', 'E2', 'I1', 'E2', 'T1', 'T2', 'L0', 'L2', 'L0', 'L2', 'T3', 'T1', 'T0', 'E1'],
            ['I1', 'E0', 'T1', 'E0', 'I0', 'E3', 'E2', 'L1', 'L2', 'T3', 'L0', 'E3', 'L2', 'I0', 'E0', 'L0', 'I0', 'L3', 'T1', 'E3', 'E3', 'L2', 'T0', 'L0', 'T1', 'E0', 'E1', 'E0', 'L2', 'E2'],
            ['E1', 'E3', 'T2', 'E2', 'T0', 'T3', 'L0', 'L1', 'E1', 'T2', 'I1', 'T0', 'T1', 'T2', 'T3', 'T0', 'T1', 'T2', 'E2', 'L0', 'T3', 'I0', 'T0', 'E2', 'T1', 'I0', 'I0', 'E3', 'E1', 'E1'],
            ['L2', 'T1', 'L3', 'E3', 'I1', 'E2', 'E0', 'L2', 'T0', 'T3', 'L1', 'I1', 'L3', 'I0', 'T1', 'I1', 'I1', 'E1', 'E1', 'E2', 'T1', 'E1', 'T1', 'L3', 'L1', 'I0', 'I0', 'I0', 'T2', 'L3'],
            ['I0', 'E2', 'E1', 'I0', 'T2', 'T1', 'T2', 'T2', 'T1', 'E0', 'E0', 'I1', 'E1', 'E3', 'L1', 'E2', 'T3', 'L0', 'I0', 'L0', 'T1', 'L1', 'E2', 'T1', 'I1', 'T0', 'T3', 'T2', 'I1', 'E0'],
            ['I0', 'T2', 'L0', 'L3', 'T2', 'E0', 'I0', 'E3', 'I1', 'L1', 'T2', 'T2', 'T1', 'L1', 'E2', 'T0', 'T3', 'T0', 'L3', 'T1', 'E2', 'I0', 'E3', 'T3', 'E1', 'E1', 'I1', 'L3', 'I1', 'E2'],
            ['E1', 'L3', 'T0', 'I0', 'T1', 'E2', 'T1', 'E0', 'I0', 'L0', 'T0', 'E0', 'I0', 'E3', 'E3', 'T0', 'I1', 'L0', 'L2', 'T3', 'L0', 'T2', 'E3', 'T1', 'T0', 'E0', 'T1', 'I0', 'T2', 'L0'],
            ['E3', 'I1', 'T3', 'E0', 'E2', 'L1', 'T3', 'L3', 'T1', 'E2', 'E0', 'L0', 'E2', 'E0', 'L0', 'T0', 'T0', 'E3', 'I0', 'I0', 'I1', 'I0', 'E1', 'T0', 'L2', 'E3', 'L1', 'E2', 'T2', 'E2'],
            ['E1', 'I1', 'T1', 'L3', 'E0', 'I0', 'L3', 'E0', 'L2', 'E0', 'E3', 'T3', 'I1', 'T2', 'L2', 'E2', 'L3', 'E0', 'E0', 'E0', 'E1', 'L3', 'E0', 'E0', 'T2', 'I1', 'I1', 'E2', 'L1', 'E3']
        ]
        grid = Grid([[Pipe(matrix[row][column]) for column in range(len(matrix[row]))] for row in range(len(matrix))])
        expected_solution = (
            ' ╶──┐  ╷  ╶──┐  ╷  ┌──┬──╴  ╷  ╷  ╷  ┌──┬──┐  ╷  ╷  ╶──┐  ╷  ╷  ╷  ┌───────────╴  ┌──╴  ╷ \n'
            ' ╷  └──┤  ╶──┴──┤  ╵  └──┬──┘  │  │  ╵  ╵  │  │  ├──┐  └──┤  ├──┘  │  ╷  ╶──┬──╴  └──┬──┤ \n'
            ' │  ╶──┤  ╷  ╶──┴─────┐  ├──┐  │  ├──╴  ╷  ├──┴──┤  └──╴  ├──┴──╴  │  ├──┐  │  ╶─────┤  ╵ \n'
            ' └──┐  │  └──┬──┬──┬──┘  │  ╵  ├──┴──╴  │  ╵  ╶──┴─────┐  └─────┬──┴──┘  ├──┴──┬─────┴──┐ \n'
            ' ┌──┴──┘  ╶──┘  ╵  │  ╷  │  ╶──┤  ┌──╴  │  ╶──┐  ╶─────┤  ╶──┬──┤  ╶──┬──┤  ╷  ╵  ╶──┐  ╵ \n'
            ' │  ┌─────╴  ╶─────┴──┴──┴──┬──┴──┴──╴  ├──╴  │  ╶──┐  │  ╶──┤  └──╴  │  ╵  │  ╷  ╷  ├──┐ \n'
            ' └──┴──┐  ╶────────┐  ┌──╴  │  ╶─────┬──┘  ╷  ├──╴  ├──┘  ╷  │  ╶──┐  ├──╴  │  │  └──┤  │ \n'
            ' ╷  ┌──┘  ╶──┐  ╷  │  └──┐  └──┐  ╷  │  ╷  │  │  ╶──┤  ╷  │  │  ╷  │  │  ╷  └──┤  ┌──┤  ╵ \n'
            ' └──┤  ╶──┐  └──┤  └─────┴─────┤  ├──┘  ├──┤  └──┐  │  │  │  │  ├──┴──┘  ├──╴  ├──┤  ╵  ╷ \n'
            ' ╷  ├──╴  │  ╶──┤  ╷  ╷  ┌──╴  │  └──┬──┘  ╵  ┌──┴──┘  ├──┘  │  │  ┌─────┘  ╶──┤  │  ┌──┘ \n'
            ' │  ├──┬──┴─────┴──┴──┴──┴─────┤  ┌──┴──┬──╴  └─────┐  ├──┬──┘  ├──┴─────╴  ┌──┤  └──┤  ╷ \n'
            ' │  │  ╵  ╷  ╶────────┐  ╶─────┤  ╵  ╷  ├──╴  ╶─────┤  │  └──╴  │  ╷  ╷  ╷  │  └──╴  └──┘ \n'
            ' ├──┴──╴  ├────────┐  └──┬─────┴──┐  │  │  ╶──┬──╴  ├──┴──┬──╴  │  │  ├──┘  │  ╷  ┌─────╴ \n'
            ' ╵  ┌──┐  ╵  ╷  ╷  ├─────┘  ╶──┬──┴──┤  └──┐  └──┬──┘  ╷  └──╴  ├──┴──┴──╴  ├──┘  │  ┌──╴ \n'
            ' ╶──┘  └──┬──┤  ├──┤  ┌────────┘  ╷  ├─────┤  ╶──┤  ┌──┴──╴  ┌──┤  ┌──╴  ┌──┴──╴  ├──┘  ╷ \n'
            ' ╷  ╶─────┘  ├──┘  ╵  └──╴  ╶─────┴──┤  ╶──┴──┬──┘  │  ┌──╴  ╵  └──┴──┬──┴──┬──┬──┤  ┌──┘ \n'
            ' └──┐  ╷  ╶──┘  ╶──┐  ╷  ╶─────┐  ╷  ╵  ╶─────┤  ╷  ├──┴──┐  ┌──┬──╴  └──╴  │  ╵  └──┴──┐ \n'
            ' ╶──┤  ├─────┐  ╶──┤  └──┐  ╶──┴──┴───────────┴──┴──┤  ╷  └──┤  ├─────╴  ╶──┴──┬─────┐  ╵ \n'
            ' ╶──┴──┘  ╷  └──┬──┴──┬──┴───────────┬──┬─────┬─────┤  └─────┘  ├─────┬─────╴  ├──╴  ├──┐ \n'
            ' ┌─────╴  ├─────┤  ╶──┤  ╷  ╶────────┤  ├──╴  ╵  ┌──┴──┬──┬──┐  └──╴  └─────┐  ├──╴  ╵  ╵ \n'
            ' └─────┬──┴──╴  ╵  ╶──┤  │  ╶──┬──┬──┤  └──┐  ╶──┤  ┌──┤  │  ├──╴  ┌──┬──╴  │  └────────╴ \n'
            ' ┌─────┤  ┌──┐  ╶─────┤  │  ╷  │  ╵  ╵  ╷  ╵  ┌──┤  ╵  │  ╵  ├──┬──┘  └──┐  └──┬──┬──┬──╴ \n'
            ' │  ╶──┤  ╵  │  ╷  ╶──┘  └──┴──┘  ╶──┐  │  ╶──┘  │  ┌──┴──╴  ╵  └──┬──┐  ├──╴  ╵  ╵  └──╴ \n'
            ' ╵  ╷  ├──╴  ├──┤  ┌──┐  ╶──┬─────┬──┴──┴──┬──┬──┤  ├──╴  ┌──┬─────┤  ╵  ├────────╴  ╷  ╷ \n'
            ' ┌──┴──┘  ╷  │  ╵  ╵  └──┬──┴──┐  │  ┌─────┤  │  │  ╵  ╷  ╵  ├──╴  ├──┐  └───────────┴──┘ \n'
            ' │  ╷  ╷  │  ├──┬──┬──┬──┤  ╷  ╵  │  ╵  ╶──┘  ╵  ├──┐  │  ┌──┴──┐  ╵  ├─────┬──┬──┬─────╴ \n'
            ' │  ├──┘  └──┤  ╵  │  ╵  │  └──┬──┴──┬──┐  ╶──┬──┤  ├──┘  ├──╴  │  ╶──┤  ╷  ╵  │  └─────╴ \n'
            ' ╵  └──┬─────┤  ╷  ├──╴  │  ┌──┴──╴  │  ╵  ╶──┤  │  └──┐  ├──┐  ├──╴  ├──┴──╴  ├─────┬──┐ \n'
            ' ╶─────┤  ╷  ╵  └──┤  ┌──┤  ╵  ╶──┐  ╵  ╷  ┌──┤  ├──╴  │  │  │  │  ╶──┴──┐  ╶──┘  ╶──┤  ╵ \n'
            ' ╶─────┴──┘  ╶─────┘  ╵  └──╴  ╶──┴─────┴──┘  ╵  └──╴  ╵  ╵  ╵  └──╴  ╶──┴────────╴  └──╴ '
        )
        solver = PipesSolver(grid, self.get_solver_engine())
        solution = solver.get_solution()
        self.assertEqual(expected_solution, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
