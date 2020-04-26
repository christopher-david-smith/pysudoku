import itertools
from .cell import Cell
from .logger import InteractiveLogger

class Sudoku:
    def __init__(self, sudoku):
        """
        Create a new Sudoku object

        arguments
        ---------
        sudoku : list
            A two dimensional list which represents a partially complete 
            sudoku grid
        """

        # Create list of Cell objects
        self.cells = []
        for r in range(9):
            for c in range(9):
                self.cells.append(Cell(r, c, sudoku[r][c], self.cells))
    
    @property
    def solved(self):
        """
        Returns True if all Cells in the Sudoku have been solved, or False if
        they have not
        """
        return True if all([c.solved for c in self.cells]) else False

    def solve(self, interactive=False):
        """
        Attempt to solve the Sudoku by using a range of techniques, falling
        back to using a backtracking algorithm if we fail

        arguments
        ---------
        interactive : boolean 
            Run interactively and print verbose messages at each step
        """

        while not self.solved:
            updated = False
            for cell in self.cells:
                if cell.solved:
                    continue

                if self.solve_cell(cell, interactive):
                    updated = True
            
            if not updated:
                break
        
        if not self.solved:
            self.solve_with_backtracking(interactive=interactive)

    def solve_cell(self, cell, interactive=False):
        """
        Solve a specific cell by using a range of techniques

        arguments
        ---------
        interactive : boolean   
            Run interactively and print verbose messages at each step
        """

        with InteractiveLogger(self, cell, interactive) as logger:

            # Run through each solving method in turn
            update = False
            update = self._identify_sole_candidate(cell, logger, update)
            update = self._identify_unique_candidate(cell, logger, update)
            update = self._identify_naked_subsets(cell, logger, update)
            update = self._identify_hidden_subsets(cell, logger, update)

            if not update:
                logger.log(f"No action taken on {repr(cell)}")

            return update
    
    def solve_with_backtracking(self, interactive=False):
        """
        Solve the Sudoku using only a backtracking algorithm, attempting to 
        solve each cell in turn by taking the first possible candidate, then
        continuing onto the next cell. When a point is reached where we cannot 
        continue we backtrack and choose the next possible candidate.

        arguments
        ---------
        interactive : bool
            Run interactively and print verbose messages at each step
        """

        for cell in self.cells:
            if cell.solved or cell.value != 0:
                continue
            
            related_cell_values = [c.value for c in cell.related_cells]
            for candidate in cell.candidates:
                if candidate not in related_cell_values:
                    with InteractiveLogger(self, cell, interactive) as logger:
                        logger.log(f"Updating {repr(cell)} to {candidate}")
                        cell.value = candidate

                    if self.solve_with_backtracking(interactive):
                        return True
            
            with InteractiveLogger(self, cell, interactive) as logger:
                logger.log(f"No valid candidates for {repr(cell)} - Backtracking")
                cell.value = 0
                return False

        return True

    def _identify_sole_candidate(self, cell, logger, update):
        """
        Attempt to update the specified Cell by looking for a sole candidate.
        A sole candidate is when there exists only one possible candidate 
        that can go in this Cell.

        arguments
        ---------
        cell : Cell                  
            Cell object to be updated

        logger : InteractiveLogger     
            InteractiveLogger object used to log messages

        update : boolean  
            Boolean to indicate if the Cell has been previously updated
        """

        if update:
            return True

        if len(cell.candidates) == 1:
            logger.log(f"Sole candidate '{cell.candidates[0]}' found")
            self._set_cell_value(cell, cell.candidates[0], logger)
            return True

    def _identify_unique_candidate(self, cell, logger, update):
        """
        Attempt to update the specified Cell by looking for a unique 
        candidate. A unique candidate is when a number can only exist in this
        Cell in the row, column, or square to which this Cell belongs.

        arguments
        ---------
        cell : Cell
            Cell object to be updated
        
        logger : InteractiveLogger
            InteractiveLogger object used to log messages

        update : boolean
            Boolean to indicate if the Cell has been previously updated
        """
        if update:
            return True

        for value in cell.candidates:
            
            for group, related_cells in cell.related_cells_as_dict.items():

                # Collate list of possible values for this row/column/square
                possible_candidates = []
                for related_cell in related_cells:
                    for candidate in related_cell.candidates:
                        possible_candidates.append(candidate)
                
                # If the value can't exist in the row/column/square then it
                # must be unique to this cell
                if value not in possible_candidates:
                    logger.log(f"Unique candidate '{value}' found in {group}")
                    self._set_cell_value(cell, value, logger)
                    return True

    def _identify_naked_subsets(self, cell, logger, update):
        """
        Look for naked subsets. A naked subset exists when there are at least 
        two cells that can only contain the same range of candidates. In this 
        case those candidates can be removed from all other cells in the row, 
        column, or square.

        arguments
        ---------
        cell : Cell
            Cell object to be updated

        logger : InteractiveLogger
            InteractiveLogger object used to log messages

        update : boolean
            Boolean to indicate if the Cell has been previously updated
        """
        
        if update:
            return True
       
        # Collate list of possible combinations
        combinations = []
        for subset in range(2, 4):
            if len(cell.candidates) not in range(2, subset + 1):
                continue
            
            tmp = list(itertools.combinations(cell.candidates, subset))
            combinations = combinations + tmp

        # Loop over related cells, then check each cell to see if it can only
        # contain the values in our combination. If it can contain anything 
        # else then it cannot be part of a naked subset.
        naked_subset_found = False
        for group, related_cells in cell.related_cells_as_dict.items():
            for combination in combinations:
                matches = [cell]
                for related_cell in related_cells:
                    if len(related_cell.candidates) not in range(2, len(combination)):
                        continue
                    
                    naked_cell_found = True
                    for value in related_cell.candidates:
                        if value not in combination:
                            naked_cell_found = False
                    
                    if naked_cell_found:
                        matches.append(related_cell)
                
                # The number of naked cells must match the number of values 
                # in the combination. For example a naked pair will have two
                # cells which can only contain (the same) two numbers.
                if len(matches) != len(combination):
                    continue
                
                cells_to_update = []
                for related_cell in related_cells:
                    if related_cell in matches or related_cell.solved:
                        continue
                    
                    cells_to_update.append(related_cell)
               
                if cells_to_update:
                    logger.log(f"Naked subset {combination} found in {group}")
                    naked_subset_found = True

                for value in combination:
                    self._remove_candidate_from_cells(cells_to_update, value, logger)
        
        return naked_subset_found       

    def _identify_hidden_subsets(self, cell, logger, update):
        """
        Look for hidden subsets. A hidden subset exists when N digits can only
        exist in N cells in a row, cell, or square. In this scenario all other
        candidates in those cells can be removed.

        arguments
        ---------
        cell : Cell
            Cell object to be updated

        logger : InteractiveLogger
            InteractiveLogger object used to log messages

        update : boolean
            Boolean to indicate if the Cell has been previously updated
        """

        if update:
            return True
       
        # Collate list of possible combinations
        combinations = []
        for subset in range(2, 4):
            tmp = list(itertools.combinations(cell.candidates, subset))
            combinations = combinations + tmp

        hidden_subset_found = False
        for group, related_cells in cell.related_cells_as_dict.items():
            for combination in combinations:
                matches = [cell]
                for related_cell in related_cells:
                    
                    hidden_cell_found = False
                    for value in related_cell.candidates:
                        if value in combination:
                            hidden_cell_found = True
                    
                    if hidden_cell_found:
                        matches.append(related_cell)
                
                if len(matches) != len(combination):
                    continue

                for match in matches:
                    for value in match.candidates.copy():
                        if value not in combination:
                            if not hidden_subset_found:
                                logger.log(f"Hidden subset {combination} "
                                           f"found in {group}")

                            hidden_subset_found = True
                            self._remove_candidate_from_cells(
                                [match],
                                value,
                                logger)

        return hidden_subset_found

    def _set_cell_value(self, cell, value, logger):
        """
        """

        cell.update_value(value, solved=True)
        logger.log(f"Cell ({repr(cell)}) updated to '{value}'")
        self._remove_candidate_from_cells(cell.related_cells, value, logger)

    def _remove_candidate_from_cells(self, cells, value, logger):
        """
        """
        for cell in cells:
            if value in cell.candidates:
                cell.remove_candidate(value)
                logger.log(f"Removed '{value}' from {repr(cell)}")

    def __str__(self):
        return (
            "+-------+-------+-------+\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "+-------+-------+-------+\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "+-------+-------+-------+\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "| {} {} {} | {} {} {} | {} {} {} |\n"
            "+-------+-------+-------+".format(*self.cells))
