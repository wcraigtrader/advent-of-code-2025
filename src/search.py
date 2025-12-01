from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heapify, heappop, heappush, heappushpop, heapreplace  # noqa: F401
from operator import gt, lt, add, sub
from typing import Any, Callable, Optional


@dataclass(order=True, unsafe_hash=True)
class SearchNode:
    """A node wrapper for Searching

    This class is hashable, but hashes only on the node.
    This class is sortable, but only on the cost.
    """

    node: Any = field(compare=False, hash=True)
    cost: float = field(compare=True, hash=False, default=0.0)
    previous: Optional[SearchNode] = field(compare=False, default=None, repr=False)

    def __eq__(self, other: SearchNode) -> bool:
        return self.node == other.node


class BaseSearch:
    """Base class that provides common operations
    for using SearchNodes that are wrappers around a generic node
    """

    @property
    def unseen(self) -> int:
        return 999_999_999

    def _clear(self) -> None:
        self._search_node_map: dict[Any, SearchNode] = {}

    def _find(self, node: Any) -> SearchNode:
        if node not in self._search_node_map:
            self._search_node_map[node] = SearchNode(node, self.unseen)
        return self._search_node_map[node]

    def _solution(self, current: SearchNode) -> list[Any]:
        path: list[Any] = [current.node]

        while current.previous:
            current = current.previous
            path.append(current.node)

        path.reverse()

        return path

    def previous(self, node: Any) -> Any:
        if node in self._search_node_map:
            prev: Optional[SearchNode] = self._search_node_map[node].previous
            if prev:
                return prev.node
        return None

    def neighbors(self, node: Any) -> list[Any]:
        """Return a list of all of the neighbors of a node"""
        raise NotImplementedError('neighbors function')

    def search(self, origin: Any, *target: Any) -> Optional[list[Any]]:
        """Return a list representing the path from the origin to a target"""
        raise NotImplementedError('search function')


# class UniformCostSearch(BaseSearch):
#     """Implement the uniform-cost search algorithm

#     Each node in the search graph / grid gets wrapped in a SearchNode
#     as it becomes visible in the search.

#     Use this as a mixin and implement the `neighbors` method(s).
#     Call `search` to get the optimum list of nodes traversed.

#     Notes: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Practical_optimizations_and_infinite_graphs
#     """

#     def search(self, origin: Any, *target: Any) -> Optional[list[Any]]:
#         self._clear()

#         s_origin: SearchNode = self._find(origin)
#         s_target: list[SearchNode] = list(map(self._find, target))

#         frontier: list[SearchNode] = []
#         expanded: list[SearchNode] = []

#         heappush(frontier, s_origin)

#         while len(frontier):
#             current: SearchNode = heappop(frontier)
#             if current in s_target:
#                 return self._solution(current)

#             expanded.append(current)

#             for node in self.neighbors(current.node):
#                 neighbor: SearchNode = self._find(node)
#                 if neighbor not in expanded and neighbor not in frontier:
#                     neighbor.previous = current
#                     heappush(frontier, neighbor)
#                 else:
#                     try:
#                         i: int = frontier.index(neighbor)
#                         if frontier[i].cost


class AstarSearch(BaseSearch):
    """Implement the A* search algorithm for Any type of node

    Each node in the search graph / grid gets wrapped in a SearchNode
    as it becomes visible in the search.

    Use this as a mixin and implement the `neighbors`, `distance`, and `heuristic` methods.
    Call `search` to get the optimum list of nodes traversed.

    Notes: https://en.wikipedia.org/wiki/A*_search_algorithm
    """

    def distance(self, src: Any, dst: Any) -> float:
        """Distance between two neighboring nodes"""
        raise NotImplementedError('distance function')

    def heuristic(self, node: Any) -> float:
        """Estimate the cost to get to the goal from a node"""
        raise NotImplementedError('heuristic function')

    @property
    def comparison(self) -> Callable:
        return lt

    @property
    def addition(self) -> Callable:
        return add

    def search(self, origin: Any, *target: Any) -> Optional[list[Any]]:

        self._clear()

        s_origin: SearchNode = self._find(origin)
        s_target: list[SearchNode] = list(map(self._find, target))

        frontier: list[SearchNode] = []
        heappush(frontier, s_origin)

        cheapest: dict[SearchNode, float] = defaultdict(lambda: self.unseen)
        cheapest[s_origin] = 0

        while len(frontier):
            current: SearchNode = heappop(frontier)
            if current in s_target:
                return self._solution(current)

            for node in self.neighbors(current.node):
                neighbor: SearchNode = self._find(node)
                tentative: float = self.addition(cheapest[current], self.distance(current.node, neighbor.node))
                if self.comparison(tentative, cheapest[neighbor]):
                    cheapest[neighbor] = tentative
                    neighbor.previous = current
                    neighbor.cost = self.addition(tentative, self.heuristic(neighbor.node))
                    if neighbor not in frontier:
                        heappush(frontier, neighbor)

        return None


class LongestSearch(AstarSearch):

    @property
    def unseen(self) -> int:
        return -super().unseen

    @property
    def comparison(self) -> Callable:
        return gt

    @property
    def addition(self) -> Callable:
        return sub


__all__: list[str] = ["SearchNode", "AstarSearch", "LongestSearch"]
