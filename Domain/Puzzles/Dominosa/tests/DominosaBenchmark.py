﻿# import timeit
# 
# from Puzzles.Dominosa.DominosaSolver import DominosaSolver
# from Utils.Board import Board
# 
# 
# class DominosaBenchmark:
#     def __init__(self):
#         self.grids4x5 = [
#             [[3, 2, 2, 0, 3], [1, 0, 0, 2, 3], [0, 1, 2, 3, 0], [2, 1, 3, 1, 1]],
#             [[3, 2, 1, 2, 3], [0, 1, 1, 0, 3], [1, 0, 0, 3, 1], [3, 2, 2, 0, 2]],
#             [[2, 2, 1, 1, 0], [1, 0, 0, 0, 3], [2, 3, 3, 1, 0], [2, 3, 3, 2, 1]],
#             [[0, 0, 1, 3, 3], [3, 2, 1, 2, 3], [1, 1, 2, 1, 0], [0, 0, 3, 2, 2]],
#         ]
# 
#         self.grids5x6 = [
#             [[0, 2, 1, 4, 0, 3], [1, 2, 3, 1, 1, 3], [1, 2, 0, 4, 2, 2], [0, 4, 3, 3, 0, 2], [4, 1, 4, 4, 0, 3]],
#             [[3, 4, 4, 3, 3, 1], [4, 0, 2, 1, 1, 0], [4, 0, 3, 2, 0, 3], [0, 1, 2, 2, 4, 1], [3, 0, 1, 4, 2, 2]],
#             [[2, 1, 4, 3, 3, 4], [0, 3, 4, 0, 2, 3], [2, 3, 0, 4, 2, 0], [0, 1, 3, 2, 1, 0], [4, 1, 2, 4, 1, 1]],
#             [[2, 4, 4, 2, 4, 0], [4, 3, 1, 1, 4, 1], [1, 3, 1, 0, 0, 2], [3, 0, 0, 1, 3, 2], [3, 2, 3, 4, 2, 0]],
#         ]
# 
#         self.grids6x7 = [
#             [[4, 2, 2, 5, 5, 1, 3], [4, 0, 5, 1, 0, 5, 4], [0, 0, 2, 0, 4, 2, 4], [1, 1, 2, 4, 1, 4, 0], [1, 1, 0, 3, 5, 5, 2], [2, 3, 3, 3, 3, 3, 5]],
#             [[4, 3, 0, 2, 1, 5, 5], [2, 3, 3, 2, 2, 3, 0], [4, 3, 4, 1, 1, 2, 1], [2, 1, 5, 5, 4, 0, 2], [5, 1, 4, 5, 0, 5, 0], [4, 4, 1, 0, 3, 3, 0]],
#             [[0, 2, 5, 5, 5, 2, 1], [0, 4, 2, 3, 3, 0, 1], [1, 3, 5, 4, 1, 2, 2], [2, 5, 5, 1, 0, 0, 5], [4, 3, 4, 4, 1, 3, 2], [4, 3, 0, 4, 3, 1, 0]],
#             [[2, 2, 0, 5, 5, 5, 2], [3, 3, 0, 4, 3, 5, 1], [3, 4, 4, 0, 2, 2, 5], [1, 3, 3, 4, 4, 1, 5], [0, 1, 0, 1, 0, 2, 4], [5, 1, 4, 2, 0, 1, 3]],
#         ]
# 
#         self.grids7x8 = [
#             [[1, 2, 2, 4, 5, 2, 5, 5], [0, 4, 3, 5, 5, 6, 0, 6], [5, 4, 2, 2, 4, 6, 2, 1], [1, 1, 1, 4, 4, 3, 1, 3], [5, 6, 4, 3, 4, 1, 1, 3], [3, 0, 6, 3, 3, 6, 0, 2], [2, 6, 0, 5, 0, 6, 0, 0]],
#             [[4, 2, 5, 3, 0, 0, 5, 5], [4, 1, 6, 1, 1, 5, 2, 6], [0, 5, 4, 0, 1, 0, 5, 3], [2, 2, 2, 6, 2, 3, 1, 1], [6, 0, 3, 4, 0, 3, 1, 3], [4, 5, 2, 4, 3, 4, 2, 5], [4, 6, 0, 6, 6, 3, 6, 1]],
#             [[0, 0, 4, 1, 5, 6, 4, 2], [3, 1, 6, 2, 2, 2, 1, 2], [3, 3, 0, 1, 5, 4, 0, 0], [5, 0, 3, 3, 5, 6, 3, 0], [2, 1, 4, 6, 4, 1, 3, 4], [6, 5, 6, 1, 5, 1, 3, 4], [6, 6, 0, 5, 2, 5, 2, 4]],
#             [[0, 6, 6, 4, 1, 2, 6, 4], [4, 0, 4, 0, 5, 6, 2, 1], [5, 3, 4, 0, 0, 3, 1, 3], [4, 0, 5, 4, 2, 3, 0, 2], [2, 1, 6, 3, 5, 1, 5, 3], [4, 1, 6, 5, 2, 2, 6, 3], [0, 5, 2, 5, 6, 1, 1, 3]],
#         ]
#         self.grids8x9 = [
#             [[0, 7, 6, 5, 7, 7, 6, 1, 1], [1, 3, 4, 7, 4, 1, 0, 0, 0], [6, 3, 2, 6, 7, 5, 4, 2, 2], [0, 4, 2, 3, 0, 7, 4, 0, 4], [1, 6, 6, 4, 5, 6, 2, 6, 1], [2, 0, 7, 1, 3, 5, 7, 4, 5], [0, 1, 3, 3, 5, 3, 2, 4, 5], [3, 3, 7, 2, 6, 5, 1, 2, 5]],
#             [[7, 4, 3, 4, 4, 1, 1, 1, 0], [2, 4, 6, 7, 0, 1, 0, 7, 6], [7, 2, 2, 3, 3, 4, 2, 2, 2], [6, 6, 2, 6, 4, 3, 6, 6, 1], [0, 6, 1, 7, 0, 3, 7, 5, 5], [5, 5, 1, 5, 3, 3, 0, 0, 5], [7, 3, 3, 4, 2, 0, 0, 5, 1], [7, 5, 6, 7, 4, 4, 1, 5, 2]],
#             [[6, 3, 5, 6, 1, 7, 7, 4, 2], [4, 0, 4, 6, 4, 2, 2, 7, 7], [4, 2, 5, 2, 1, 6, 7, 1, 2], [5, 6, 5, 0, 1, 1, 3, 0, 7], [2, 4, 2, 0, 7, 0, 3, 6, 5], [1, 5, 4, 7, 6, 6, 2, 0, 5], [3, 1, 0, 3, 3, 5, 7, 1, 0], [1, 3, 4, 3, 3, 4, 0, 6, 5]],
#             [[3, 6, 7, 3, 1, 7, 7, 5, 5], [3, 2, 2, 0, 0, 6, 7, 5, 0], [0, 6, 1, 4, 2, 4, 1, 3, 4], [1, 3, 3, 0, 3, 3, 4, 0, 5], [3, 6, 0, 7, 2, 4, 4, 5, 1], [1, 1, 1, 0, 5, 7, 2, 2, 1], [5, 7, 6, 2, 4, 6, 7, 2, 5], [7, 2, 6, 6, 4, 5, 4, 0, 6]],
#         ]
# 
#         self.grids9x10 = [
#             [[4, 0, 6, 6, 1, 6, 5, 6, 3, 7], [1, 7, 4, 8, 1, 7, 7, 1, 0, 2], [0, 4, 4, 8, 7, 0, 2, 6, 8, 8], [5, 4, 4, 6, 2, 3, 5, 0, 7, 2], [5, 8, 1, 5, 2, 8, 1, 3, 4, 7], [0, 3, 4, 3, 6, 7, 4, 2, 2, 8], [0, 5, 5, 8, 6, 7, 2, 5, 1, 0], [0, 6, 8, 3, 5, 7, 4, 3, 8, 5], [2, 3, 1, 0, 6, 3, 2, 3, 1, 1]],
#             [[4, 6, 2, 3, 6, 8, 1, 2, 1, 4], [7, 3, 4, 3, 8, 2, 8, 0, 5, 0], [5, 1, 5, 0, 6, 0, 4, 1, 7, 3], [8, 3, 2, 2, 1, 7, 5, 5, 7, 6], [2, 2, 0, 3, 4, 3, 4, 2, 3, 6], [8, 5, 5, 6, 3, 1, 7, 7, 3, 1], [7, 8, 2, 6, 5, 0, 6, 0, 1, 4], [4, 8, 7, 0, 8, 5, 4, 5, 1, 4], [2, 8, 1, 7, 7, 0, 0, 6, 8, 6]],
#             [[2, 3, 0, 4, 5, 7, 0, 7, 2, 7], [8, 7, 3, 6, 7, 2, 3, 1, 0, 0], [4, 3, 8, 4, 1, 0, 4, 2, 3, 4], [6, 0, 1, 8, 7, 3, 5, 3, 0, 4], [6, 1, 1, 3, 3, 5, 5, 8, 0, 1], [6, 6, 7, 2, 2, 2, 6, 8, 5, 5], [5, 4, 1, 8, 0, 2, 2, 4, 8, 0], [2, 6, 4, 6, 3, 5, 8, 8, 6, 8], [1, 1, 4, 7, 6, 5, 1, 5, 7, 7]],
#             [[7, 4, 1, 2, 8, 1, 1, 7, 0, 2], [5, 3, 1, 8, 0, 0, 7, 5, 5, 2], [1, 3, 1, 5, 4, 0, 1, 7, 4, 2], [5, 3, 3, 7, 2, 6, 3, 6, 4, 8], [5, 0, 4, 2, 1, 6, 6, 6, 4, 8], [3, 2, 1, 2, 0, 6, 5, 5, 8, 3], [8, 6, 4, 8, 6, 5, 0, 7, 8, 2], [0, 8, 8, 4, 3, 7, 5, 0, 0, 7], [4, 1, 3, 7, 3, 7, 4, 6, 2, 6]],
#         ]
# 
#         self.grids10x11 = [
#             [[1, 5, 6, 8, 8, 4, 9, 9, 2, 6, 6], [1, 8, 4, 7, 2, 0, 9, 7, 7, 4, 0], [4, 5, 9, 6, 4, 3, 9, 7, 5, 9, 0], [6, 1, 0, 2, 7, 8, 3, 9, 4, 7, 5], [7, 4, 1, 5, 3, 5, 0, 0, 9, 0, 5], [6, 3, 2, 3, 0, 2, 5, 5, 3, 0, 6], [2, 1, 5, 7, 6, 1, 8, 9, 4, 8, 8], [5, 6, 2, 3, 8, 3, 1, 8, 2, 9, 6], [1, 2, 4, 4, 3, 1, 3, 7, 2, 9, 0], [8, 8, 2, 1, 7, 4, 3, 0, 7, 1, 6]],
#             [[0, 1, 2, 7, 1, 5, 4, 6, 2, 0, 3], [8, 8, 5, 7, 4, 2, 1, 7, 2, 5, 3], [0, 5, 1, 0, 1, 6, 5, 4, 3, 1, 3], [6, 2, 6, 6, 3, 8, 8, 4, 6, 1, 7], [8, 9, 8, 2, 2, 6, 2, 0, 1, 9, 3], [4, 5, 5, 9, 0, 8, 5, 0, 4, 4, 0], [4, 5, 7, 9, 7, 9, 8, 3, 7, 0, 7], [2, 5, 1, 9, 4, 9, 7, 8, 8, 7, 1], [9, 9, 6, 0, 4, 3, 7, 1, 5, 3, 6], [3, 9, 4, 9, 2, 6, 0, 8, 2, 3, 6]],
#             [[5, 2, 3, 8, 7, 5, 4, 7, 9, 0, 9], [3, 1, 2, 8, 6, 5, 7, 3, 2, 1, 6], [4, 0, 1, 8, 2, 1, 5, 7, 7, 8, 9], [2, 1, 4, 9, 0, 1, 9, 5, 4, 8, 2], [6, 0, 3, 0, 3, 7, 1, 6, 8, 4, 2], [3, 5, 5, 2, 0, 6, 8, 3, 9, 5, 8], [6, 5, 0, 2, 1, 5, 4, 9, 6, 3, 3], [7, 7, 8, 7, 5, 4, 9, 9, 6, 1, 9], [4, 8, 6, 4, 0, 2, 6, 6, 7, 4, 4], [3, 7, 0, 1, 0, 2, 3, 9, 0, 8, 1]],
#             [[5, 2, 4, 4, 8, 3, 9, 0, 4, 4, 8], [4, 7, 7, 9, 5, 4, 5, 1, 9, 6, 0], [2, 7, 3, 4, 3, 2, 2, 4, 9, 2, 8], [5, 5, 0, 0, 8, 4, 3, 3, 7, 8, 2], [7, 3, 3, 1, 5, 9, 1, 0, 1, 8, 0], [7, 6, 0, 1, 8, 3, 2, 7, 6, 5, 7], [6, 6, 9, 6, 1, 5, 0, 1, 9, 8, 7], [9, 5, 3, 1, 4, 8, 1, 0, 9, 1, 8], [5, 6, 2, 6, 6, 3, 5, 4, 0, 6, 2], [7, 8, 2, 7, 1, 3, 2, 6, 9, 9, 0]],
#         ]
# 
#         self.grids16x17 = [
#             #[[11, 14, 12, 7, 7, 7, 5, 15, 2, 2, 1, 2, 13, 14, 11, 10, 0], [0, 12, 6, 6, 15, 15, 1, 2, 13, 1, 10, 5, 0, 14, 1, 9, 8], [0, 3, 10, 2, 8, 14, 0, 15, 15, 15, 5, 3, 6, 4, 2, 11, 15], [0, 1, 12, 13, 14, 2, 3, 5, 3, 8, 11, 3, 14, 7, 9, 7, 1], [5, 1, 2, 4, 4, 4, 4, 1, 5, 2, 13, 13, 5, 4, 9, 15, 7], [8, 11, 7, 15, 9, 6, 0, 10, 15, 10, 8, 10, 12, 1, 9, 9, 8], [6, 6, 12, 7, 0, 5, 6, 10, 4, 12, 1, 14, 10, 2, 7, 9, 3], [7, 14, 11, 7, 12, 0, 4, 12, 8, 5, 3, 8, 9, 8, 14, 12, 4], [10, 15, 10, 2, 2, 1, 12, 2, 0, 11, 1, 11, 6, 0, 8, 12, 14], [3, 10, 0, 4, 11, 6, 11, 9, 1, 11, 8, 3, 5, 4, 8, 5, 1], [5, 15, 0, 8, 2, 14, 11, 9, 1, 6, 11, 7, 11, 0, 12, 13, 6], [5, 11, 13, 13, 10, 14, 1, 0, 12, 15, 12, 7, 9, 9, 2, 14, 14], [13, 4, 1, 9, 7, 4, 0, 10, 10, 10, 13, 12, 13, 3, 3, 5, 9], [13, 6, 10, 6, 6, 8, 4, 12, 11, 13, 12, 7, 3, 5, 15, 15, 5], [7, 3, 9, 14, 10, 13, 11, 5, 3, 2, 9, 7, 3, 8, 13, 6, 3], [8, 2, 4, 6, 8, 4, 15, 4, 14, 13, 3, 0, 6, 13, 15, 14, 9]],
#             #[[15, 0, 3, 12, 2, 4, 5, 1, 15, 15, 11, 4, 4, 14, 13, 9, 1], [6, 6, 13, 12, 6, 15, 14, 9, 4, 13, 5, 10, 0, 15, 12, 4, 3], [14, 0, 0, 8, 9, 12, 9, 12, 3, 9, 3, 4, 2, 11, 5, 8, 8], [14, 15, 13, 3, 7, 3, 10, 7, 12, 8, 0, 14, 3, 1, 3, 15, 4], [7, 1, 5, 6, 6, 3, 8, 6, 7, 11, 12, 0, 1, 0, 4, 1, 12], [2, 10, 5, 12, 5, 3, 3, 10, 8, 11, 6, 7, 8, 1, 3, 8, 14], [5, 10, 7, 9, 9, 1, 11, 15, 9, 5, 0, 4, 9, 1, 4, 0, 12], [0, 10, 3, 12, 6, 11, 15, 11, 13, 2, 13, 3, 7, 7, 5, 11, 12], [15, 14, 8, 11, 8, 10, 10, 7, 6, 0, 10, 2, 11, 15, 13, 4, 2], [14, 8, 8, 7, 4, 6, 13, 11, 2, 9, 13, 2, 6, 10, 1, 15, 2], [0, 13, 13, 9, 14, 13, 12, 0, 11, 13, 15, 14, 6, 1, 14, 11, 8], [7, 15, 4, 6, 1, 3, 8, 3, 2, 7, 2, 9, 6, 14, 4, 10, 14], [3, 2, 2, 1, 5, 11, 14, 7, 4, 11, 12, 10, 10, 10, 14, 10, 0], [5, 11, 6, 2, 5, 9, 12, 4, 9, 7, 12, 8, 15, 5, 0, 13, 15], [0, 8, 2, 7, 14, 9, 5, 1, 15, 6, 0, 10, 9, 7, 1, 1, 11], [8, 7, 1, 10, 12, 13, 2, 4, 5, 5, 9, 2, 6, 14, 5, 13, 13]],
#             # [[13, 2, 13, 3, 3, 7, 6, 1, 10, 12, 12, 12, 11, 15, 10, 0, 15], [15, 15, 6, 9, 7, 0, 7, 8, 7, 9, 8, 12, 8, 3, 12, 14, 2], [11, 5, 1, 3, 7, 2, 10, 15, 4, 13, 1, 4, 0, 0, 7, 12, 12], [4, 15, 13, 14, 4, 5, 7, 1, 13, 7, 0, 12, 5, 8, 0, 5, 15], [1, 9, 5, 7, 12, 4, 3, 5, 2, 6, 12, 3, 5, 2, 6, 1, 6], [3, 4, 0, 12, 2, 2, 9, 5, 8, 14, 0, 9, 7, 4, 5, 0, 6], [14, 13, 12, 10, 8, 11, 0, 13, 8, 8, 0, 5, 7, 2, 5, 6, 3], [9, 11, 15, 8, 11, 0, 9, 0, 11, 9, 10, 14, 14, 14, 14, 12, 10], [9, 11, 1, 11, 9, 6, 11, 10, 8, 14, 14, 7, 4, 10, 1, 9, 7], [2, 6, 6, 6, 14, 0, 15, 14, 2, 5, 2, 9, 8, 11, 3, 7, 11], [12, 1, 1, 13, 3, 6, 4, 9, 2, 1, 1, 2, 10, 15, 8, 5, 8], [6, 15, 8, 6, 14, 3, 0, 12, 3, 13, 13, 7, 13, 7, 10, 0, 3], [3, 0, 13, 10, 8, 4, 3, 4, 7, 11, 4, 3, 4, 13, 11, 5, 9], [6, 5, 15, 14, 1, 4, 11, 14, 10, 6, 13, 9, 10, 8, 11, 10, 9], [4, 15, 15, 1, 14, 15, 6, 12, 15, 2, 13, 11, 5, 1, 13, 10, 4], [14, 13, 10, 2, 1, 2, 3, 2, 8, 1, 15, 10, 12, 9, 11, 5, 4]],
#             [[12, 9, 1, 4, 12, 12, 10, 9, 8, 5, 15, 10, 2, 4, 11, 8, 4], [2, 14, 11, 5, 8, 1, 5, 1, 15, 15, 8, 6, 9, 13, 14, 7, 15], [2, 7, 10, 10, 3, 9, 4, 13, 6, 2, 14, 6, 15, 3, 15, 7, 11], [11, 13, 13, 9, 3, 8, 8, 7, 13, 13, 11, 3, 5, 1, 10, 5, 6], [3, 1, 7, 6, 7, 12, 12, 10, 14, 5, 4, 4, 13, 1, 7, 15, 13], [8, 5, 15, 1, 7, 9, 4, 1, 2, 11, 13, 11, 5, 9, 3, 12, 0], [6, 14, 14, 1, 15, 15, 10, 3, 2, 12, 7, 0, 11, 12, 9, 11, 1], [15, 12, 0, 6, 1, 14, 0, 12, 8, 2, 5, 8, 10, 11, 9, 4, 14], [14, 14, 2, 2, 15, 12, 6, 6, 12, 5, 15, 12, 15, 5, 5, 10, 13], [4, 3, 1, 8, 2, 5, 3, 3, 0, 0, 1, 1, 10, 14, 3, 9, 8], [1, 10, 10, 3, 2, 4, 6, 8, 14, 0, 8, 5, 3, 6, 2, 9, 6], [12, 9, 11, 10, 11, 4, 0, 2, 2, 9, 0, 0, 13, 4, 12, 13, 6], [14, 4, 12, 13, 6, 8, 5, 7, 11, 0, 2, 12, 8, 6, 10, 7, 10], [0, 13, 13, 8, 7, 3, 5, 7, 2, 7, 14, 0, 6, 11, 0, 3, 3], [11, 11, 5, 9, 8, 3, 4, 14, 0, 10, 14, 14, 2, 13, 4, 0, 4], [6, 1, 7, 15, 10, 7, 15, 0, 9, 11, 15, 9, 1, 7, 4, 13, 9]],
#         ]
# 
#         self.grids21x22 = [
#             [[3, 14, 4, 4, 4, 9, 15, 19, 4, 18, 3, 13, 16, 0, 5, 1, 13, 9, 12, 16, 3, 12], [16, 18, 17, 0, 14, 10, 10, 14, 8, 9, 18, 2, 4, 1, 8, 2, 17, 7, 19, 16, 15, 8], [13, 8, 15, 19, 18, 9, 0, 12, 8, 4, 13, 13, 4, 1, 17, 4, 13, 13, 13, 16, 10, 10], [10, 13, 12, 5, 17, 17, 15, 0, 5, 4, 1, 5, 10, 14, 14, 5, 3, 10, 6, 4, 19, 20], [10, 3, 15, 9, 11, 6, 13, 8, 10, 16, 6, 6, 15, 14, 2, 17, 11, 14, 8, 1, 14, 20], [4, 5, 15, 12, 6, 8, 4, 13, 14, 8, 19, 6, 11, 6, 16, 10, 15, 20, 2, 11, 2, 13], [2, 12, 5, 14, 3, 11, 5, 4, 15, 16, 1, 8, 14, 11, 19, 17, 11, 18, 4, 8, 13, 13], [1, 8, 5, 0, 16, 20, 2, 15, 12, 4, 3, 8, 14, 18, 14, 6, 7, 5, 4, 19, 13, 19], [12, 6, 7, 17, 14, 16, 10, 18, 6, 18, 19, 18, 9, 15, 14, 14, 12, 7, 5, 19, 11, 14], [12, 17, 12, 19, 7, 1, 11, 1, 7, 17, 17, 19, 3, 13, 5, 8, 19, 3, 17, 15, 1, 16], [0, 0, 11, 16, 16, 18, 5, 3, 18, 18, 5, 13, 12, 6, 5, 18, 3, 7, 7, 15, 20, 12], [2, 1, 15, 5, 17, 7, 18, 16, 9, 4, 7, 17, 10, 3, 20, 12, 17, 19, 3, 15, 16, 20], [12, 12, 1, 18, 0, 5, 7, 18, 14, 6, 8, 8, 19, 3, 3, 7, 2, 17, 2, 2, 2, 18], [9, 2, 9, 2, 5, 13, 0, 19, 16, 18, 10, 18, 2, 1, 0, 18, 0, 11, 8, 12, 6, 11], [3, 9, 3, 10, 2, 20, 0, 0, 16, 15, 3, 18, 19, 16, 3, 8, 10, 1, 3, 6, 6, 17], [17, 0, 15, 16, 9, 3, 1, 6, 7, 17, 15, 12, 9, 15, 6, 9, 20, 2, 5, 4, 20, 2], [5, 12, 9, 1, 19, 4, 4, 20, 20, 20, 17, 11, 0, 10, 20, 0, 11, 8, 11, 19, 10, 13], [8, 16, 14, 7, 19, 13, 11, 18, 3, 20, 16, 11, 1, 0, 14, 10, 7, 1, 15, 17, 12, 1], [0, 7, 11, 5, 11, 7, 19, 0, 20, 20, 8, 0, 9, 20, 15, 0, 9, 9, 16, 11, 0, 6], [1, 2, 6, 2, 9, 11, 12, 20, 20, 20, 7, 9, 7, 20, 9, 14, 14, 17, 1, 8, 10, 2], [13, 12, 7, 7, 5, 6, 4, 10, 9, 13, 6, 9, 4, 6, 10, 11, 2, 19, 1, 10, 15, 7]],
#             # [[8, 13, 4, 2, 20, 13, 11, 14, 3, 6, 9, 15, 20, 9, 17, 15, 2, 1, 12, 4, 11, 0], [6, 0, 20, 14, 11, 13, 12, 18, 14, 6, 18, 14, 10, 16, 0, 18, 9, 8, 2, 1, 14, 17], [5, 17, 2, 0, 16, 11, 2, 9, 14, 7, 2, 6, 10, 19, 0, 0, 12, 20, 17, 19, 10, 19], [1, 3, 14, 10, 20, 8, 20, 14, 12, 16, 15, 11, 3, 1, 9, 15, 9, 10, 9, 15, 17, 13], [13, 18, 13, 7, 12, 11, 10, 11, 6, 7, 16, 16, 12, 8, 2, 4, 4, 13, 14, 8, 1, 7], [2, 20, 2, 0, 14, 15, 6, 12, 18, 18, 4, 17, 12, 0, 14, 17, 9, 12, 11, 9, 7, 10], [11, 3, 6, 17, 14, 2, 5, 1, 19, 3, 17, 19, 12, 17, 16, 17, 10, 5, 4, 19, 7, 0], [11, 3, 17, 12, 2, 19, 6, 7, 7, 1, 17, 1, 14, 16, 6, 3, 5, 7, 11, 1, 18, 12], [4, 12, 16, 3, 18, 3, 17, 19, 2, 5, 3, 4, 5, 5, 18, 1, 7, 3, 4, 20, 7, 0], [20, 7, 15, 10, 17, 18, 0, 6, 11, 13, 20, 18, 16, 20, 9, 19, 20, 9, 16, 19, 15, 3], [15, 17, 15, 18, 10, 18, 19, 3, 1, 12, 8, 8, 11, 15, 3, 2, 15, 9, 20, 7, 4, 14], [0, 2, 0, 13, 15, 12, 8, 14, 15, 3, 19, 14, 8, 19, 18, 10, 18, 18, 11, 17, 10, 5], [3, 8, 16, 18, 0, 20, 20, 8, 12, 9, 2, 10, 8, 9, 10, 0, 19, 13, 8, 11, 0, 0], [0, 8, 13, 6, 4, 13, 13, 20, 16, 19, 5, 1, 15, 7, 16, 19, 18, 2, 5, 10, 6, 11], [8, 15, 14, 13, 6, 8, 18, 20, 8, 1, 10, 19, 13, 9, 2, 4, 15, 4, 6, 13, 7, 2], [13, 5, 0, 17, 20, 20, 0, 4, 18, 0, 10, 12, 7, 8, 4, 16, 1, 19, 13, 14, 11, 2], [19, 5, 20, 11, 9, 3, 13, 19, 11, 15, 8, 1, 4, 1, 17, 9, 6, 2, 3, 9, 11, 4], [14, 5, 6, 10, 1, 3, 16, 14, 17, 5, 11, 1, 7, 4, 12, 4, 16, 7, 7, 4, 9, 10], [3, 6, 0, 6, 4, 8, 8, 12, 16, 14, 20, 12, 7, 2, 15, 5, 20, 7, 1, 15, 2, 1], [13, 16, 10, 18, 3, 9, 17, 15, 13, 14, 19, 4, 5, 18, 5, 16, 1, 7, 6, 6, 3, 13], [8, 16, 5, 12, 6, 6, 5, 17, 15, 11, 19, 5, 12, 9, 16, 5, 16, 10, 5, 9, 10, 1]],
#             # [[0, 0, 2, 0, 0, 14, 13, 14, 4, 13, 6, 16, 4, 0, 4, 13, 9, 7, 20, 1, 7, 11], [10, 15, 8, 19, 2, 1, 4, 4, 6, 15, 13, 20, 3, 1, 15, 6, 10, 3, 9, 1, 4, 11], [15, 19, 6, 16, 17, 8, 2, 17, 8, 11, 1, 1, 20, 8, 7, 15, 11, 20, 0, 16, 10, 17], [15, 4, 19, 8, 14, 14, 5, 5, 3, 15, 8, 3, 12, 13, 11, 3, 13, 9, 11, 6, 6, 6], [0, 2, 7, 12, 19, 18, 3, 5, 5, 7, 8, 14, 0, 13, 1, 17, 5, 8, 16, 7, 4, 19], [20, 1, 4, 17, 13, 8, 19, 17, 1, 9, 8, 10, 7, 1, 19, 12, 8, 16, 18, 2, 10, 14], [4, 9, 1, 8, 5, 20, 3, 16, 20, 2, 10, 5, 18, 15, 8, 12, 17, 19, 13, 13, 2, 3], [16, 9, 6, 6, 16, 4, 8, 12, 14, 14, 8, 19, 14, 17, 10, 13, 3, 0, 9, 14, 19, 10], [8, 14, 9, 4, 18, 19, 12, 2, 2, 17, 9, 15, 7, 1, 12, 10, 20, 14, 17, 6, 13, 15], [5, 0, 9, 20, 11, 3, 12, 10, 7, 0, 7, 15, 0, 9, 13, 10, 18, 15, 20, 6, 0, 4], [1, 4, 8, 10, 6, 13, 14, 19, 7, 16, 9, 18, 14, 13, 2, 16, 7, 4, 6, 6, 18, 10], [16, 7, 17, 7, 3, 15, 6, 11, 7, 15, 19, 1, 2, 5, 17, 3, 5, 1, 19, 6, 1, 15], [8, 0, 15, 2, 17, 2, 12, 0, 7, 17, 17, 17, 9, 16, 20, 0, 1, 12, 7, 18, 18, 5], [16, 5, 4, 5, 17, 14, 17, 15, 5, 9, 20, 0, 20, 18, 3, 2, 3, 17, 9, 15, 0, 18], [3, 11, 2, 16, 5, 16, 15, 12, 17, 18, 19, 12, 3, 3, 4, 4, 11, 10, 0, 12, 13, 5], [5, 8, 13, 8, 18, 15, 5, 11, 10, 4, 19, 6, 9, 9, 13, 18, 14, 3, 3, 9, 2, 17], [12, 6, 19, 20, 4, 11, 12, 12, 12, 5, 18, 11, 16, 2, 20, 0, 12, 18, 14, 10, 18, 6], [9, 14, 11, 11, 11, 10, 7, 19, 1, 16, 2, 8, 16, 2, 14, 20, 6, 1, 0, 3, 18, 5], [10, 1, 16, 13, 2, 13, 12, 7, 10, 20, 11, 7, 7, 11, 11, 5, 1, 1, 18, 10, 20, 14], [20, 20, 9, 11, 2, 19, 12, 4, 5, 8, 18, 13, 15, 17, 0, 13, 20, 4, 2, 12, 16, 14], [11, 14, 3, 16, 3, 6, 15, 7, 16, 12, 10, 10, 20, 11, 9, 19, 19, 19, 6, 18, 18, 9]],
#             # [[15, 3, 8, 7, 15, 8, 16, 16, 0, 20, 10, 5, 3, 3, 7, 6, 20, 13, 2, 2, 5, 5], [14, 3, 8, 17, 11, 7, 14, 12, 2, 18, 17, 5, 5, 3, 5, 1, 17, 12, 14, 1, 11, 4], [14, 2, 8, 11, 15, 17, 11, 2, 4, 6, 6, 0, 17, 4, 0, 8, 18, 2, 9, 9, 20, 3], [6, 20, 5, 2, 19, 0, 3, 7, 12, 6, 3, 11, 14, 13, 14, 7, 7, 14, 1, 13, 13, 17], [6, 17, 12, 12, 8, 1, 8, 11, 16, 18, 17, 18, 9, 2, 6, 8, 5, 17, 13, 0, 13, 15], [6, 20, 4, 4, 10, 9, 3, 0, 20, 8, 2, 17, 1, 11, 1, 16, 10, 18, 20, 16, 15, 7], [16, 9, 12, 8, 10, 3, 3, 15, 14, 0, 0, 3, 6, 8, 18, 10, 10, 20, 0, 14, 0, 6], [11, 5, 4, 4, 0, 3, 11, 11, 0, 18, 1, 13, 3, 10, 10, 4, 12, 20, 15, 1, 12, 12], [2, 15, 19, 9, 19, 20, 13, 10, 5, 2, 2, 10, 13, 15, 1, 6, 17, 3, 7, 7, 18, 2], [16, 7, 9, 10, 2, 6, 9, 16, 8, 16, 10, 14, 12, 19, 3, 0, 7, 18, 19, 6, 2, 7], [14, 13, 1, 15, 18, 5, 19, 3, 7, 13, 1, 8, 15, 13, 12, 4, 10, 4, 0, 0, 11, 11], [14, 19, 17, 16, 9, 20, 12, 2, 17, 6, 8, 12, 8, 16, 9, 12, 11, 1, 19, 0, 9, 7], [2, 1, 15, 12, 11, 4, 11, 4, 13, 18, 16, 10, 13, 15, 20, 15, 17, 11, 11, 7, 16, 6], [16, 1, 7, 3, 17, 19, 13, 5, 19, 19, 19, 9, 5, 16, 17, 5, 19, 1, 10, 6, 16, 20], [11, 16, 18, 12, 13, 14, 11, 8, 4, 4, 15, 9, 17, 14, 9, 7, 19, 8, 14, 14, 6, 8], [6, 17, 4, 10, 20, 17, 13, 9, 4, 4, 12, 2, 5, 10, 14, 19, 7, 20, 15, 4, 3, 2], [19, 11, 14, 12, 7, 7, 13, 19, 10, 16, 1, 9, 19, 1, 19, 14, 15, 18, 15, 15, 19, 18], [18, 18, 10, 12, 5, 12, 18, 17, 17, 6, 5, 11, 6, 20, 19, 1, 9, 18, 1, 20, 9, 4], [8, 9, 11, 19, 0, 0, 3, 1, 5, 9, 10, 4, 8, 20, 0, 9, 13, 12, 14, 20, 9, 0], [8, 16, 18, 18, 13, 17, 0, 14, 18, 5, 5, 5, 16, 13, 3, 6, 15, 8, 7, 16, 15, 0], [1, 5, 20, 2, 20, 4, 7, 4, 10, 14, 3, 16, 20, 15, 10, 6, 13, 12, 2, 2, 1, 18]],
#         ]
# 
#         self.grids26x27 = [
#             [[0, 14, 22, 4, 4, 3, 23, 1, 7, 25, 16, 1, 15, 13, 14, 11, 10, 9, 4, 20, 25, 4, 18, 13, 18, 2, 22], [24, 7, 7, 13, 6, 13, 14, 23, 7, 16, 15, 23, 16, 13, 1, 18, 18, 14, 2, 2, 24, 24, 9, 13, 18, 9, 23], [25, 11, 25, 25, 17, 10, 20, 8, 13, 19, 20, 19, 9, 1, 13, 25, 15, 19, 12, 3, 2, 8, 4, 21, 21, 20, 24], [22, 25, 3, 8, 14, 25, 5, 10, 23, 10, 14, 7, 12, 20, 24, 7, 18, 16, 11, 3, 20, 1, 10, 20, 0, 2, 17], [0, 4, 1, 14, 10, 0, 5, 2, 16, 17, 11, 9, 6, 6, 11, 7, 22, 9, 1, 3, 9, 3, 4, 8, 4, 13, 1], [0, 8, 1, 1, 9, 20, 20, 23, 1, 17, 24, 1, 6, 15, 13, 3, 9, 14, 9, 7, 10, 25, 2, 5, 22, 12, 6], [0, 5, 24, 16, 15, 0, 19, 2, 15, 23, 15, 15, 9, 22, 7, 20, 12, 18, 2, 19, 25, 4, 7, 19, 11, 8, 11], [25, 5, 22, 5, 0, 6, 24, 7, 3, 25, 24, 23, 17, 16, 19, 19, 15, 11, 14, 9, 8, 1, 3, 24, 18, 0, 23], [17, 17, 23, 6, 24, 1, 9, 4, 19, 19, 11, 23, 6, 24, 5, 23, 16, 17, 4, 13, 8, 21, 17, 13, 11, 2, 6], [13, 8, 21, 22, 2, 14, 11, 8, 8, 5, 12, 2, 20, 11, 3, 5, 21, 9, 9, 16, 18, 10, 18, 9, 8, 8, 20], [1, 20, 5, 19, 0, 21, 1, 6, 9, 24, 17, 8, 21, 17, 21, 4, 14, 2, 22, 2, 8, 22, 20, 16, 3, 25, 12], [22, 11, 10, 0, 7, 8, 12, 3, 2, 12, 14, 0, 7, 1, 19, 24, 23, 25, 21, 22, 6, 8, 20, 19, 19, 4, 3], [18, 6, 24, 17, 11, 23, 16, 10, 9, 12, 3, 0, 12, 13, 22, 5, 17, 23, 1, 15, 15, 0, 5, 0, 18, 23, 3], [5, 1, 18, 10, 22, 7, 8, 20, 9, 3, 7, 15, 20, 2, 19, 5, 16, 19, 25, 20, 7, 14, 21, 18, 19, 1, 22], [25, 19, 15, 11, 10, 0, 23, 16, 5, 21, 8, 17, 2, 23, 18, 13, 17, 22, 14, 25, 13, 25, 10, 10, 21, 21, 8], [1, 7, 6, 0, 6, 5, 9, 14, 23, 22, 15, 18, 20, 18, 14, 14, 22, 9, 2, 5, 10, 15, 23, 2, 7, 6, 15], [25, 21, 4, 24, 3, 21, 0, 1, 7, 25, 15, 7, 23, 11, 11, 18, 24, 0, 1, 6, 22, 16, 19, 0, 14, 12, 0], [24, 19, 2, 7, 12, 2, 16, 2, 7, 16, 0, 13, 21, 2, 10, 6, 15, 3, 9, 23, 14, 3, 11, 3, 16, 16, 24], [11, 8, 18, 14, 8, 7, 18, 17, 6, 11, 13, 5, 5, 21, 1, 23, 14, 5, 21, 13, 5, 21, 9, 20, 12, 5, 8], [15, 4, 12, 6, 20, 12, 23, 17, 25, 5, 18, 12, 4, 14, 4, 24, 23, 21, 8, 4, 11, 12, 10, 12, 19, 0, 0], [15, 16, 12, 19, 8, 19, 11, 24, 15, 13, 1, 0, 3, 24, 20, 12, 24, 21, 25, 10, 6, 14, 10, 6, 17, 4, 2], [3, 19, 19, 14, 20, 18, 24, 12, 15, 24, 15, 14, 25, 12, 14, 13, 5, 22, 10, 12, 6, 18, 22, 5, 11, 16, 0], [8, 13, 6, 16, 12, 22, 16, 12, 21, 24, 5, 7, 11, 4, 10, 16, 5, 15, 21, 20, 4, 18, 22, 21, 7, 13, 20], [6, 2, 6, 16, 17, 10, 3, 6, 4, 15, 1, 21, 13, 12, 20, 16, 17, 23, 11, 4, 21, 25, 9, 9, 2, 3, 9], [7, 21, 15, 18, 11, 10, 8, 9, 24, 22, 12, 25, 17, 3, 10, 17, 20, 2, 19, 16, 16, 10, 10, 17, 6, 0, 1], [13, 13, 22, 3, 18, 25, 19, 18, 4, 4, 23, 7, 17, 22, 14, 17, 3, 15, 4, 17, 10, 13, 11, 17, 4, 22, 25]],
#         ]
# 
#         self.grids31x32 = [
#             [[23, 11, 24, 3, 11, 30, 21, 15, 24, 27, 29, 20, 8, 30, 23, 6, 0, 23, 19, 0, 2, 3, 7, 29, 20, 1, 14, 10, 9, 19, 21, 11], [23, 29, 0, 10, 19, 27, 19, 9, 14, 8, 8, 12, 1, 14, 12, 28, 13, 12, 30, 17, 10, 16, 16, 29, 8, 25, 8, 21, 23, 10, 27, 12], [19, 2, 19, 13, 11, 17, 1, 21, 3, 10, 24, 20, 14, 4, 19, 27, 3, 21, 25, 6, 20, 3, 24, 28, 20, 17, 6, 19, 29, 9, 5, 25], [21, 21, 8, 23, 5, 9, 27, 7, 27, 16, 13, 29, 4, 12, 11, 10, 0, 0, 14, 7, 2, 10, 25, 4, 11, 13, 26, 0, 30, 29, 3, 18], [17, 2, 19, 3, 1, 13, 27, 11, 7, 5, 15, 15, 1, 7, 1, 13, 8, 14, 16, 8, 2, 2, 29, 1, 25, 7, 30, 5, 5, 9, 2, 19], [15, 25, 19, 12, 8, 13, 1, 8, 30, 14, 15, 6, 6, 19, 23, 11, 0, 11, 13, 17, 6, 15, 30, 23, 18, 29, 9, 21, 7, 19, 23, 23], [25, 13, 23, 12, 9, 28, 5, 23, 30, 28, 1, 30, 21, 15, 21, 1, 4, 3, 28, 8, 0, 26, 25, 22, 2, 4, 4, 28, 0, 7, 0, 7], [8, 8, 9, 9, 16, 6, 15, 17, 26, 17, 3, 5, 27, 11, 16, 1, 17, 29, 19, 18, 30, 0, 15, 24, 20, 18, 16, 28, 27, 26, 8, 29], [9, 24, 16, 5, 13, 19, 27, 21, 22, 4, 25, 1, 19, 20, 5, 14, 17, 29, 6, 10, 28, 17, 12, 14, 11, 4, 17, 21, 26, 29, 30, 28], [7, 26, 6, 22, 14, 26, 18, 3, 24, 1, 26, 15, 30, 13, 29, 7, 4, 28, 26, 26, 11, 14, 24, 3, 10, 20, 20, 13, 19, 12, 19, 28], [12, 12, 8, 28, 24, 23, 0, 8, 30, 11, 7, 11, 26, 3, 17, 2, 20, 18, 24, 28, 20, 16, 20, 28, 21, 27, 18, 1, 12, 2, 5, 23], [22, 20, 9, 11, 11, 25, 23, 16, 26, 27, 24, 11, 17, 6, 18, 17, 13, 23, 2, 30, 25, 18, 11, 3, 28, 19, 29, 17, 27, 2, 8, 12], [29, 26, 29, 24, 25, 26, 16, 16, 24, 21, 8, 18, 26, 5, 5, 9, 16, 15, 16, 1, 15, 17, 22, 4, 10, 24, 4, 14, 3, 13, 10, 0], [9, 2, 29, 12, 9, 13, 1, 8, 17, 18, 8, 21, 14, 5, 5, 4, 25, 27, 25, 25, 19, 15, 13, 6, 19, 14, 17, 4, 29, 16, 23, 4], [13, 7, 0, 5, 26, 14, 5, 6, 25, 15, 13, 8, 12, 2, 11, 9, 29, 2, 24, 9, 13, 13, 18, 28, 27, 18, 17, 5, 16, 13, 9, 14], [26, 27, 9, 2, 30, 9, 14, 2, 15, 7, 0, 27, 1, 6, 22, 22, 8, 23, 17, 3, 30, 9, 10, 9, 14, 21, 8, 29, 12, 19, 4, 14], [21, 28, 16, 21, 25, 7, 1, 15, 20, 13, 8, 18, 25, 14, 12, 4, 13, 24, 12, 6, 14, 8, 14, 20, 15, 14, 15, 18, 27, 27, 27, 11], [12, 20, 29, 23, 24, 27, 18, 23, 4, 29, 5, 7, 28, 30, 9, 27, 10, 27, 22, 20, 24, 1, 30, 20, 3, 21, 0, 16, 5, 28, 3, 19], [14, 16, 3, 23, 30, 12, 22, 16, 24, 17, 2, 20, 18, 19, 1, 22, 5, 20, 6, 21, 16, 29, 4, 15, 2, 20, 5, 0, 25, 1, 22, 12], [24, 18, 29, 27, 12, 20, 6, 7, 3, 17, 18, 4, 2, 22, 1, 4, 13, 29, 17, 21, 2, 23, 5, 10, 22, 8, 4, 14, 6, 1, 22, 19], [12, 30, 13, 20, 0, 0, 1, 16, 1, 2, 22, 23, 1, 5, 15, 1, 7, 26, 29, 21, 0, 27, 15, 3, 13, 19, 7, 20, 28, 16, 3, 3], [21, 3, 3, 29, 26, 16, 5, 6, 26, 6, 10, 20, 21, 10, 22, 7, 2, 6, 6, 1, 6, 9, 15, 17, 30, 7, 30, 4, 15, 20, 22, 6], [4, 10, 16, 26, 6, 2, 12, 12, 17, 14, 0, 3, 6, 0, 21, 17, 2, 18, 9, 1, 6, 24, 6, 3, 0, 8, 27, 29, 24, 1, 10, 4], [23, 23, 23, 25, 28, 22, 24, 11, 21, 26, 18, 10, 2, 28, 25, 7, 28, 15, 16, 24, 11, 5, 11, 27, 11, 4, 18, 0, 24, 18, 19, 10], [26, 9, 17, 10, 4, 21, 19, 12, 12, 22, 20, 0, 5, 25, 7, 4, 30, 19, 8, 8, 20, 27, 22, 6, 0, 8, 12, 26, 2, 16, 25, 12], [9, 29, 14, 21, 20, 6, 24, 2, 20, 8, 17, 4, 5, 28, 7, 22, 22, 14, 30, 13, 18, 15, 3, 26, 26, 29, 6, 24, 11, 26, 10, 22], [12, 4, 28, 8, 13, 30, 10, 5, 0, 3, 9, 23, 18, 11, 28, 23, 10, 21, 30, 3, 18, 18, 9, 7, 11, 25, 26, 4, 16, 4, 0, 4], [14, 18, 19, 25, 24, 16, 7, 11, 24, 27, 9, 10, 2, 23, 15, 11, 0, 18, 10, 28, 19, 22, 18, 22, 11, 5, 1, 7, 6, 7, 9, 26], [14, 28, 16, 25, 22, 25, 20, 23, 26, 3, 22, 15, 27, 14, 16, 15, 25, 3, 28, 22, 14, 0, 1, 19, 17, 22, 7, 25, 12, 7, 21, 21], [30, 10, 30, 24, 26, 13, 5, 21, 15, 10, 18, 22, 30, 20, 2, 0, 27, 29, 10, 30, 30, 13, 11, 24, 9, 28, 11, 7, 15, 3, 26, 28], [15, 10, 12, 17, 25, 28, 5, 23, 16, 10, 17, 13, 23, 13, 6, 22, 22, 15, 18, 9, 5, 25, 17, 7, 30, 10, 25, 27, 0, 24, 2, 2]],
#         ]
# 
#         self.grids41x42 = [
#             [[4, 18, 29, 38, 35, 5, 34, 19, 33, 33, 30, 21, 19, 38, 9, 26, 18, 13, 26, 33, 15, 23, 35, 15, 15, 9, 11, 3, 22, 9, 5, 21, 23, 2, 16, 3, 29, 34, 31, 24, 34, 14], [6, 28, 31, 33, 21, 12, 40, 33, 22, 1, 20, 25, 22, 6, 12, 35, 31, 38, 30, 21, 8, 13, 20, 5, 19, 17, 23, 14, 6, 24, 39, 21, 2, 29, 18, 3, 36, 28, 38, 22, 19, 4], [36, 11, 40, 27, 19, 38, 16, 6, 34, 21, 4, 28, 7, 16, 1, 20, 28, 16, 27, 29, 17, 26, 10, 14, 15, 28, 9, 10, 18, 38, 6, 38, 34, 4, 15, 38, 17, 4, 19, 27, 15, 19], [27, 4, 25, 34, 0, 20, 5, 24, 11, 6, 40, 18, 35, 2, 23, 40, 3, 0, 37, 4, 21, 36, 2, 20, 22, 22, 0, 17, 31, 26, 6, 29, 34, 16, 34, 9, 32, 1, 25, 9, 20, 39], [40, 26, 17, 0, 11, 11, 40, 24, 30, 20, 28, 11, 35, 19, 30, 33, 35, 36, 4, 6, 13, 22, 10, 26, 20, 14, 36, 30, 10, 6, 32, 31, 5, 36, 1, 17, 33, 24, 4, 9, 13, 24], [11, 35, 21, 14, 7, 2, 34, 36, 23, 21, 37, 40, 18, 39, 34, 26, 37, 7, 20, 14, 17, 23, 12, 12, 40, 27, 20, 16, 29, 19, 14, 4, 9, 39, 1, 7, 11, 1, 7, 17, 2, 15], [3, 39, 13, 3, 19, 31, 39, 0, 18, 2, 16, 25, 11, 32, 28, 0, 11, 10, 5, 16, 19, 31, 32, 20, 14, 26, 21, 9, 9, 10, 39, 12, 37, 33, 31, 30, 35, 16, 34, 16, 12, 5], [1, 17, 26, 28, 28, 0, 10, 31, 30, 29, 20, 8, 13, 11, 29, 40, 40, 4, 27, 13, 20, 39, 26, 26, 35, 25, 1, 22, 21, 10, 22, 29, 22, 5, 16, 18, 26, 3, 25, 20, 35, 6], [19, 21, 38, 7, 24, 26, 6, 40, 24, 0, 8, 24, 25, 9, 6, 15, 18, 14, 15, 39, 2, 12, 12, 27, 11, 0, 9, 2, 18, 23, 16, 3, 39, 20, 25, 33, 35, 33, 17, 23, 30, 7], [11, 25, 21, 33, 16, 22, 15, 25, 10, 37, 13, 34, 2, 19, 30, 40, 7, 10, 0, 12, 35, 17, 36, 33, 23, 32, 19, 7, 32, 35, 36, 24, 16, 6, 31, 33, 20, 15, 29, 28, 8, 0], [3, 36, 3, 21, 13, 0, 27, 0, 10, 36, 36, 26, 0, 16, 28, 2, 20, 28, 39, 14, 38, 35, 22, 32, 9, 39, 2, 38, 25, 1, 17, 32, 36, 24, 1, 8, 2, 26, 32, 10, 1, 29], [23, 20, 4, 25, 5, 1, 31, 37, 37, 38, 34, 19, 3, 8, 19, 25, 29, 1, 26, 16, 15, 1, 36, 28, 29, 28, 30, 18, 26, 20, 39, 37, 36, 20, 9, 14, 2, 8, 38, 32, 0, 38], [30, 29, 2, 11, 32, 10, 40, 5, 36, 1, 6, 33, 23, 40, 13, 28, 22, 15, 8, 37, 14, 4, 23, 2, 3, 40, 21, 19, 27, 30, 21, 32, 3, 24, 20, 10, 2, 35, 18, 28, 12, 25], [31, 29, 29, 20, 26, 24, 8, 16, 37, 12, 13, 9, 11, 5, 37, 10, 25, 0, 16, 28, 38, 10, 34, 8, 34, 32, 11, 31, 6, 36, 31, 3, 9, 9, 26, 33, 0, 27, 3, 12, 13, 7], [30, 14, 32, 10, 8, 27, 8, 30, 24, 26, 32, 10, 30, 40, 3, 35, 34, 29, 8, 14, 35, 28, 5, 0, 31, 28, 12, 21, 26, 5, 36, 17, 40, 15, 18, 20, 7, 38, 3, 39, 29, 22], [25, 12, 6, 12, 25, 2, 13, 14, 31, 39, 28, 22, 15, 23, 39, 14, 28, 39, 14, 32, 2, 4, 35, 34, 32, 22, 30, 20, 24, 5, 22, 20, 32, 29, 21, 4, 24, 39, 12, 32, 16, 12], [20, 20, 24, 18, 2, 3, 10, 2, 1, 17, 23, 22, 26, 7, 39, 38, 12, 1, 24, 28, 8, 14, 6, 33, 18, 23, 15, 10, 17, 27, 39, 36, 7, 4, 0, 16, 16, 31, 22, 4, 10, 5], [22, 31, 13, 1, 36, 21, 25, 4, 18, 18, 26, 27, 36, 30, 12, 32, 40, 40, 37, 19, 4, 21, 23, 0, 13, 29, 12, 10, 11, 19, 10, 6, 7, 22, 26, 22, 34, 6, 11, 36, 37, 8], [1, 10, 11, 17, 25, 23, 6, 40, 33, 28, 21, 10, 10, 34, 31, 23, 33, 1, 30, 29, 34, 34, 38, 8, 21, 33, 0, 0, 7, 1, 26, 5, 21, 21, 13, 2, 18, 15, 3, 4, 38, 14], [34, 22, 21, 25, 40, 2, 14, 23, 7, 27, 27, 30, 13, 12, 1, 37, 15, 21, 27, 35, 10, 5, 25, 35, 29, 8, 14, 9, 29, 25, 14, 1, 28, 17, 15, 12, 2, 25, 21, 8, 8, 23], [20, 26, 15, 19, 29, 19, 17, 9, 26, 30, 15, 22, 19, 16, 7, 37, 8, 23, 17, 24, 2, 2, 40, 32, 25, 31, 29, 36, 5, 4, 3, 1, 2, 30, 6, 27, 40, 13, 19, 30, 2, 25], [4, 4, 8, 3, 31, 33, 0, 39, 9, 27, 32, 5, 39, 5, 26, 35, 35, 23, 37, 17, 40, 21, 15, 30, 30, 26, 17, 13, 31, 5, 8, 6, 5, 11, 27, 22, 33, 23, 37, 7, 3, 17], [24, 34, 14, 14, 26, 32, 30, 34, 5, 3, 35, 5, 25, 1, 21, 23, 3, 30, 34, 29, 34, 9, 10, 35, 39, 22, 13, 5, 4, 19, 31, 20, 22, 6, 0, 22, 17, 17, 33, 17, 39, 32], [5, 27, 39, 23, 19, 26, 15, 7, 40, 21, 8, 31, 31, 19, 34, 36, 20, 32, 6, 13, 7, 36, 25, 27, 23, 13, 0, 11, 4, 38, 16, 6, 26, 13, 6, 28, 18, 37, 14, 25, 33, 8], [25, 27, 39, 31, 38, 39, 31, 31, 38, 24, 20, 5, 15, 28, 11, 12, 3, 26, 38, 13, 27, 10, 18, 30, 40, 20, 38, 16, 3, 38, 5, 16, 27, 32, 31, 29, 34, 0, 32, 7, 29, 11], [11, 29, 14, 29, 2, 12, 18, 33, 25, 12, 28, 28, 27, 38, 24, 16, 4, 0, 9, 13, 29, 40, 23, 30, 37, 3, 4, 19, 27, 21, 38, 3, 18, 16, 24, 12, 40, 39, 0, 40, 9, 8], [28, 22, 1, 1, 25, 35, 23, 38, 36, 10, 22, 7, 31, 15, 6, 7, 23, 27, 38, 15, 19, 33, 16, 11, 36, 31, 12, 30, 4, 2, 5, 19, 24, 18, 8, 9, 8, 21, 2, 8, 17, 27], [37, 5, 11, 24, 20, 10, 34, 2, 24, 19, 39, 18, 32, 27, 40, 35, 13, 19, 32, 4, 28, 0, 14, 15, 12, 36, 16, 25, 22, 1, 14, 19, 35, 12, 13, 27, 7, 21, 20, 18, 13, 19], [39, 30, 5, 23, 39, 31, 29, 36, 14, 28, 3, 14, 20, 37, 4, 39, 33, 13, 26, 27, 27, 16, 36, 8, 36, 32, 39, 38, 15, 2, 9, 7, 35, 34, 38, 14, 27, 34, 34, 7, 9, 24], [1, 12, 2, 6, 37, 4, 37, 31, 3, 6, 40, 23, 37, 13, 26, 38, 33, 35, 36, 36, 6, 38, 1, 6, 30, 28, 8, 15, 9, 32, 22, 40, 17, 40, 10, 20, 24, 19, 11, 26, 35, 38], [17, 5, 7, 3, 16, 23, 0, 22, 17, 7, 36, 19, 25, 6, 14, 40, 12, 24, 29, 1, 28, 11, 33, 37, 9, 39, 15, 17, 12, 1, 0, 33, 34, 8, 16, 27, 10, 24, 39, 7, 34, 18], [32, 3, 34, 40, 8, 13, 2, 11, 23, 5, 14, 25, 9, 28, 7, 11, 11, 14, 18, 7, 0, 5, 33, 22, 14, 36, 17, 18, 22, 8, 9, 34, 7, 39, 21, 39, 18, 24, 0, 32, 10, 22], [25, 21, 11, 31, 17, 4, 31, 9, 12, 8, 19, 33, 29, 25, 27, 1, 35, 10, 21, 35, 15, 29, 1, 4, 33, 28, 40, 15, 10, 24, 28, 3, 6, 12, 7, 11, 16, 12, 34, 20, 22, 27], [27, 5, 5, 37, 21, 24, 24, 9, 17, 15, 40, 28, 3, 16, 36, 34, 23, 4, 8, 29, 6, 0, 36, 6, 11, 8, 19, 36, 32, 14, 5, 3, 8, 28, 17, 17, 4, 19, 35, 9, 38, 23], [31, 30, 18, 4, 32, 28, 22, 20, 16, 20, 20, 35, 38, 38, 7, 31, 15, 40, 23, 37, 19, 26, 11, 10, 10, 32, 2, 37, 13, 5, 33, 18, 31, 24, 4, 3, 4, 3, 5, 0, 40, 26], [5, 37, 33, 12, 3, 1, 40, 3, 33, 0, 32, 29, 39, 13, 6, 21, 13, 36, 9, 37, 33, 11, 16, 11, 36, 9, 9, 0, 20, 8, 21, 12, 24, 33, 31, 17, 17, 36, 16, 7, 34, 6], [29, 27, 1, 15, 29, 0, 23, 3, 22, 15, 7, 9, 5, 35, 39, 7, 15, 25, 32, 38, 38, 7, 33, 19, 16, 25, 18, 6, 11, 8, 24, 16, 26, 4, 30, 33, 32, 18, 10, 15, 37, 29], [18, 37, 17, 5, 39, 38, 8, 18, 20, 11, 35, 11, 16, 0, 39, 23, 18, 22, 22, 14, 0, 24, 0, 14, 0, 2, 7, 23, 17, 1, 6, 26, 38, 18, 3, 2, 32, 38, 35, 11, 14, 18], [10, 30, 35, 30, 16, 27, 13, 10, 13, 4, 14, 7, 24, 2, 31, 7, 40, 37, 35, 37, 18, 9, 9, 2, 15, 6, 24, 27, 32, 1, 30, 25, 33, 37, 9, 1, 23, 37, 8, 19, 17, 1], [37, 32, 28, 6, 1, 31, 13, 4, 6, 14, 37, 9, 1, 18, 33, 19, 28, 15, 31, 14, 30, 29, 12, 18, 34, 35, 34, 34, 30, 27, 9, 7, 8, 37, 30, 13, 33, 21, 23, 28, 13, 18], [24, 23, 13, 30, 4, 37, 22, 2, 17, 37, 25, 25, 12, 2, 21, 40, 13, 15, 29, 26, 12, 12, 10, 3, 17, 24, 11, 21, 35, 15, 30, 16, 35, 30, 39, 37, 26, 36, 13, 25, 12, 27]],
#         ]
# 
#         self.grids_by_size = {
#             4: self.grids4x5,
#             5: self.grids5x6,
#             6: self.grids6x7,
#             7: self.grids7x8,
#             8: self.grids8x9,
#             9: self.grids9x10,
#             10: self.grids10x11,
#             16: self.grids16x17,
#             21: self.grids21x22,
#             26: self.grids26x27,
#             31: self.grids31x32,
#             41: self.grids41x42,
#         }
# 
#     def loop_game_xxx(self, x: int | str):
#         grids = self.grids_by_size[x]
#         for grid in grids:
#             game_solver = DominosaSolver(Board(grid))
#             solution = game_solver.get_solution()
#             assert solution != {}
# 
#     def benchmark(self, x, loops_count):
#         y = x + 1
#         print(f"Starting benchmark for {x}x{y} grids")
#         grids = self.grids_by_size[x]
#         print(f"  runs {loops_count} loops of {len(grids)} boards")
#         execution_time = timeit.timeit(lambda: self.loop_game_xxx(x), number=loops_count)
#         print(f"  Average execution time : {execution_time / loops_count / len(grids):.3f} seconds")
#         print("Benchmark finished")
#         print("----------------------\n")
#         return execution_time
# 
#     def run_benchmarks(self):
#         size_loops_time = dict()
#         # size_loops_time[4] = [2, self.benchmark(4, 2)]
#         # size_loops_time[5] = [2, self.benchmark(5, 2)]
#         # size_loops_time[6] = [2, self.benchmark(6, 2)]
#         # size_loops_time[7] = [2, self.benchmark(7, 2)]
#         # size_loops_time[8] = [2, self.benchmark(8, 2)]
#         # size_loops_time[9] = [2, self.benchmark(9, 2)]
#         # size_loops_time[10] = [1, self.benchmark(10, 1)]
#         # size_loops_time[16] = [1, self.benchmark(16, 1)]
#         # size_loops_time[21] = [1, self.benchmark(21, 1)]
#         # size_loops_time[26] = [1, self.benchmark(26, 1)]
#         # size_loops_time[31] = [1, self.benchmark(31, 1)]
#         size_loops_time[41] = [1, self.benchmark(41, 1)]
# 
#         print()
#         print("----------------------")
#         total_executions_time = sum(loop_time[1] for loop_time in size_loops_time.values())
#         print(f"Total execution time: {total_executions_time:.3f} seconds")
#         print("Benchmark finished")
# 
# 
# if __name__ == '__main__':
#     benchmark = DominosaBenchmark()
#     benchmark.run_benchmarks()
