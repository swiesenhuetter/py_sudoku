from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QFileDialog
)
from PySide6.QtGui import QIntValidator, QColor
from PySide6.QtCore import Qt
from board import Board


class SudokuWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.grid_layout = QGridLayout()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.board = Board()
        self.board.change.connect(self.update_ui)
        self.init_ui()

    def init_ui(self):
        # Create Sudoku Grid
        for row in range(9):
            for col in range(9):
                cell = QLineEdit()
                cell.setFixedSize(40, 40)
                cell.setAlignment(Qt.AlignCenter)
                cell.setValidator(QIntValidator(1, 9))  # Only numbers 1–9
                self.style_cell(cell, row, col)
                self.grid_layout.addWidget(cell, row, col)
                self.cells[row][col] = cell

        # Add grid to main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)

        # Add action buttons
        button_layout = QVBoxLayout()
        solve_button = QPushButton("Solve")
        clear_button = QPushButton("Clear")
        validate_button = QPushButton("Validate")
        load_button = QPushButton("Load from File")

        button_layout.addWidget(solve_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(validate_button)
        button_layout.addWidget(load_button)

        solve_button.clicked.connect(self.solve)
        clear_button.clicked.connect(self.clear_grid)
        validate_button.clicked.connect(self.validate_grid)
        load_button.clicked.connect(self.load_from_file)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def style_cell(self, cell, row, col):
        # Base border styles
        base_style = "border: 1px solid #aaa;"

        # Add thicker borders for 3x3 subgrid separators
        if row % 3 == 0:  # Top border
            base_style += "border-top: 2px solid black;"
        if col % 3 == 0:  # Left border
            base_style += "border-left: 2px solid black;"
        if row % 3 == 2:  # Bottom border for last row
            base_style += "border-bottom: 2px solid black;"
        if col % 3 == 2:  # Right border for last column
            base_style += "border-right: 2px solid black;"
        cell.setStyleSheet(base_style)

    def solve(self):
        print("Solve button pressed")
        try:
            self.board.solve_background()
        except ValueError:
            print("No solution")
        self.update_ui()

    def clear_grid(self):
        """Clear all cells."""
        for row in range(9):
            for col in range(9):
                self.cells[row][col].clear()

    def validate_grid(self):
        # Placeholder for validation logic
        print("Validate button pressed")

    def load_from_file(self):
        # txt files only
        file_select_dlg = QFileDialog()
        file_select_dlg.setNameFilter("Text files (*.txt)")
        file_select_dlg.exec()
        file_path = file_select_dlg.selectedFiles()[0]
        print(f"Loading from {file_path}")
        self.board = Board.from_file(file_path)
        self.board.change.connect(self.update_ui)
        self.board.change.emit()

    def update_ui(self):
        """Update the UI based on the model data."""
        for row in range(9):
            for col in range(9):
                value = self.board.cells[row*9+col]
                if type(value) == set:
                    grey_level = 255 - len(value) * 20
                    bg_col = QColor(grey_level, grey_level, grey_level)

                    self.cells[row][col].setText("")
                    self.cells[row][col].setStyleSheet(f"background-color: {bg_col.name()};")
                    self.cells[row][col].setToolTip(", ".join(str(num) for num in value))
                else:
                    self.cells[row][col].setText(str(value) if value != 0 else "")
                    self.cells[row][col].setStyleSheet("background-color: lightgreen;")
                    self.cells[row][col].setToolTip("solved")


if __name__ == "__main__":
    app = QApplication([])

    widget = SudokuWidget()
    widget.show()
    app.exec()