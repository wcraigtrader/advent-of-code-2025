from __future__ import annotations

from typing import Any

from common import *


NEIGHBORS: list[GridDirection] = [NORTH, SOUTH, WEST, EAST, NW, NE, SW, SE]


class Rolls(Grid):

    def __init__(self, lines):
        # Use a sparse grid with a 1-deep border, using 1 for rolls, and 0 for empty spaces
        super().__init__(lines, sparse=True, offset=1, conversion=self.conversion, default=0)

    def is_accessible(self, position) -> bool:
        return self[position] and (sum([self[position+offset] for offset in NEIGHBORS]) < 4)

    @property
    def accessible(self) -> list[GridPosition]:
        return list(filter(self.is_accessible, self.keys()))

    def remove_accessible(self) -> int:
        positions: list[GridPosition] = self.accessible
        for pos in positions:
            self[pos] = 0
        return len(positions)

    @staticmethod
    def conversion(ch: str) -> Any:
        return 1 if ch == '@' else None


class Day04(Puzzle):
    """Solution for day 04 (Printing Department)"""

    def parse_data(self, filename: str) -> Data:
        return Rolls(self.read_stripped(filename))

    def part1(self, data: Rolls) -> PuzzleResult:
        return len(data.accessible)

    def part2(self, data: Rolls) -> PuzzleResult:
        total = 0
        removed: int = data.remove_accessible()
        while removed:
            total += removed
            removed = data.remove_accessible()

        return total


puzzle = Day04()
puzzle.run(13, 43)
