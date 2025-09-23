import copy

from PySide6.QtCore import QObject, Signal
import threading
from collections import deque
from enum import Enum
import time


class Result(Enum):
    SOLVED: int = 1
    NO_SOLUTION: int = 2
    NO_PROGRESS: int = 3


class Board(QObject):
    change = Signal()
    stop = False

    def __init__(self, cells=None):
        super().__init__()
        self.worker = None
        if cells:
            self.cells = cells
        else:
            self.cells = [{1, 2, 3, 4} for _ in range(16)]

    @classmethod
    def from_string(cls, string):
        cells = []
        for c in string:
            if c not in "1234":
                cells.append(set(range(1, 5)))
            else:
                cells.append(int(c))
        return cls(cells)

    @classmethod
    def from_file(cls, path):
        with open(path) as file:
            content = file.read()
        return cls.from_string(eval(content))

    @property
    def rows(self):
        return [self.cells[i:i + 4] for i in range(0, 16, 4)]

    @property
    def columns(self):
        return [self.cells[i::4] for i in range(4)]

    @staticmethod
    def get_index(row: int, col: int) -> int:
        return row * 4 + col

    def get_cell(self, row: int, col: int):
        return self.cells[self.get_index(row, col)]

    def set_cell(self, row: int, col: int, value):
        self.cells[self.get_index(row, col)] = value

    def __str__(self):
        result = ""
        for row in self.rows:
            for cell in row:
                if type(cell) == set:
                    result += "- "
                else:
                    result += f"{str(cell)} "
            result += "\n"
        return result

    def solve_background(self):
        self.worker = threading.Thread(target=self.solve,
                                       name="Sudoku Solver")
        self.worker.start()

    def hidden_single(self, row: int, col: int):
        if type(self.cells[row * 4 + col]) != set:
            return False
        # is there a number that only exists in this cell but nowhere else in the row or column?
        cell = set(self.cells[row * 4 + col])
        self.cells[row * 4 + col] = None
        for num in cell:
            found = {num in s for s in self.rows[row] if type(s) == set}
            found &= {num in s for s in self.columns[col] if type(s) == set}
            if not any(found):
                self.cells[row * 4 + col] = num
                return True
        self.cells[row * 4 + col] = cell
        return False

    def naked_single(self, row: int, col: int) -> bool:
        cell = self.cells[row * 4 + col]
        line_found = {num for num in self.rows[row] if type(num) == int}
        col_found = {num for num in self.columns[col] if type(num) == int}
        cell -= line_found
        cell -= col_found
        return self.clean_up()

    def naked_pairs(self, row: int, col: int) -> bool:
        success = False
        # does this line have 2 equal sets of size 2?
        other_cells = [self.cells[row * 4 + c] for c in range(4) if c != col]
        two_element_sets = [s for s in other_cells if type(s) == set and len(s) == 2]
        two_equals = [s for s in two_element_sets if two_element_sets.count(s) > 1]
        if two_equals:
            #  remove these two numbers if possible
            cell = self.cells[row * 4 + col]
            for s in two_equals:
                if type(cell) == set and len(cell) > 2:
                    cell -= s
                    success = True
            self.cells[row * 4 + col] = cell
        # does this column have 2 equal sets of size 2?
        other_cells = [self.cells[r * 4 + col] for r in range(4) if r != row]
        two_element_sets = [s for s in other_cells if type(s) == set and len(s) == 2]
        two_equals = [s for s in two_element_sets if two_element_sets.count(s) > 1]
        if two_equals:
            #  remove these two numbers if possible
            cell = self.cells[row * 4 + col]
            for s in two_equals:
                if type(cell) == set and len(cell) > 2:
                    cell -= s
                    success = True
            self.cells[row * 4 + col] = cell
        success |= self.clean_up()
        return success

    def clean_up(self) -> bool:
        for row in range(4):
            for col in range(4):
                cell = self.cells[row * 4 + col]
                if type(cell) == set and len(cell) == 1:
                    self.cells[row * 4 + col] = cell.pop()
                    return True
        return False

    def solve(self) -> Result:
        result = Result.NO_SOLUTION
        made_progress = False
        for row in range(4):
            for col in range(4):
                cell = self.cells[row * 4 + col]
                if type(cell) == set:
                    orig_val = cell.copy()

                    # try solving cell with three methods
                    made_progress |= self.naked_single(row, col)
                    made_progress |= self.naked_pairs(row, col)
                    made_progress |= self.hidden_single(row, col)

                    # anything changed (reduced options)?
                    if cell  != orig_val:
                        made_progress = True
                    if made_progress:
                        self.change.emit()
                        time.sleep(0.001)
                    if not self.cells[row * 4 + col]:
                        print("No solution")
                        return Result.NO_SOLUTION

        if made_progress:
            result = self.solve()
        else:
            if self.is_solved():
                print("Solved")
                return Result.SOLVED
            else:
                print("No more progress")
                return result.NO_PROGRESS
        return result

    def locate_least_options(self):
        min_options = 5
        min_row = 0
        min_col = 0
        for row in range(4):
            for col in range(4):
                cell = self.cells[row * 4 + col]
                if type(cell) == set:
                    if min_options > len(cell) > 1:
                        min_options = len(cell)
                        min_row = row
                        min_col = col
        if min_options == 5:
            return None, None
        return min_row, min_col

    def is_solved(self):
        for row in self.rows:
            for cell in row:
                if type(cell) != int:
                    return False
        return True

    def back_tracking_solver(self):
        result = Result.NO_PROGRESS
        unknowns = []
        while not self.stop and result != Result.SOLVED:
            unexplored = copy.deepcopy(self.cells)
            row, col = self.locate_least_options()
            guess = unexplored[row * 9 + col].pop()
            unknowns.append(unexplored)
            self.cells[row * 4 + col] = guess
            self.change.emit()
            for row in range(4):
                for col in range(4):
                    cell = self.cells[row * 4 + col]
                    if type(cell) == set:
                        self.naked_single(row, col)
                        # self.naked_pairs(row, col)
                        # self.hidden_single(row, col)
            if self.is_solved():
                result = Result.SOLVED
                break
        return result

    def validate(self):
        for cell in self.cells:
            if type(cell) != int:
                return False

        nums = list(range(1, 5))
        for row in self.rows:
            ro = list(row)
            if len(ro) != 4:
                return False
            if sorted(ro) != nums:
                return False
        for col in self.columns:
            co = list(col)
            if len(co) != 4:
                return False
            if sorted(co) != nums:
                return False
        return True
