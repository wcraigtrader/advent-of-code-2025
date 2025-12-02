from __future__ import annotations

from common import *

import re


@dataclass
class Range:
    first: int
    last: int

    def __len__(self) -> int:
        return self.last-self.first+1

    @property
    def range(self):
        return range(self.first, self.last+1)

    @classmethod
    def parse(cls, text: str) -> Range:
        first, _, last = text.partition('-')
        return cls(int(first), int(last))


class Day02(Puzzle):
    """Solution for day 02 (Gift Shop)"""

    def parse_data(self, filename: str) -> Data:
        data: list[Range] = list(map(Range.parse, self.read_split(filename, ',')))
        return data

    def part1(self, data: Data) -> PuzzleResult:
        def match(number: int) -> bool:
            return re.fullmatch(r'([1-9][0-9]*)\1', str(number)) is not None

        ranges: list[range] = [d.range for d in data]
        matches: list[list[int]] = [list(filter(match, r)) for r in ranges]
        return sum([x for mlist in matches for x in mlist])

    def part2(self, data: Data) -> PuzzleResult:
        def match(number: int) -> bool:
            return re.fullmatch(r'([1-9][0-9]*)(\1)+', str(number)) is not None

        ranges: list[range] = [d.range for d in data]
        matches: list[list[int]] = [list(filter(match, r)) for r in ranges]
        return sum([x for mlist in matches for x in mlist])


puzzle = Day02()
puzzle.run(1227775554, 4174379265)
