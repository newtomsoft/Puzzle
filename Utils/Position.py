﻿from Direction import Direction


class Position:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def neighbors(self, mode='orthogonal') -> list['Position']:
        neighbors = [Position(self.r + 1, self.c), Position(self.r - 1, self.c), Position(self.r, self.c + 1), Position(self.r, self.c - 1)]
        if mode == 'diagonal':
            neighbors.extend([Position(self.r + 1, self.c + 1), Position(self.r + 1, self.c - 1), Position(self.r - 1, self.c + 1), Position(self.r - 1, self.c - 1)])
        return neighbors

    def direction_to(self, other: 'Position') -> Direction:
        if other is None or self == other:
            return Direction(Direction.NONE)
        if self.r == other.r:
            if self.c < other.c:
                return Direction(Direction.RIGHT)
            return Direction(Direction.LEFT)
        if self.r < other.r:
            return Direction(Direction.DOWN)
        return Direction(Direction.UP)

    def direction_from(self, other: 'Position') -> Direction:
        return other.direction_to(self)

    @property
    def left_neighbor(self):
        return Position(self.r, self.c - 1)

    @property
    def right_neighbor(self):
        return Position(self.r, self.c + 1)

    @property
    def up_neighbor(self):
        return Position(self.r - 1, self.c)

    @property
    def down_neighbor(self):
        return Position(self.r + 1, self.c)

    @property
    def up_left_neighbor(self):
        return Position(self.r - 1, self.c - 1)

    @property
    def up_right_neighbor(self):
        return Position(self.r - 1, self.c + 1)

    @property
    def down_left_neighbor(self):
        return Position(self.r + 1, self.c - 1)

    @property
    def down_right_neighbor(self):
        return Position(self.r + 1, self.c + 1)

    def __eq__(self, other):
        return isinstance(other, Position) and self.r == other.r and self.c == other.c

    def __hash__(self):
        return hash((self.r, self.c))

    def __str__(self):
        return f'({self.r}, {self.c})'

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Position(self.r + other.r, self.c + other.c)

    def __sub__(self, other):
        return Position(self.r - other.r, self.c - other.c)

    def __mul__(self, other):
        return Position(self.r * other, self.c * other)

    def __truediv__(self, other):
        return Position(self.r / other, self.c / other)

    def __floordiv__(self, other):
        return Position(self.r // other, self.c // other)

    def __mod__(self, other):
        return Position(self.r % other, self.c % other)

    def __lt__(self, other):
        return self.r < other.r or (self.r == other.r and self.c < other.c)

    def __le__(self, other):
        return self.r <= other.r or (self.r == other.r and self.c <= other.c)

    def __gt__(self, other):
        return self.r > other.r or (self.r == other.r and self.c > other.c)

    def __ge__(self, other):
        return self.r >= other.r or (self.r == other.r and self.c >= other.c)

    def __getitem__(self, item):
        return self.r if item == 0 else self.c

    def __setitem__(self, key, value):
        if key == 0:
            self.r = value
        else:
            self.c = value

    def __iter__(self):
        return iter([self.r, self.c])

    def __neg__(self):
        return Position(-self.r, -self.c)
