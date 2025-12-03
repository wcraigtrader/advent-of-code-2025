from __future__ import annotations

from common import *


class Day03(Puzzle):
    """Solution for day 03"""

    def parse_data(self, filename: str) -> Data:
        return self.read_stripped(filename)

    def part1(self, data: Data) -> PuzzleResult:
        return sum(self.rating(batteries, 2) for batteries in data)

    def part2(self, data: Data) -> PuzzleResult:
        return sum(self.rating(batteries, 12) for batteries in data)

    @staticmethod
    def rating(batteries: str, count: int) -> int:
        value = 0
        pos = 0
        for end in range(len(batteries)-count+1, len(batteries)+1):
            biggest: str = max(batteries[pos:end])
            pos: int = batteries.index(biggest, pos, end) + 1
            value: int = value * 10 + int(biggest)
        return value


puzzle = Day03()
puzzle.run(357, 3121910778619)
