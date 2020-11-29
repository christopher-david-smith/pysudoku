import os

class InteractiveLogger:
    def __init__(self, sudoku, cell, interactive=False):
        self.sudoku = sudoku
        self.cell = cell
        self.interactive = interactive
        self.messages = ["Running in interactive mode, press enter to continue"]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):

        if not self.interactive:
            return

        os.system("clear")
        with self.cell.highlighted():
            lines_in_sudoku = str(self.sudoku).split("\n")

        line_count = max(len(lines_in_sudoku), len(self.messages))

        print()
        print("  Sudoku                     |  Messages")
        print("  ---------------------------|---------------------------")
        for index in range(line_count):

            try:
                sudoku_line = lines_in_sudoku[index]
            except IndexError:
                sudoku_line = " " * 25

            try:
                message = self.messages[index]
            except IndexError:
                message = ""

            print(f"  {sudoku_line}  |  {message}")

        input()

    def log(self, message):

        self.messages.append(message)
