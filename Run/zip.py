﻿from Domain.Puzzles.Zip.ZipSolver import ZipSolver
from GridPlayers.LinkedIn.ZipPlayer import ZipPlayer
from GridProviders.Linkedin.ZipGridProvider import ZipGridProvider


grid_provider = ZipGridProvider()
grid, browser_context = grid_provider.get_grid("https://www.linkedin.com/games/zip/")
game_player = ZipPlayer(browser_context)
game_solver = ZipSolver(grid)
solution = game_solver.get_solution()
game_player.play(solution)
