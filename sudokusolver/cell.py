from contextlib import contextmanager
from termcolor import colored

class Cell:
    def __init__(self, row, column, value, cells):
        """
        Create a new Cell object

        arguments
        ---------
        row : int
            Row to which this cell belongs

        column : int
            Column to which this cell belongs

        value : int 
            The inital value of the cell

        cells : list 
            Other cells that belong to the Sudoku board
        """

        # Default cell values
        self._row = row
        self._column = column
        self._highlighted = False
        self.value = value

        # Store information about other cells on the Sudoku board
        self._other_cells = cells

        # Store information about the status of this Cell
        self.solved = False if value == 0 else True
        self.changed = False
        self._candidates = []

    @property
    def candidates(self):
        """
        Return a list of possible candidates for this Cell
        """

        if not self._candidates and not self.solved:
            for value in range(1, 10):
                values = [c.value for c in self.related_cells if c.solved]
                if value not in values and value not in self._candidates:
                    self._candidates.append(value)
        
        return self._candidates
    
    def update_value(self, value, solved=False):
        """
        """

        self.changed = True
        if solved:
            self.solved = True
            self._candidates = []

        self.value = value

    def remove_candidate(self, value):
        """
        """

        if value in self.candidates:
            self._candidates.remove(value)
        
    @property
    def related_cells(self):
        """
        Get all the related cells in the same row, column, and square as this
        Cell object
        """
        cells = set()
        for list_of_cells in self.related_cells_as_dict.values():
            for cell in list_of_cells:
                cells.add(cell)
        
        return cells

    @property
    def related_cells_as_dict(self):
        """
        Get all the related cells in the same row, column, and square as this
        Cell object and return them as a dictionary
        """
        return {
            'row': self.other_cells_in_row,
            'column': self.other_cells_in_column,
            'square': self.other_cells_in_square}

        
    @property
    def other_cells_in_row(self):
        """
        Get all the related cells in the same row as this Cell object
        """

        cells = []
        start, end = 9 * self._row, (9 * self._row) + 9
        for current_cell in self._other_cells[start:end]:
            if current_cell == self:
                continue

            cells.append(current_cell)
        
        return cells

    @property
    def other_cells_in_column(self):
        """
        Get all the related cells in the same column as this Cell object
        """
        
        cells = []
        indexes = [self._column + (9 * row) for row in range(9)]
        for index in indexes:
            if self._other_cells[index] == self:
                continue
            
            cells.append(self._other_cells[index])
        
        return cells

    @property
    def other_cells_in_square(self):
        """
        Get all the related cells in the same square as this Cell object
        """
        
        cells = []
        for r in range(3):
            for c in range(3):
                row_index = self._row - (self._row % 3)
                col_index = self._column - (self._column % 3)
                
                index = (9 * row_index) + col_index + (r * 9) + c
                if self._other_cells[index] == self:
                    continue

                cells.append(self._other_cells[index])

        return cells
        
    @contextmanager
    def highlighted(self):
        """
        """
        self._highlighted = True
        try:
            yield
        finally:
            self._highlighted = False

    def __repr__(self):
        """
        """
        
        return ("sudokusolver.Cell("
                f"row={self._row}, "
                f"column={self._column}, "
                f"candidates={self.candidates}, "
                f"value={self.value} "
                f"solved={self.solved})")

    def __str__(self):
        """
        """

        # Set the cell value
        cell_value = str(self.value)
        if self.value == 0:
            cell_value = "-"
        
        if self._highlighted:
            return colored(cell_value, "blue")
        
        if self.changed is True and self.solved is False:
            return colored(cell_value, "yellow")

        if self.changed is True and self.solved is True:
            return colored(cell_value, "green")

        return colored(cell_value, "white")
