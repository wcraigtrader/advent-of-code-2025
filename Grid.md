## Grid Concepts

Many of the AoC puzzles are best solved using a mutable sparse grid. As an example, here is some test data:

```
    .......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ...............
```

As a traditional doubly-nested list, this would require 240 `str` objects, plus 16 row `list` objects, and 1 grid `list` object. for a total of **257** objects.

Assuming that the dots (`.`) represent empty spaces, you could represent this as a map with a row-column tuples as the keys, which would require 23 objects for the values (`S` and `^`), 23 key `tuple` objects, each having a row and column object, and of course the map object itself, for a total **93** objects.

We can do better by using `complex` numbers as the keys by using the `real` portion as the row, and the `imag` portion as the column, for a total of **47** objects.

## Grid constructor

`Grid(source: Optional[list[str] | Grid] = None, **keywords)`

* source: Either a list of strings representing the initial data, or another Grid

keywords:

* `sparse`: bool = False, If True, then only non-None values will be stored in the Grid.
* `offset`: int = 0, A positive integer, which if set, extends the Grid boundaries in all directions.
* `origin`: str = 'ul', Indicates where the origin of the grid is (ul = Upper Left, ll=Lower Left).
* `default`: Any = None, Value to return for values that aren't represented in a sparse Grid
* `dynamic`: bool = False, If True, Grid boundaries will expand as data is added, otherwise boundaries are fixed.
* `empty`: bool = False, If True, when initializing from another Grid, will start with an empty grid instead of copying data.
* `transpose`: bool = False, If True, when initializing, swap the row and column addresses.
* `conversion`: Callable = None, If set, use this conversion on each element as the Grid is initialized

## Grid behaviors

A `Grid` is a collection, more specifically, a `MutableMapping`. Thus the normal map behaviors can be expected. The map key can either be a `GridPosition` or `GridDirection`, or a `tuple[int, int]` for row, col.

