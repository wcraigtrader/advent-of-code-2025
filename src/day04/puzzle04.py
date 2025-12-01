from __future__ import annotations

from common import *


class Day04(Puzzle):
    """Solution for day 04"""

    def parse_data(self, filename: str) -> Data:
        return self.read_stripped(filename)

    def part1(self, data: Data) -> PuzzleResult:
        return 0

    def part2(self, data: Data) -> PuzzleResult:
        return 0


puzzle = Day04()
puzzle.run()
