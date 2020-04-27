# pysudoku

`pysudoku` is a small Python3 package designed to solve Sudoku puzzles using a
range of different techniques. If these techniques fail to solve the puzzle,
we fall back to using a backtracking algorithm.

### Quick Start

Loading and solving a Sodoku is easy;

```python
>>> import pysudoku
>>> sudoku = pysudoku.load([
  [2, 0, 0, 8, 0, 4, 0, 0, 6],
  [0, 0, 6, 0, 0, 0, 5, 0, 0],
  [0, 7, 4, 0, 0, 0, 9, 2, 0],
  [3, 0, 0, 0, 4, 0, 0, 0, 7],
  [0, 0, 0, 3, 0, 5, 0, 0, 0],
  [4, 0, 0, 0, 6, 0, 0, 0, 9],
  [0, 1, 9, 0, 0, 0, 7, 4, 0],
  [0, 0, 8, 0, 0, 0, 2, 0, 0],
  [5, 0, 0, 6, 0, 8, 0, 0, 1]])
>>> sudoku.solve()
```

To help get things up and running quickly there are `easy`, `medium`, and `hard`
puzzles included within the `pysudoku` package.

```python
>>> import pysudoku
>>> sudoku = pysudoku.load(pysudoku.examples.easy)
>>> sudoku.solve()
```

### Running interactively
Both the `solve` and `solve_with_backtracking` functions take an optional
`interactive` keyword argument. By calling `solve(interactive=True)` the Sudoku
board will be printed at each step along with so me information about the cell
and what decisions are being made.

[![asciicast](https://asciinema.org/a/324403.svg)](https://asciinema.org/a/324403)
