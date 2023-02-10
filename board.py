
class Board:
    def __init__(self, cells=None):
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

    def solve(self):
        found_something = False
        for row in range(9):
            for col in range(9):
                cell = self.cells[row*9+col]
                if type(cell) == set:
                    cell -= {num for num in self.rows[row] if type(num) == int}
                    cell -= {num for num in self.columns[col] if type(num) == int}
                    cell -= {num for num in self.box(row, col) if type(num) == int}
                    if len(cell) == 1:
                        self.cells[row*9+col] = cell.pop()
                        found_something = True
        if found_something:
            self.solve()
        else:
            print(self)
