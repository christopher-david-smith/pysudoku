#!/usr/bin/python3

from sudokusolver import SudokuSolver
import time

sudoku = []
sudoku.append([
    [5, 3, 8, 0, 1, 6, 0, 7, 9],
    [0, 0, 0, 3, 8, 0, 5, 4, 1],
    [2, 4, 1, 5, 0, 0, 0, 0, 0],
    [0, 6, 0, 9, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 5, 0, 9, 0],
    [0, 9, 0, 0, 0, 4, 0, 0, 2],
    [6, 0, 0, 2, 0, 0, 9, 3, 0],
    [1, 2, 9, 0, 4, 0, 0, 5, 0],
    [0, 5, 4, 6, 9, 0, 0, 0, 8]
])

sudoku.append([
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

sudoku.append([
    [0, 0, 0, 0, 3, 7, 6, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 9, 0],
    [0, 0, 8, 0, 0, 0, 0, 0, 4],
    [0, 9, 0, 0, 0, 0, 0, 0, 1],
    [6, 0, 0, 0, 0, 0, 0, 0, 9],
    [3, 0, 0, 0, 0, 0, 0, 4, 0],
    [7, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 1, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 2, 5, 4, 0, 0, 0, 0]
])

sudoku.append([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 8, 5],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 7, 3],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 9]
])

while True:

    print((
        "Select a sudoku to solve:\n"
        " 1. Easy\n"
        " 2. Medium\n"
        " 3. Hard\n"
        " 4. Extreme\n"
        " x. Exit\n"
    ))

    selection = input(":> ")

    if selection in ["1", "2", "3", "4"]:
        print("Solving sudoku...")
        solver = SudokuSolver(sudoku[int(selection) - 1])
        start = time.time()
        solver.solve()
        solver.pretty_print()
        end = time.time()
        print("Time taken: {} seconds".format(int(end) - int(start)))
        break

    if selection in ["x", "X"]:
        exit()
