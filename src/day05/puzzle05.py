from __future__ import annotations

from operator import attrgetter

from common import *


@dataclass
class Inventory:
    ranges: list[range]
    ingredients: list[int]

    @classmethod
    def factory(cls, lines: list[str]) -> Inventory:
        ranges: list[range] = []
        ingredients: list[int] = []

        # Parse input lines
        for line in lines:
            if line == '':
                continue
            elif '-' in line:
                start, _, stop = line.partition('-')
                ranges.append(range(int(start), int(stop)+1))
            else:
                ingredients.append(int(line))

        # Combine ranges
        ranges.sort(key=attrgetter('start'))
        pos: int = 0
        while pos < len(ranges)-1:
            curr: range = ranges[pos]
            next: range = ranges[pos+1]

            if next.start not in curr:
                pos += 1
                continue

            combined = range(min(curr.start, next.stop), max(curr.stop, next.stop))
            # print(f'combined {curr} and {next} => {combined}')

            ranges[pos] = combined
            del ranges[pos+1]

        return cls(ranges, ingredients)

    def __len__(self) -> int:
        return len(self.ranges)


class Day05(Puzzle):
    """Solution for day 05 (Cafeteria)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory(filename, Inventory)

    def part1(self, data: Inventory) -> PuzzleResult:
        result = 0
        for i in data.ingredients:
            if any(i in r for r in data.ranges):
                result += 1

        return result

    def part2(self, data: Inventory) -> PuzzleResult:

        return sum([len(r) for r in data.ranges])


puzzle = Day05()
puzzle.run(3, 14)
