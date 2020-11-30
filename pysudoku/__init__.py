from . import sudoku
from . import boards 

def load(cells):
    return sudoku.Sudoku(cells)
