from __future__ import annotations

from collections.abc import MutableMapping, KeysView, ItemsView, ValuesView
from typing import Any, Callable, Iterator, Mapping, Optional, cast, TypeAlias  # noqa: F401
from math import sqrt


GridPosition: TypeAlias = complex
GridDirection: TypeAlias = complex
# GridPosition = GridDirection = complex

NORTH = UP = GridDirection(-1, 0)
SOUTH = DOWN = GridDirection(1, 0)
EAST = RIGHT = GridDirection(0, 1)
WEST = LEFT = GridDirection(0, -1)

NW: GridDirection = NORTH + WEST
NE: GridDirection = NORTH + EAST
SE: GridDirection = SOUTH + EAST
SW: GridDirection = SOUTH + WEST


def GridRow(position: GridPosition) -> int:
    return int(position.real)


def GridCol(position: GridPosition) -> int:
    return int(position.imag)


def GridOpposite(direction: GridDirection) -> GridDirection:
    return -direction


def GridOrthogonalDistance(src: GridPosition, tgt: GridPosition) -> int:
    return abs(GridRow(tgt)-GridRow(src))+abs(GridCol(tgt)-GridCol(src))


def GridDiagonalDistance(src: GridPosition, tgt: GridPosition) -> float:
    dx = GridCol(tgt) - GridCol(src)
    dy = GridRow(tgt) - GridRow(src)
    distance = sqrt(dx*dx + dy*dy)
    return distance


class Grid(MutableMapping):
    """Two-Dimensional Grid backed by a hash map with complex keys for locations"""

    _properties: list[str] = [
        '_rows',
        '_cols',
        '_offset',
        '_sparse',
        '_origin',
        '_default',
        '_dynamic',
    ]

    def __init__(self, source: Optional[list[str] | Grid] = None, **keywords) -> None:
        """
        Grid constructor
        
        :param source: Either a list of strings representing the initial data, or another Grid
        :type source: Optional[list[str] | Grid]
        :param keywords: Modify Grid behavior, as follows:

        * sparse: bool = False, If True, then only non-None values will be stored in the Grid.
        * offset: int = 0, A positive integer, which if set, extends the Grid boundaries in all directions.
        * origin: str = 'ul', Indicates where the origin of the grid is (ul = Upper Left, ll=Lower Left).
        * default: Any = None, Value to return for values that aren't represented in a sparse Grid
        * dynamic: bool = False, If True, Grid boundaries will expand as data is added, otherwise boundaries are fixed.
        * empty: bool = False, If True, when initializing from another Grid, will start with an empty grid instead of copying data.
        * transpose: bool = False, If True, when initializing, swap the row and column addresses.
        * conversion: Callable = None, If set, use this conversion on each element as the Grid is initialized
        """

        self._grid: dict[GridPosition, Any] = {}

        self._min_row: int = 1_000_000_000_000
        self._max_row: int = -1_000_000_000_000
        self._min_col: int = 1_000_000_000_000
        self._max_col: int = -1_000_000_000_000

        self._getop = 0
        self._setop = 0
        self._delop = 0

        if source is None:
            self._rows: int = keywords.get('rows', 0)
            self._cols: int = keywords.get('cols', 0)
            self._init(**keywords)
        elif issubclass(source.__class__, Grid):
            for p in self._properties:
                setattr(self, p, getattr(source, p))
            self._init(**keywords)
            empty: bool = keywords.get('empty', False)
            if not empty:
                self._grid = source._grid.copy()  # type: ignore
        elif isinstance(source, list):
            self._init(**keywords)
            self._parse(source, **keywords)
        elif isinstance(source, str):
            self._init(**keywords)
            self._parse(source.strip().split('\n'), **keywords)
        else:
            raise ValueError('Invalid source: {source}')

    def _init(self, **keywords) -> None:
        self._offset: int = keywords.get('offset', 0)
        self._sparse: bool = keywords.get('sparse', False)
        self._origin: str = keywords.get('origin', 'ul')
        self._default: Any = keywords.get('default', None)
        self._dynamic: bool = keywords.get('dynamic', False)

    def _parse(self, source: list[str], **keywords) -> None:
        transpose: bool = keywords.get('transpose', False)
        conversion: Callable = keywords.get('conversion', None)  # type: ignore

        rows: int = len(source)
        cols: int = len(source[0])

        self._rows: int = cols if transpose else rows
        self._cols: int = rows if transpose else cols

        for row, line in enumerate(source):
            for col, value in enumerate(line):
                r, c = row + self._offset, col + self._offset
                if transpose:
                    r, c = c, r
                if self._origin == 'll':
                    r = self._rows + self._offset - r

                if conversion:
                    value = conversion(value)

                if not (self._sparse and value is None):
                    self._grid[GridPosition(r, c)] = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._rows}, {self._cols})'

    def __getitem__(self, key: GridPosition) -> Any:
        if isinstance(key, GridPosition):
            if key in self._grid:
                self._getop += 1
                return self._grid[key]
            elif self._sparse:
                self._getop += 1
                return self._default
            else:
                raise IndexError
        raise KeyError

    def __setitem__(self, key: GridPosition, value: Any) -> None:
        if isinstance(key, GridPosition):
            self._grid[key] = value
            self._setop += 1
            if self._dynamic:
                self._min_row = min(self._min_row, GridRow(key))
                self._max_row = max(self._max_row, GridRow(key))
                self._min_col = min(self._min_col, GridCol(key))
                self._max_col = max(self._max_col, GridCol(key))
                self._rows = self._max_row - self._min_row + 1
                self._cols = self._max_col - self._min_col + 1
            return
        raise KeyError

    def __delitem__(self, key: GridPosition) -> None:
        if isinstance(key, GridPosition):
            if key in self._grid:
                del self._grid[key]
                self._delop += 1
                return
            elif self._sparse:
                self._delop += 1
                return
            else:
                raise IndexError
        raise KeyError

    def __contains__(self, key: GridPosition) -> bool:
        return key in self._grid

    def __len__(self) -> int:
        return len(self._grid)

    def __iter__(self) -> KeysView[GridPosition]:
        return KeysView(self._grid)

    def __eq__(self, other: Grid) -> bool:
        if any([getattr(self, p) != getattr(other, p) for p in self._properties]):
            return False

        if len(self._grid) != len(other._grid):
            return False

        return all([v == other._grid[k] for k, v in self._grid.items()])

    def __str__(self) -> str:
        rows: range = reversed(self.row_range) if self._origin == 'll' else self.row_range  # type: ignore
        lines: list[str] = [f'{r:3d}: {self.render_row(r)}' for r in rows]
        return '\n'.join(lines)

    def keys(self) -> KeysView[GridPosition]:
        return KeysView(self._grid)

    def values(self) -> ValuesView[Any]:
        return ValuesView(self._grid)

    def items(self) -> ItemsView[GridPosition, Any]:
        return ItemsView(self._grid)

    def clear(self) -> None:
        self._grid.clear()

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def center(self) -> GridPosition:
        if self._dynamic:
            row: int = (self._max_row - self._min_row) // 2 + self._min_row
            col: int = (self._max_col - self._min_col) // 2 + self._min_col
        else:
            row = self.rows // 2 + self._offset
            col = self.cols // 2 + self._offset
        return GridPosition(row, col)

    @property
    def row_range(self) -> range:
        if self._dynamic:
            return range(self._min_row, self._max_row+1)
        return range(self._offset, self._rows + self._offset)

    @property
    def col_range(self) -> range:
        if self._dynamic:
            return range(self._min_col, self._max_col+1)
        return range(self._offset, self._cols+self._offset)

    @property
    def lines(self) -> list[str]:
        return [self.render_row(r) for r in self.row_range]

    @property
    def operations(self) -> Mapping:
        return { 'set': self._setop, 'get': self._getop, 'del': self._delop }

    def render(self, value: Any) -> str:
        return ' ' if value is None else str(value)[0]

    def render_row(self, row: int) -> str:
        return ''.join([self.render(v) for v in self.row(row)])

    def row(self, r: int) -> list[Any]:
        return [self[GridPosition(r, c)] for c in self.col_range]

    def col(self, c: int) -> list[Any]:
        return [self[GridPosition(r, c)] for r in self.row_range]

    def inbounds(self, position: GridPosition) -> bool:
        return (GridRow(position) in self.row_range and GridCol(position) in self.col_range)


__all__: list[str] = [
    "Grid",
    "GridCol",
    "GridDirection",
    "GridDiagonalDistance",
    "GridOrthogonalDistance",
    "GridPosition",
    "GridRow",
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST",
    "UP",
    "RIGHT",
    "DOWN",
    "LEFT",
    "NW",
    "NE",
    "SE",
    "SW",
]
