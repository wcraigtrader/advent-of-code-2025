from __future__ import annotations

import re

from common import *
from operator import mul
from functools import reduce


@dataclass
class ProblemSet:

    ops1: list[str]
    data1: list[list[int]]
    ops2: list[str]
    data2: list[list[int]]

    def math(self, op: str, args: list[int]) -> int:
        if op == '+':
            return sum(args)
        elif op == '*':
            return reduce(mul, args, 1)
        else:
            raise ValueError(f'Unexpected opcode ({op})')

    def total(self, ops: list[str], data: list[list[int]]) -> int:
        results: list[int] = [self.math(ops[i], data[i]) for i in range(len(ops))]
        return sum(results)

    @classmethod
    def factory(cls, lines: list[str]) -> ProblemSet:
        ops1: list[str] = list(re.split(r' +', lines[-1].strip()))
        data1: list[list[int]] = [list(map(int, re.split(r' +', row.strip()))) for row in lines[0:-1]]
        data1 = list(map(list, zip(*data1)))

        ops2: list[str] = list(reversed(ops1))
        data2: list[list[int]] = []

        args: list[int] = []
        nums: int = len(lines)-1
        pos: int = len(lines[0])-2
        while pos >= 0:
            arg: str = ''.join([lines[i][pos] for i in range(nums)]).strip()
            if arg:
                args.append(int(arg))

            if lines[-1][pos] != ' ':
                data2.append(args)
                args = []

            pos -= 1

        return cls(ops1, data1, ops2, data2)


class Day06(Puzzle):
    """Solution for day 06 (Trash Compactor)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory_lines(filename, ProblemSet)

    def part1(self, data: ProblemSet) -> PuzzleResult:
        return data.total(data.ops1, data.data1)

    def part2(self, data: ProblemSet) -> PuzzleResult:
        return data.total(data.ops2, data.data2)


puzzle = Day06()
puzzle.run(4277556, 3263827)
