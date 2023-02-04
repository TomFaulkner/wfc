#!/usr/bin/env python3

import random
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
from typing import Sequence


class InvalidColumn(ValueError):
    pass


class InvalidRow(ValueError):
    pass


class InvalidQuadrent(ValueError):
    pass


class InvalidBoard(ValueError):
    pass


nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}


@dataclass
class Board:
    rows: list[list[int | None]]
    _current: int = 0
    _stop: int = 9

    def __iter__(self):
        return self

    def __next__(self):
        cur = self._current
        if self._current >= self._stop:
            raise StopIteration()

        self._current += 1
        return self.rows[cur]

    def __getitem__(self, __name: tuple[int, int] | int) -> int | None:
        try:
            x, y = int(__name[0]), int(__name[1])
            assert 0 <= x <= 8, f"{x} is out of range"
            assert 0 <= y <= 8, f"{y} is out of range"
            return self.rows[x][y]
        except TypeError:
            return self.get_quadrent(__name)

    def __setitem__(self, __name: tuple[int, int] | int, __value: int) -> None:
        x, y = int(__name[0]), int(__name[1])
        self.rows[x][y] = __value

    def draw(self) -> None:
        def sub_none(value: int | None):
            if value is None:
                return " - "
            return f" {str(value)} "

        print("-" * 35)
        for row in self.rows:
            print("|".join([sub_none(cell) for cell in row]))
            print("-" * 35)

    def get_column(self, col: int) -> list[int | None]:
        return [row[col] for row in self.rows]

    def get_row(self, row: int) -> list[int, None]:
        return self.rows[row]

    def check_column(self, col: int) -> None:
        if {1, 2, 3, 4, 5, 6, 7, 8, 9} != set(self.get_column(col)):
            raise InvalidColumn()

    def check_row(self, row: int):
        if {1, 2, 3, 4, 5, 6, 7, 8, 9} != set(self.rows[row]):
            raise InvalidRow()

    def check_quadrent(self, q: int):
        if {1, 2, 3, 4, 5, 6, 7, 8, 9} != self.vals_in_quadrent(q):
            raise InvalidQuadrent()

    def check_board(self, raise_on_invalid: bool = True) -> tuple[bool, list[str]]:
        errors = []
        for row in range(9):
            try:
                self.check_row(row)
            except InvalidRow as e:
                errors.append(str(e))
        for col in range(9):
            try:
                self.check_column(col)
            except InvalidColumn as e:
                errors.append(str(e))
        for quad in range(1, 10):
            try:
                self.check_quadrent(quad)
            except InvalidQuadrent as e:
                errors.append(str(e))
        if errors:
            if raise_on_invalid:
                raise InvalidBoard(str(errors))
            return False, errors
        return True, []

    def valid_in_cell(self, x, y) -> set[int]:
        c = self.valid_in_column(y)
        r = self.valid_in_row(x)
        quad = self.which_quadrent(x, y)
        q = self.valid_in_quadrent(self.which_quadrent(x, y))
        return c.intersection(r.intersection(q))

    def valid_in_column(self, y: int) -> set[int]:
        return nums - set(self._rm_none(self.get_column(y)))

    def valid_in_row(self, x: int) -> set[int]:
        row_values = set(self._rm_none(self.rows[x]))
        return set(nums - row_values)

    def which_quadrent(self, x: int, y: int) -> int:
        def section(val: int):
            match val:
                case (0 | 1 | 2):
                    return 1
                case (3 | 4 | 5):
                    return 2
                case (6 | 7 | 8):
                    return 3

        super_col = section(x)
        super_row = section(y)
        match super_col, super_row:
            case [1, 1]:
                return 1
            case [1, 2]:
                return 2
            case [1, 3]:
                return 3
            case [2, 1]:
                return 4
            case [2, 2]:
                return 5
            case [2, 3]:
                return 6
            case [3, 1]:
                return 7
            case [3, 2]:
                return 8
            case [3, 3]:
                return 9
        raise ValueError(f"Not a valid x, y? {x}, {y}")

    def get_quadrent(self, q: int) -> list[list[int]]:
        x_top = {"xs": 0, "xe": 2}
        x_mid = {"xs": 3, "xe": 5}
        x_bottom = {"xs": 6, "xe": 8}
        y_left = {"ys": 0, "ye": 2}
        y_mid = {"ys": 3, "ye": 5}
        y_right = {"ys": 6, "ye": 8}

        quads = {
            1: x_top | y_left,
            2: x_top | y_mid,
            3: x_top | y_right,
            4: x_mid | y_left,
            5: x_mid | y_mid,
            6: x_mid | y_right,
            7: x_bottom | y_left,
            8: x_bottom | y_mid,
            9: x_bottom | y_right,
        }
        quad = quads[q]
        lines = []

        for x in range(quads[q]["xs"], quads[q]["xe"] + 1):
            lines.append(
                [
                    self[x, quad["ys"]],
                    self[x, quad["ys"] + 1],
                    self[x, quad["ys"] + 2],
                ]
            )
        return lines

    def vals_in_quadrent(self, q: int) -> set[int]:
        return set(self._rm_none(chain.from_iterable(self.get_quadrent(q))))

    def valid_in_quadrent(self, q: int) -> set[int]:
        return nums - self.vals_in_quadrent(q)

    def empty_cells(self) -> list[tuple[int, int]]:
        empties = []
        for x, row in enumerate(self.rows):
            for y, cell in enumerate(row):
                if cell is None:
                    empties.append((x, y))

        return empties

    @staticmethod
    def _rm_none(items: Sequence[int]) -> list[int]:
        return [x for x in items if x is not None]


class SolverImpossible(Exception):
    pass


def least_empties(empties, board):
    empty_cell_choices = []
    for e in empties:
        empty_cell_choices.append((e, board.valid_in_cell(e[0], e[1])))
    return sorted(empty_cell_choices, key=lambda x: len(x[1]))


def solve(board: Board) -> tuple[Board, int]:
    working = deepcopy(board)
    iteration = 0
    while not working.check_board(False)[0]:
        try:
            print("w1")
            while working.empty_cells():
                iteration += 1
                print("iter: ", iteration)
                empties = working.empty_cells()
                next_cell = least_empties(empties, working)[0][0]

                print("w2", next_cell, empties)
                print(next_cell, working.valid_in_cell(next_cell[0], next_cell[1]))
                valid_options = list(working.valid_in_cell(next_cell[0], next_cell[1]))
                if not valid_options:
                    raise SolverImpossible("A next_cell has no valid options.")
                working[next_cell] = random.choice(valid_options)
                # random.choice(working.valid_in_next_cell(next_cell[0], next_cell[1]))
                # working[next_cell] = random.choice(working.valid_in_next_cell(next_cell[0], next_cell[1]))
            break
        except SolverImpossible:
            working = deepcopy(board)

    return working, iteration

    # iterate over empty cells
    # populate one with a valid number
    # repeat


if __name__ == "__main__":
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
    print(solve(Board(sudoku)))
