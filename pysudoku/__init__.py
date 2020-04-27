from . import sudoku
from . import examples

def load(cells):
    return sudoku.Sudoku(cells)
