from __future__ import annotations

from common import *
from typing import Any


@dataclass
class Present:
    id: int
    shape: Grid

    @staticmethod
    def convert(ch: str) -> Any:
        return 1 if ch == '#' else None

    @classmethod
    def factory(cls, lines: list[str]) -> Present:
        id = int(lines[0][0])
        shape = Grid(lines[1:4], sparse=True, conversion=cls.convert)
        return cls(id, shape)


@dataclass
class Region:
    x: int
    y: int
    presents: list[int]

    @classmethod
    def factory(cls, line: str) -> Region:
        size, _, quantities = line.partition(': ')
        x, _, y = size.partition('x')
        presents = list(map(int, quantities.split(' ')))
        return cls(int(x), int(y), presents)


class Trees:

    def __init__(self, lines):
        self.presents: list[Present] = [Present.factory(list(map(str.strip, lines[p:p+4]))) for p in range(0, 30, 5)]
        self.regions: list[Region] = [Region.factory(line) for line in lines[30:]]


class Day12(Puzzle):
    """Solution for day 12 (Christmas Tree Farm)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory_lines(filename, Trees)

    def part1(self, data: Trees) -> PuzzleResult:
        return 0

    def part2(self, data: Trees) -> PuzzleResult:
        return 0


puzzle = Day12()
puzzle.run(2)
