#!/usr/bin/env python3

from copy import deepcopy

import pytest

from wfc.wfc import Board, InvalidRow, InvalidColumn, nums

n = None

sudoku = [
    [2, 9, 6, n, 7, 8, 4, 3, n],
    [5, n, n, 9, 4, 3, 2, 7, n],
    [n, 4, 3, n, n, n, n, n, n],
    [n, n, n, n, n, n, 7, n, n],
    [n, 7, n, 8, n, 5, 6, n, n],
    [n, n, 9, 4, 6, n, n, n, 8],
    [9, 1, 7, n, n, 6, 5, 2, n],
    [6, n, n, 7, n, n, n, 9, 3],
    [n, n, 2, n, 1, n, 8, 6, 7],
]

sudoku_with_a_row = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [5, n, n, 9, 4, 3, 2, 7, n],
    [n, 4, 3, n, n, n, n, n, n],
    [n, n, n, n, n, n, 7, n, n],
    [n, 7, n, 8, n, 5, 6, n, n],
    [n, n, 9, 4, 6, n, n, n, 8],
    [9, 1, 7, n, n, 6, 5, 2, n],
    [6, n, n, 7, n, n, n, 9, 3],
    [n, n, 2, n, 1, n, 8, 6, 7],
]

sudoku_with_more_populated_board = [
    [n, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, n, 3, 4, n, 6, 7, n, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
]


@pytest.fixture
def board():
    return deepcopy(Board(sudoku.copy()))


@pytest.fixture
def row_complete():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


@pytest.fixture
def row_incomplete():
    return [n, 2, 3, 4, 5, 6, 7, 8, 9]


def test_board_draw(board):
    board.draw()
    assert True


def test_row_check_row():
    Board(sudoku_with_a_row.copy()).check_row(0)


def test_board_set_get(board):
    board[(0, 0)] = 9
    assert board[(0, 0)] == 9


def test_row_check_row_duplicates_error(board):
    board[(0, 3)] = 2
    with pytest.raises(InvalidRow):
        board.check_row(0)


def test_board_check_column(board):
    with pytest.raises(InvalidColumn):
        board.check_column(0)


def test_board_valid_in_row(board):
    assert board.valid_in_row(0) == nums - set(board.get_row(0))


def test_board_get_column(board):
    assert board.get_column(0) == [2, 5, n, n, n, n, 9, 6, n]


def test_board_valid_in_col(board):
    assert board.valid_in_column(0) == nums - set(board.get_column(0))


def test_board_quadrent(board):
    res = board.get_quadrent(5)
    assert res == [
        [n, n, n],
        [8, n, 5],
        [4, 6, n],
    ]


def test_board_vals_in_quadrent(board):
    assert board.vals_in_quadrent(5) == {8, 5, 4, 6}


def test_board_valid_in_quadrent(board):
    assert board.valid_in_quadrent(5) == {1, 2, 3, 7, 9}


def test_board_which_quadrent(board):
    assert board.which_quadrent(4, 4) == 5


def test_board_cell_valid_options(board):
    assert board.cell_valid_options(4, 4) == {2, 3, 9}


def test_board_empty_cells(board):
    board = Board(sudoku_with_more_populated_board.copy())
    assert board.empty_cells() == [
        (0, 0),
        (4, 1),
        (4, 4),
        (4, 7),
    ]
