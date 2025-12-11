from __future__ import annotations

from common import *
from collections import deque


@dataclass
class Node:
    name: str
    edges: list[str] = field(default_factory=list)
    paths: list[list[str]] = field(default_factory=list)

    def render(self) -> list[str]:
        return [f'"{self.name}" -> "{edge}"' for edge in self.edges]

    @classmethod
    def factory(cls, line: str) -> Node:
        name, _, edges = line.partition(': ')
        edges = edges.split(' ')
        return cls(name, edges)


class Reactor:

    def __init__(self, lines: str) -> None:
        self.nodes: dict[str, Node] = {}
        for line in lines:
            node: Node = Node.factory(line)
            self.nodes[node.name] = node
        self.nodes['out'] = Node('out')

    def render(self, filename: str, start: str, finish: str = 'out', stops: list[str] | None = None, nodes: dict[str, Node] | None = None):
        filename = 'src/day11/'+filename.replace('.data', '.dot')
        stops = stops or []
        nodes = nodes or self.nodes

        with open(filename, 'w') as dot:
            lf = '\n'
            br = '\n  '
            dot.write("digraph {\n")
            dot.write(f'  "{start}" [color=red]\n')
            for stop in stops:
                dot.write(f'  "{stop}" [color=blue]\n')
            dot.write('  "out" [color=red]\n')

            for node in self.nodes.values():
                dot.write(f"\n  {br.join(node.render())}{lf}")

            dot.write('}\n')

    def traverse(self, start: str, finish: str = 'out', stops: list[str] | None = None) -> int:
        stops = stops or []
        count = 0
        queue: deque[list[str]] = deque([[start]])
        while len(queue):
            path = queue.popleft()
            name = path[-1]
            if name == finish:
                if all([stop in path for stop in stops]):
                    count += 1
                    # print(count, history)
            else:
                node = self.nodes[name]
                for next in node.edges:
                    if next not in path:
                        queue.append(path+[next])

        print(f'{start} -> {stops} -> {finish} = {count}')
        return count


class Day11(Puzzle):
    """Solution for day 11 (Reactor)"""

    def parse_data(self, filename: str) -> Data:
        return self.read_factory(filename, Reactor)

    def part1(self, data: Reactor) -> PuzzleResult:
        data.render(self.currentfile, 'you')
        return data.traverse('you')

    def part2(self, data: Reactor) -> PuzzleResult:
        data.render(self.currentfile, 'svr', 'out', ['dac', 'fft'])
        # return data.traverse('svr', ['dac', 'fft'])

        p1 = data.traverse('svr', 'fft')
        p2 = data.traverse('fft', 'dac')
        p3 = data.traverse('dac', 'out')
        return p1 * p2 * p3


puzzle = Day11('real.data', 'test1.data', 'test2.data')
puzzle.run([5, None], [None, 2])
