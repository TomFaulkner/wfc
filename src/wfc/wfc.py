#!/usr/bin/env python3

from dataclasses import dataclass
from itertools import chain
from typing import Sequence


class InvalidColumn(ValueError):
    pass


class InvalidRow(ValueError):
    pass


@dataclass
class Row:
    row: list[int | None]
    _current: int = 0
    _stop: int = 9

    def __post_init__(self):
        assert len(self.row) == 9

    def __iter__(self):
        return self

    def __next__(self):
        cur = self._current
        if self._current >= self._stop:
            raise StopIteration()
        self._current += 1
        return self.row[cur]

    def check_row(self):
        if {1, 2, 3, 4, 5, 6, 7, 8, 9} != set(self.row):
            raise InvalidRow()

    def __getitem__(self, __name: str) -> int | None:
        col = int(__name)
        return self.row[col]

    def __setitem__(self, __name: str, __value: int) -> None:
        col = int(__name)
        self.row[col] = __value


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
            return self.rows[x][y]
        except TypeError:
            return quadrent(__name)

    def __setitem__(self, __name: str, __value: int) -> None:
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

    def cell_valid_options(self, x, y) -> list[int]:
        self.valid_in_column(y)
        self.valid_in_row(x)
        self.valid_in_quadrent(quadrent)

    def valid_in_column(self, y: int) -> set[int]:
        return nums - set(self._rm_none(self.get_column(y)))

    def valid_in_row(self, x: int) -> set[int]:
        row_values = set(self._rm_none(self.rows[x]))
        return set(nums - row_values)

    def get_quadrent(self, q: int) -> list[list[int]]:
        x_top = {"ys": 0, "ye": 2}
        x_mid = {"ys": 3, "ye": 5}
        x_bottom = {"ys": 6, "ye": 8}
        y_left = {"xs": 0, "xe": 2}
        y_mid = {"xs": 3, "xe": 5}
        y_right = {"xs": 6, "xe": 9}

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

    def solve(self):
        pass

    @staticmethod
    def _rm_none(items: Sequence[int]) -> list[int]:
        return [x for x in items if x is not None]
