from __future__ import annotations

from collections import deque

from common import *

SPLITTER = '^'
PATH = '|'


class Tachyon:

    def __init__(self, lines):
        self.manifold = Grid(lines, sparse=True, conversion=Grid.conv_blank('.'))

    def tachyon_manifold(self) -> int:
        splits = 0
        queue: deque[GridPosition] = deque([self.manifold.first])
        while len(queue):
            next: GridPosition = queue.popleft() + DOWN
            if next in self.manifold and self.manifold[next] == SPLITTER:
                split = False

                left: GridPosition = next+LEFT
                if left not in self.manifold:
                    self.manifold[left] = PATH
                    queue.append(left)
                    split = True

                right: GridPosition = next+RIGHT
                if right not in self.manifold:
                    self.manifold[right] = PATH
                    queue.append(right)
                    split = True

                if split:
                    splits += 1

            elif GridRow(next) <= self.manifold.rows:
                if next not in self.manifold:
                    self.manifold[next] = PATH
                    queue.append(next)

        return splits

    @cache
    def count_paths(self, position) -> int:
        while position in self.manifold and self.manifold[position] != SPLITTER:
            position += DOWN

        if self.manifold[position] == SPLITTER:
            return self.count_paths(position+LEFT)+self.count_paths(position+RIGHT)
        else:
            return 1

    def quantum_tachyon_manifold(self) -> int:
        return self.count_paths(self.manifold.first)


class Day07(Puzzle):
    """Solution for day 07 (Laboratories)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory(filename, Tachyon)

    def part1(self, data: Tachyon) -> PuzzleResult:
        return data.tachyon_manifold()

    def part2(self, data: Tachyon) -> PuzzleResult:
        return data.quantum_tachyon_manifold()


puzzle = Day07()
puzzle.run(21, 40)
