from typing import Dict, Tuple

from Utils.Direction import Direction
from Utils.Position import Position


class Island:
    def __init__(self, position: Position, bridges: int, positions_bridges: Dict[Position, int] = None):
        self.position = position
        self.bridges_count = bridges
        if bridges < 0 or bridges > 8:
            raise ValueError("Bridges must be between 0 and 8")
        self.direction_position_bridges: Dict[Direction, Tuple[Position, int]] = {}
        if positions_bridges is not None:
            for position, bridges in positions_bridges.items():
                self.set_bridge(position, bridges)

    def set_bridge(self, position: Position, number: int):
        direction = self.position.direction_to(position)
        self.direction_position_bridges[direction] = position, number

    def set_bridges_count_according_to_directions_bridges(self):
        self.bridges_count = sum([bridges for (_, bridges) in self.direction_position_bridges.values()])

    def has_no_bridge(self):
        return self.bridges_count == 0

    def __eq__(self, other):
        return self.position == other.position and self.bridges_count == other.bridges_count and self.direction_position_bridges == other.direction_position_bridges

    def __repr__(self):
        return f"{self.bridges_count} ; {self.direction_position_bridges}"