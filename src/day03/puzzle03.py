from __future__ import annotations

from common import *


class Day03(Puzzle):
    """Solution for day 03 (Lobby)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_stripped(filename)

    def part1(self, data: Data) -> PuzzleResult:
        return sum(self.joltage(batteries, 2) for batteries in data)

    def part2(self, data: Data) -> PuzzleResult:
        return sum(self.joltage(batteries, 12) for batteries in data)

    @staticmethod
    def joltage(batteries: str, count: int) -> int:
        result: str = ''
        pos = 0
        for end in range(len(batteries)-count+1, len(batteries)+1):
            biggest: str = max(batteries[pos:end])
            pos: int = batteries.index(biggest, pos, end) + 1
            result = result + biggest
        return int(result)


puzzle = Day03()
puzzle.run(357, 3121910778619)
