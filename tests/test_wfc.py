#!/usr/bin/env python3

from copy import deepcopy

import pytest

from wfc.wfc import (
    Board,
    InvalidRow,
    InvalidColumn,
    nums,
    InvalidBoard,
    solve,
    least_empties,
)

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
    [1, 2, 3, 4, 5, 6, 1, 2, 3],
    [1, 2, 3, 4, 5, 6, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
]

sudoku_solved = [
    [9, 8, 5, 7, 2, 4, 1, 6, 3],
    [1, 4, 6, 8, 9, 3, 2, 7, 5],
    [3, 7, 2, 1, 5, 6, 4, 9, 8],
    [6, 9, 8, 4, 7, 5, 3, 1, 2],
    [7, 1, 4, 9, 3, 2, 5, 8, 6],
    [5, 2, 3, 6, 1, 8, 7, 4, 9],
    [8, 5, 9, 3, 4, 1, 6, 2, 7],
    [2, 6, 1, 5, 8, 7, 9, 3, 4],
    [4, 3, 7, 2, 6, 9, 8, 5, 1],
]

sudoku_almost_solved = [
    [n, n, n, 7, 2, 4, 1, 6, 3],
    [n, n, n, 8, 9, 3, 2, 7, 5],
    [n, n, n, 1, 5, 6, 4, 9, 8],
    [6, 9, 8, 4, 7, 5, 3, 1, 2],
    [7, 1, 4, 9, 3, 2, 5, 8, 6],
    [5, 2, 3, 6, 1, 8, 7, 4, 9],
    [8, 5, 9, 3, 4, 1, 6, 2, 7],
    [2, 6, 1, 5, 8, 7, 9, 3, 4],
    [4, 3, 7, 2, 6, 9, 8, 5, 1],
]

sudoku_almost_solved_2_quads = [
    [n, n, n, 7, 2, 4, n, n, n],
    [n, n, n, n, n, n, n, n, n],
    [n, n, n, 1, 5, 6, n, n, n],
    [6, 9, 8, 4, 7, 5, 3, 1, 2],
    [7, 1, 4, 9, n, 2, 5, 8, 6],
    [5, 2, 3, 6, 1, 8, 7, 4, 9],
    [8, 5, 9, n, n, n, 6, 2, 7],
    [2, 6, 1, 5, 8, 7, 9, 3, 4],
    [4, 3, 7, 2, 6, 9, 8, 5, 1],
]


@pytest.fixture
def board():
    return deepcopy(Board(sudoku.copy()))


@pytest.fixture
def board_solved():
    return deepcopy(Board(sudoku_solved.copy()))


@pytest.fixture
def board_almost_solved():
    return deepcopy(Board(sudoku_almost_solved.copy()))


@pytest.fixture
def board_almost_solved_2_quads():
    return deepcopy(Board(sudoku_almost_solved_2_quads.copy()))


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


def test_board_quadrent_last(board):
    res = board.get_quadrent(9)
    assert res == [
        [5, 2, n],
        [n, 9, 3],
        [8, 6, 7],
    ]


def test_board_quadrent_topright(board):
    res = board.get_quadrent(3)
    assert res == [
        [4, 3, n],
        [2, 7, n],
        [n, n, n],
    ]


def test_board_vals_in_quadrent(board):
    assert board.vals_in_quadrent(5) == {8, 5, 4, 6}


def test_board_vals_in_quadrent_empty(board_almost_solved_2_quads):
    print(board_almost_solved_2_quads[0, 8])
    assert board_almost_solved_2_quads.vals_in_quadrent(3) == set()


def test_board_valid_in_quadrent(board):
    assert board.valid_in_quadrent(5) == {1, 2, 3, 7, 9}


def test_board_valid_in_quadrent_empty(board_almost_solved_2_quads):
    assert board_almost_solved_2_quads.valid_in_quadrent(3) == nums


def test_board_which_quadrent(board):
    assert board.which_quadrent(4, 4) == 5


def test_board_valid_in_cell(board):
    assert board.valid_in_cell(4, 4) == {2, 3, 9}


def test_board_valid_in_cell_2_quads(board_almost_solved_2_quads):
    assert board_almost_solved_2_quads.valid_in_cell(0, 6) == {1}
    assert board_almost_solved_2_quads.valid_in_cell(0, 7) == {9, 6}


def test_board_empty_cells(board):
    board = Board(sudoku_with_more_populated_board.copy())
    assert board.empty_cells() == [
        (0, 0),
        (4, 1),
        (4, 4),
        (4, 7),
    ]


def test_board_empty_cells_goes_higher_than_nine(board_almost_solved_2_quads):
    res = board_almost_solved_2_quads.empty_cells()
    print(res)
    assert len(res) == 25


def test_board_check_quadrent(board):
    board = Board(sudoku_with_more_populated_board.copy())
    board.check_quadrent(9)


def test_check_board(board_solved):
    board_solved.check_board()


def test_check_board_wrong(board_solved):
    board_solved[(0, 0)] = 1
    with pytest.raises(InvalidBoard):
        board_solved.check_board()


def test_least_empties(board_almost_solved_2_quads):
    res = least_empties(
        board_almost_solved_2_quads.empty_cells(), board_almost_solved_2_quads
    )
    assert res[0] == ((0, 1), {8})
    assert res[1] == ((0, 6), {1})
    assert len(res) == 25
    assert len(res[24][1]) == 3


def test_solve(board):
    finished, _ = solve(board)
    assert finished.check_board()[0]


def test_solve_solved_board(board_solved):
    finished, _ = solve(board_solved)
    assert finished.check_board()[0]


def test_solve_almost_solved_board(board_almost_solved):
    board, _ = solve(board_almost_solved)
    assert board.check_board()[0]


def test_solve_easy_board(board):
    board, _ = solve(board)
    assert board.check_board()[0]
