from __future__ import annotations

from math import sqrt
from operator import attrgetter
from common import *


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    z: int

    def distance(self, other: Box) -> float:
        return sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)

    def nearest(self, boxes: list[Box]) -> Box:
        nearest = boxes[0]
        closest = self.distance(nearest)
        for box in boxes[1:]:
            distance = self.distance(box)
            if distance < closest:
                nearest = box
                closest = distance
        return nearest

    @classmethod
    def factory(cls, line) -> Box:
        x, y, z = line.split(',')
        return cls(int(x), int(y), int(z))


@dataclass
class Pair:
    a: Box
    b: Box

    @property
    def distance(self) -> float:
        return sqrt((self.a.x - self.b.x)**2 + (self.a.y - self.b.y)**2 + (self.a.z - self.b.z)**2)

    def __repr__(self) -> str:
        return f'Pair({self.a.x},{self.a.y},{self.a.z}--{self.b.x},{self.b.y},{self.b.z} = {self.distance})'


Circuit = set


class Playground:

    def __init__(self, lines):
        self.boxes: list[Box] = [Box.factory(line) for line in lines]
        self.pairs: list[Pair] = []
        for this, a in enumerate(self.boxes):
            self.pairs.extend([Pair(a, b) for b in self.boxes[this+1:]])

        self.pairs.sort(key=attrgetter('distance'))

    def __len__(self) -> int:
        return len(self.boxes)

    def connect(self) -> int:
        limit: int = 1000 if hasattr(self, 'datatype') and getattr(self, 'datatype') == 'real' else 10

        lookup: dict[Box, Circuit] = {}
        for box in self.boxes:
            lookup[box] = set([box])
        circuits: list[Circuit] = list(lookup.values())

        for pair in self.pairs[:limit]:
            circuit_a = lookup[pair.a]
            circuit_b = lookup[pair.b]

            if circuit_a == circuit_b:
                continue

            elif len(circuit_a) > len(circuit_b):
                circuit_a |= circuit_b
                for box in circuit_b:
                    lookup[box] = circuit_a
                circuits.remove(circuit_b)

            else:
                circuit_b |= circuit_a
                for box in circuit_a:
                    lookup[box] = circuit_b
                circuits.remove(circuit_a)

        circuits.sort(key=lambda x: len(x), reverse=True)

        return len(circuits[0])*len(circuits[1])*len(circuits[2])

    def distance(self) -> int:
        lookup: dict[Box, Circuit] = {}
        for box in self.boxes:
            lookup[box] = set([box])
        circuits: list[Circuit] = list(lookup.values())

        for pair in self.pairs:
            circuit_a = lookup[pair.a]
            circuit_b = lookup[pair.b]

            if circuit_a == circuit_b:
                continue

            elif len(circuit_a) > len(circuit_b):
                circuit_a |= circuit_b
                for box in circuit_b:
                    lookup[box] = circuit_a
                circuits.remove(circuit_b)

            else:
                circuit_b |= circuit_a
                for box in circuit_a:
                    lookup[box] = circuit_b
                circuits.remove(circuit_a)

            if len(circuits) == 1:
                break

        return pair.a.x * pair.b.x


class Day08(Puzzle):
    """Solution for day 08 (Playground)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory_lines(filename, Playground)

    def part1(self, data: Playground) -> PuzzleResult:
        return data.connect()

    def part2(self, data: Playground) -> PuzzleResult:
        return data.distance()


puzzle = Day08()
puzzle.run(40, 25272)
