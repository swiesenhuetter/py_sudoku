from board import Board, Result
from pytest import fixture

def test_shape_4():
    board = Board(list(range(1, 17)))
    assert len(board.rows) == 4
    assert len(board.rows[0]) == 4
    assert len(board.columns) == 4


@fixture
def one_two_board():
    s1 = "12  " \
         "21  " \
         "    " \
         "    "
    return Board.from_string(s1)


def test_from_string():
    board = Board.from_string("1234" * 4)
    assert board.rows[0] == list(range(1, 5))
    assert board.rows[0] == board.rows[1] == board.rows[2] == board.rows[3]


def test_from_four_line(one_two_board):
    assert len(one_two_board.rows[0]) == 4
    assert len(one_two_board.columns[0]) == 4

    assert one_two_board.rows[0][0] == 1
    assert one_two_board.rows[0][1] == 2
    assert one_two_board.rows[1][1] == 1
    assert one_two_board.rows[0][3] == set(range(1, 5))

    one_two_board.solve()
    print(f"\n{one_two_board}")

def test_solve_one_two(one_two_board):
    result = one_two_board.solve()
    assert result == Result.NO_PROGRESS
    print(f"\n{one_two_board}")

def test_naked_singles(one_two_board):
    one_two_board.set_cell(0, 3, 4)
    result = one_two_board.naked_single(0, 2)
    assert result == True
    assert one_two_board.get_cell(0, 3) == 4
    assert one_two_board.get_cell(0, 2) == 3

    resul12 = one_two_board.naked_single(1, 2)
    assert resul12 == True
    assert one_two_board.get_cell(1, 2) == 4


def test_hidden_singles():
    empty_board = Board.from_string(" " * 81)
    result = empty_board.hidden_single(0, 0)
    assert result == False
    # remove all 7s from row 0
    for col in range(1,9):
        empty_board.cells[col] -= {7}
    assert empty_board.hidden_single(0, 0)
    assert empty_board.cells[0] == 7

def test_naked_pairs():
    empty_board = Board.from_string(" " * 16)
    result = empty_board.naked_pairs(0, 0)
    assert result == False

    empty_board.cells[0] = {3, 4}
    empty_board.cells[1] = {3, 4}
    res2 = empty_board.naked_pairs(0, 2)
    assert res2 == True
    res3 = empty_board.naked_pairs(0, 3)
    assert res3 == True
    assert empty_board.get_cell(0, 2) == {1, 2}
    assert empty_board.get_cell(0, 3) == {1, 2}