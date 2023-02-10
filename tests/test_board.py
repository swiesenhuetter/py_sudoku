from board import Board
from pytest import fixture

def test_shape():
    board = Board(list(range(1, 82)))
    assert len(board.rows) == 9
    assert len(board.rows[0]) == 9
    assert len(board.columns) == 9
    assert len(board.boxes) == 9

def test_boxes():
    board = Board(list(range(1, 82)))
    assert board.box(0, 0) == board.boxes[0]
    assert board.box(2, 2) == board.box(0, 0)

@fixture
def difficult_board():
    s1 = "    5 3  " \
         "96  8    " \
         "     7 9 " \
         "7  1 2   " \
         "  2      " \
         "  13   5 " \
         "      231" \
         " 4      7" \
         " 78     5"
    return Board.from_string(s1)


def test_from_string():
    board = Board.from_string("123456789" * 9)
    assert board.rows[0] == list(range(1, 10))
    assert board.rows[0] == board.rows[8]


def test_solve(difficult_board):
    assert len(difficult_board.rows[0]) == 9
    assert difficult_board.rows[0][4] == 5
    assert difficult_board.rows[0][6] == 3
    assert difficult_board.rows[0][0] == set(range(1, 10))

    difficult_board.solve()


