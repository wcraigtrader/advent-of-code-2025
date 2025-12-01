from __future__ import annotations

from common import *


@dataclass
class Rotation:
    direction: str
    rotation: int

    @property
    def offset(self) -> int:
        return self.rotation if self.direction == 'R' else -self.rotation

    @classmethod
    def parse(cls, text: str) -> Rotation:
        d = text[0]
        r: int = int(text[1:])
        return cls(d, r)


class Day01(Puzzle):
    """Solution for day 01"""

    def parse_data(self, filename: str) -> Data:
        return [Rotation.parse(line) for line in self.read_stripped(filename)]

    def part1(self, data: Data) -> PuzzleResult:
        dial: int = 50
        zero: int = 0

        for rotation in data:
            dial += rotation.offset
            dial = dial % 100
            if dial == 0:
                zero += 1

        return zero

    def part2(self, data: Data) -> PuzzleResult:
        dial: int = 50
        zero: int = 0

        for rotation in data:
            turn: int = rotation.offset
            prev: int = dial
            next: int = prev + turn
            dial = next % 100

            wrap: int = 0
            if next == 0:
                wrap = 1
            elif next < 0:
                wrap = (-next) // 100
                wrap = wrap if prev == 0 else wrap+1
            elif next > 99:
                wrap = next // 100
            zero += wrap

            # print(f'{prev=} {turn=} {next=} {dial=} {wrap=} {zero=}')

        return zero


puzzle = Day01()
puzzle.run(3, 6)
