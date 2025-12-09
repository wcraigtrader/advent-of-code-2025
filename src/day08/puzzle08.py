from __future__ import annotations

from math import sqrt
from common import *


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int

    def distance(self, other: JunctionBox) -> float:
        return sqrt(
            (other.x - self.x ^ 2) + (other.y - self.y ^ 2) + (other.z - self.z) ^ 2
        )

    @classmethod
    def factory(cls, line) -> JunctionBox:
        x, y, z = line.split(',')
        return cls(int(x), int(y), int(z))


@dataclass
class Distance:
    link: tuple[int, int]
    boxes: 

class Playground:

    def __init__(self, lines):
        self.boxes: list[JunctionBox] = [JunctionBox.factory(line) for line in lines]


class Day08(Puzzle):
    """Solution for day 08 (Playground)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory_lines(filename, Playground)

    def part1(self, data: Data) -> PuzzleResult:
        return 0

    def part2(self, data: Data) -> PuzzleResult:
        return 0


puzzle = Day08()
puzzle.run(40)
