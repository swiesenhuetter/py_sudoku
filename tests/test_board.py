from board import Board

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
