from __future__ import annotations

from common import *


ROLL = '@'
SURROUNDING: list[GridDirection] = [NORTH, SOUTH, WEST, EAST, NW, NE, SW, SE]


class Rolls(Grid):

    def __init__(self, lines):
        super().__init__(lines, offset=1, sparse=True, conversion=self.conversion, default=0)

    @staticmethod
    def conversion(ch: str) -> int:
        return 1 if ch == ROLL else 0

    def is_accessible(self, position) -> bool:
        return self[position] and (sum([self[position+offset] for offset in SURROUNDING]) < 4)

    @property
    def accessible(self) -> list[GridPosition]:
        return list(filter(self.is_accessible, self.keys()))

    @property
    def total_accessible(self) -> int:
        return len(self.accessible)

    def remove_accessible(self) -> int:
        positions: list[complex] = self.accessible
        for pos in positions:
            self[pos] = 0
        return len(positions)


class Day04(Puzzle):
    """Solution for day 04 (Printing Department)"""

    def parse_data(self, filename: str) -> Data:
        return Rolls(self.read_stripped(filename))

    def part1(self, data: Rolls) -> PuzzleResult:
        return data.total_accessible

    def part2(self, data: Rolls) -> PuzzleResult:
        total = 0
        removed: int = data.remove_accessible()
        while removed:
            total += removed
            removed = data.remove_accessible()

        return total


puzzle = Day04()
puzzle.run(13, 43)
