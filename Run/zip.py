﻿from Domain.Puzzles.Zip.ZipSolver import ZipSolver
from GridPlayers.LinkedIn.ZipGridPlayer import ZipGridPlayer
from GridProviders.Linkedin.ZipGridProvider import ZipGridProvider


grid_provider = ZipGridProvider()
game_player = ZipGridPlayer()
grid, browser_context = grid_provider.get_grid("https://www.linkedin.com/games/zip/")
game_solver = ZipSolver(grid)
solution = game_solver.get_solution()
game_player.play(solution, browser_context)
