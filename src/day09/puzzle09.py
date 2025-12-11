from __future__ import annotations

from common import *


RED = '#'
GREEN = 'X'


class MovieTheater:

    def __init__(self, lines):
        self.grid: Grid = Grid(sparse=True, dynamic=True, default='.')
        for col, row in [line.split(',') for line in lines]:
            self.grid[int(row), int(col)] = RED

    def __len__(self) -> int:
        return len(self.grid)

    def largest_square(self) -> int:
        largest: int = 0
        positions: list[complex] = self.grid.find(RED)
        for index, left in enumerate(positions[:-1]):
            for right in positions[index:]:
                area: int = GridArea(left, right)
                if area > largest:
                    largest = area

        return largest


class Day09(Puzzle):
    """Solution for day 09 (Movie Theater)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory_lines(filename, MovieTheater)

    def part1(self, data: MovieTheater) -> PuzzleResult:
        # print(f'             : part1 {len(data.grid)} => {data.grid.rows} x {data.grid.cols}')
        print(f'             : part1 {data.grid}')
        return data.largest_square()

    def part2(self, data: MovieTheater) -> PuzzleResult:
        return 0


puzzle = Day09()
puzzle.run(50, 24)
