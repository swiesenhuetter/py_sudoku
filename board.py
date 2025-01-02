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
            self.cells = [0] * 81

    @classmethod
    def from_string(cls, string):
        cells = []
        for c in string:
            if c not in "123456789":
                cells.append(set(range(1, 10)))
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
        return [self.cells[i:i+9] for i in range(0, 81, 9)]

    @property
    def columns(self):
        return [self.cells[i::9] for i in range(9)]

    @property
    def boxes(self):
        return [self.cells[i:i+3] + self.cells[i+9:i+12] + self.cells[i+18:i+21] for i in (0, 3, 6, 27, 30, 33, 54, 57, 60)]

    def box(self, row, col):
        return self.boxes[(row // 3) * 3 + col // 3]

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
        self.worker = threading.Thread(target=self.back_tracking_solver,
                                       name="Sudoku Solver")
        self.worker.start()

    def solve(self) -> Result:
        result = Result.NO_SOLUTION
        made_progress = False
        for row in range(9):
            for col in range(9):
                cell = self.cells[row*9+col]
                if type(cell) == set:
                    orig_val = cell.copy()
                    cell -= {num for num in self.rows[row] if type(num) == int}
                    cell -= {num for num in self.columns[col] if type(num) == int}
                    cell -= {num for num in self.box(row, col) if type(num) == int}
                    if len(cell) == 1:
                        self.cells[row*9+col] = cell.pop()
                        if orig_val != cell:
                            made_progress = True
                    elif len(cell) < len(orig_val):
                        made_progress = True
                    if made_progress:
                        self.change.emit()
                        time.sleep(0.001)
                    if not self.cells[row*9+col]:
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
                return Result.NO_PROGRESS
        return result

    def locate_least_options(self):
        min_options = 10
        min_row = 0
        min_col = 0
        for row in range(9):
            for col in range(9):
                cell = self.cells[row*9+col]
                if type(cell) == set:
                    if len(cell) < min_options and len(cell) > 1:
                        min_options = len(cell)
                        min_row = row
                        min_col = col
        if min_options == 10:
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
        unexplored = [copy.deepcopy(self.cells)]
        while not self.stop and result != Result.SOLVED:
            if not unexplored:
                break
            self.cells = unexplored.pop()
            self.change.emit()
            result = self.solve()
            if result == Result.NO_PROGRESS:
                row, col = self.locate_least_options()
                cell = self.cells[row * 9 + col]
                # remove first option
                val = cell.pop()
                cells_copied = copy.deepcopy(self.cells)
                unexplored.append(cells_copied)
                self.cells[row * 9 + col] = val
                unexplored.append(copy.deepcopy(self.cells))
                self.change.emit()
                # restore previous state
            elif result == Result.SOLVED:
                break
        return result

    def validate(self):
        for cell in self.cells:
            if type(cell) != int:
                return False

        nums = list(range(1, 10))
        for row in self.rows:
            ro = list(row)
            if len(ro) != 9:
                return False
            if sorted(ro) != nums:
                return False
        for col in self.columns:
            co = list(col)
            if len(co) != 9:
                return False
            if sorted(co) != nums:
                return False
        for box in self.boxes:
            qu = list(box)
            if len(qu) != 9:
                return False
            if sorted(qu) != nums:
                return False
        return True
