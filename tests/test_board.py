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
    print(f"\n{difficult_board}")

def test_locate_least_options(difficult_board):
    row, col = difficult_board.locate_least_options()
    assert len(difficult_board.rows[row][col]) == 9
    difficult_board.solve()
    row, col = difficult_board.locate_least_options()
    assert len(difficult_board.rows[row][col]) == 2

def test_is_solved(simple_board):
    assert not simple_board.is_solved()
    simple_board.solve()
    assert simple_board.is_solved()

@fixture
def simple_board():
    s1 = "53-" "-7-" "---"\
         "6--" "195" "---"\
         "-98" "---" "-6-"\
         "8--" "-6-" "--3"\
         "4--" "8-3" "--1"\
         "7--" "-2-" "--6"\
         "-6-" "---" "28-"\
         "---" "419" "--5"\
         "---" "-8-" "-79"
    return Board.from_string(s1)

def test_solve_simple(simple_board):
    assert len(simple_board.rows[0]) == 9
    assert simple_board.rows[0][0] == 5
    assert simple_board.rows[0][4] == 7
    assert simple_board.rows[8][6] == set(range(1, 10))

    simple_board.solve()
    print(f"\n{simple_board}")


@fixture
def arto_inkala_board():
    s1 = "8--" "---" "---"\
         "--3" "6--" "---"\
         "-7-" "-9-" "2--"\
         "-5-" "--7" "---"\
         "---" "-45" "7--"\
         "---" "1--" "-3-"\
         "--1" "---" "-68"\
         "--8" "5--" "-1-"\
         "-9-" "---" "4--"
    return Board.from_string(s1)

def test_solve_simple(arto_inkala_board):
    arto_inkala_board.solve()
    print(f"\n{arto_inkala_board}")

    Board.back_tracking_solver(arto_inkala_board)
    print(f"\n{arto_inkala_board}")
