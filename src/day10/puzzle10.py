from __future__ import annotations

from collections import deque
from multiprocessing import Pool

from common import *

BINARY = str.maketrans('.#', '01')


@dataclass
class Machine:
    lights: str
    buttons: list[list[int]]
    joltage: list[int]
    goal: int
    ops: list[int]
    jolts: list[list[int]]

    @property
    def size(self) -> int:
        return len(self.ops)

    def light_presses(self) -> int:
        queue: deque[tuple[int, int]] = deque([(0, 1)])
        while True:
            state, depth = queue.popleft()
            states = [state ^ op for op in self.ops]
            if self.goal in states:
                return depth
            queue.extend([(s, depth+1) for s in states])

    def power_presses(self) -> int:
        start = [0]*len(self.joltage)
        queue: deque[tuple[list[int], int]] = deque([(start, 1)])
        while True:
            current, depth = queue.popleft()
            joltages = [[c+j for c, j in zip(current, self.jolts[b])] for b in range(self.size)]
            if self.joltage in joltages:
                return depth
            queue.extend([(j, depth+1) for j in joltages])

    @classmethod
    def factory(cls, line: str) -> Machine:
        groups: list[str] = line.split(' ')

        size: int = len(groups[0][1:-1])

        lights: str = groups[0][1:-1].translate(BINARY)
        buttons: list[list[int]] = [list(map(int, g[1:-1].split(','))) for g in groups[1:-1]]
        joltage: list[int] = [int(j) for j in groups[-1][1:-1].split(',')]

        goal = int(lights, 2)

        ops: list[int] = []
        jolts: list[list[int]] = []
        for button in buttons:
            op = ['0']*size
            jolt = [0]*size
            for b in button:
                op[b] = '1'
                jolt[b] = 1
            ops.append(int(''.join(op), 2))
            jolts.append(jolt)

        return cls(lights, buttons, joltage, goal, ops, jolts)


class Day10(Puzzle):
    """Solution for day 10 (Factory)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory_list(filename, Machine)

    @staticmethod
    def indicate(machine: Machine):
        results = machine.light_presses()
        return results

    def part1(self, data: Data) -> PuzzleResult:
        with Pool() as pool:
            presses = pool.map(self.indicate, data)
        return sum(presses)

    @staticmethod
    def joltage(machine: Machine) -> int:
        results = machine.power_presses()
        return results

    def part2(self, data: Data) -> PuzzleResult:
        # with Pool(1) as pool:
        #     presses = pool.map(self.joltage, data)
        # return sum(presses)
        return 0


puzzle = Day10()
puzzle.run(7, 33)
