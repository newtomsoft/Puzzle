﻿from abc import ABC, abstractmethod

from Utils.Grid import Grid


class GameSolver(ABC):
    @abstractmethod
    def get_solution(self) -> Grid:
        pass

    @abstractmethod
    def get_other_solution(self) -> Grid:
        pass
