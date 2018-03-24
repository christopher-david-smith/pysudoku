import copy
from termcolor import colored


class SudokuSolver:
    '''
    '''

    def __init__(self, sudoku):
        '''
        '''
        self.original = copy.deepcopy(sudoku)
        self.rows = copy.deepcopy(sudoku)

    def pretty_print(self):
        '''
        '''
        self._print_sudoku(self.rows)

    def _print_sudoku(self, rows, row_index=None, cell_index=None):
        '''
        '''
        numbers = []
        for r, row in enumerate(rows):
            for c, cell_value in enumerate(row):

                original_cell = self.original[r][c]
                colour = 'white'
                attributes = []

                # Colour highlighted cell
                if (r is row_index) and (c is cell_index):
                    colour = 'red'
                    attributes = ['bold']

                # Colour found numbers
                elif original_cell is not cell_value:
                    colour = 'green'
                    attributes = ['bold']

                numbers.append(colored("{} ".format(cell_value), colour,
                               attrs=attributes))

        # Decoration
        border_output = " +------+------+------+\n"
        row_output = " |{}{}{}|{}{}{}|{}{}{}|\n"

        # Generate and print sudoku board
        output = ((border_output + (row_output * 3)) * 3 + border_output)
        print(output.format(*numbers))

        return

    def is_valid(self, rows=None):
        '''
        '''
        if rows is None:
            rows = self.rows

        columns = self._transpose(rows)
        squares = []

        for rindex in [0, 3, 6]:
            for cindex in [0, 3, 6]:
                squares.append(self._return_square(rows, rindex, cindex))

        for numbers_list in [rows, columns, squares]:
            for numbers in numbers_list:
                if self._are_numbers_valid(numbers) is False:
                    return False

        return True

    def solve(self, method="backtracking"):
        '''
        '''
        if method == "backtracking":
            self.rows = self._solve_with_backtracking(self.rows)[0]

    def _solve_with_backtracking(self, rows):
        '''
        '''
        for row_index, row in enumerate(rows):
            for col_index, number in enumerate(row):
                if number is 0:

                    possible_values = self._return_missing_numbers(
                        rows, row_index, col_index)
                    if not possible_values:
                        possible_values = range(1, 10)

                    for possible_value in possible_values:

                        rows[row_index][col_index] = possible_value
                        valid_guess = self.is_valid(rows)

                        if valid_guess:
                            tmp_rows, valid = self._solve_with_backtracking(
                                rows)

                            if valid is True:
                                return tmp_rows, True

                        if possible_value is possible_values[-1]:
                            rows[row_index][col_index] = 0
                            return rows, False

        return rows, True

    def _transpose(self, list_to_transpose):
        '''
        '''
        return list(map(list, zip(*list_to_transpose)))

    def _are_numbers_valid(self, numbers):
        '''
        '''
        seen_numbers = []
        for number in numbers:
            if number in seen_numbers:
                return False

            if number is not 0:
                seen_numbers.append(number)

        return True

    def _return_square(self, rows, row_index, column_index):
        '''
        '''
        row_index_start = row_index - (row_index % 3)
        col_index_start = column_index - (column_index % 3)

        square = []
        for row in rows[row_index_start:row_index_start + 3]:
            for number in row[col_index_start:col_index_start + 3]:
                square.append(number)

        return square

    def _return_missing_numbers(self, rows, row_index, column_index):
        '''
        '''
        columns = self._transpose(rows)
        square = self._return_square(rows, row_index, column_index)

        seen_numbers = []
        for numbers in [rows[row_index], columns[column_index], square]:
            for number in numbers:
                if number is not 0 and number not in seen_numbers:
                    seen_numbers.append(number)

        missing_numbers = []
        for number in range(1, 10):
            if number not in seen_numbers:
                missing_numbers.append(number)

        return missing_numbers
