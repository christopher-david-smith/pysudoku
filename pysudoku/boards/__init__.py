import sys
import random
from ..sudoku import Sudoku


class __boards(object):

    easy = Sudoku([
        [2, 0, 0, 8, 0, 4, 0, 0, 6],
        [0, 0, 6, 0, 0, 0, 5, 0, 0],
        [0, 7, 4, 0, 0, 0, 9, 2, 0],
        [3, 0, 0, 0, 4, 0, 0, 0, 7],
        [0, 0, 0, 3, 0, 5, 0, 0, 0],
        [4, 0, 0, 0, 6, 0, 0, 0, 9],
        [0, 1, 9, 0, 0, 0, 7, 4, 0],
        [0, 0, 8, 0, 0, 0, 2, 0, 0],
        [5, 0, 0, 6, 0, 8, 0, 0, 1]
    ])

    medium = Sudoku([
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 1, 0, 0, 0, 6],
        [0, 4, 0, 0, 2, 0, 0, 3, 0],
        [1, 0, 0, 0, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 0, 0, 4, 0, 0],
        [2, 0, 0, 6, 0, 0, 0, 0, 8],
        [0, 9, 0, 0, 7, 0, 0, 4, 0],
        [7, 0, 0, 0, 8, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0]
    ])

    @property
    def random(self):

        # Generate a random (filled) board
        def pattern(r, c): return (3 * (r % 3) + r // 3 + c) % 9
        rbase = [i for i in range(3)]
        rows = [g * 3 + r for g in rbase for r in rbase]
        cols = [g * 3 + c for g in rbase for c in rbase]
        nums = random.sample(range(1, 10), 9)
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # Flatten board into a list of cells and record their position
        cells = []
        for ri, row in enumerate(board):
            for ci, col in enumerate(row):
                cells.append((ri, ci, row[ci]))

        # Randomise cell positions, then iterate over each cell and set it to
        # 0 and see if the puzzle is solvable. If it isn't, set the cell back
        # to its original value and continue.
        random.shuffle(cells)
        for index, cell in enumerate(list(cells)):
            original_value = cell[2]
            cells[index] = (cell[0], cell[1], 0)

            tmp_board = [[0 for _ in range(9)] for _ in range(9)]
            for tmp_cell in cells:
                r, c, v = tmp_cell
                tmp_board[r][c] = v

            sudoku = Sudoku(tmp_board)
            if not sudoku.solve(fallback_to_bruteforce=False):
                cells[index] = (cell[0], cell[1], original_value)

        # Once we've got to this part we've removed as many cells as possible
        # whilst ensuring the puzzle is solvable, return the puzzle
        random_board = [[0 for _ in range(9)] for _ in range(9)]
        for cell in cells:
            r, c, v = cell
            random_board[r][c] = v

        return Sudoku(random_board)

sys.modules[__name__] = __boards()
