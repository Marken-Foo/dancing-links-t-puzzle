from __future__ import annotations

import unittest
from itertools import product

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from collections.abc import Iterable


class Square:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Square) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def translate(self, dx: int, dy: int) -> Square:
        return Square(self.x + dx, self.y + dy)

    def rotate_anticlockwise(self) -> Square:
        return Square(x=-self.y, y=self.x)

    def reflect_about_x_axis(self) -> Square:
        return Square(-self.x, self.y)

    def reflect_about_y_axis(self) -> Square:
        return Square(self.x, -self.y)


class Polyomino:
    MAX_XY = 9999

    def __init__(self, squares: Iterable[Square]) -> None:
        self.squares: set[Square] = set(squares)

    def __str__(self) -> str:
        return f"Polyomino({','.join((str(sq) for sq in self.squares))})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Polyomino) and self.squares == other.squares

    def __hash__(self) -> int:
        return hash(tuple(self.squares))

    def translate_to_origin(self) -> Polyomino:
        x_min = Polyomino.MAX_XY
        y_min = Polyomino.MAX_XY
        for sq in self.squares:
            if sq.x < x_min:
                x_min = sq.x
            if sq.y < y_min:
                y_min = sq.y
        return self.translate(-x_min, -y_min)

    def get_bounds(self) -> tuple[int, int, int, int]:
        x_min = Polyomino.MAX_XY
        y_min = Polyomino.MAX_XY
        x_max = -Polyomino.MAX_XY
        y_max = -Polyomino.MAX_XY
        for sq in self.squares:
            if sq.x < x_min:
                x_min = sq.x
            if sq.x > x_max:
                x_max = sq.x
            if sq.y < y_min:
                y_min = sq.y
            if sq.y > y_max:
                y_max = sq.y
        return (x_min, x_max, y_min, y_max)

    def translate(self, dx: int, dy: int) -> Polyomino:
        return Polyomino((sq.translate(dx, dy) for sq in self.squares))

    def rotate_anticlockwise(self) -> Polyomino:
        return Polyomino((sq.rotate_anticlockwise() for sq in self.squares))

    def reflect_about_x_axis(self) -> Polyomino:
        return Polyomino((sq.reflect_about_x_axis() for sq in self.squares))

    def reflect_about_y_axis(self) -> Polyomino:
        return Polyomino((sq.reflect_about_y_axis() for sq in self.squares))

    def contains(self, polyomino: Polyomino) -> bool:
        return all((sq in self.squares for sq in polyomino.squares))


# Assumes board and polyomino have already been translated to origin.
def generate_positions(
    origin_board: Polyomino, origin_polyomino: Polyomino
) -> set[Polyomino]:
    (_, board_x_max, _, board_y_max) = origin_board.get_bounds()
    (_, x_max, _, y_max) = origin_polyomino.get_bounds()
    displacements = product(
        range(1 + board_x_max - x_max), range(1 + board_y_max - y_max)
    )
    return set(
        filter(
            lambda p: origin_board.contains(p),
            (origin_polyomino.translate(x, y) for (x, y) in displacements),
        )
    )


class PolyominoTests(unittest.TestCase):
    def test_translate_square(self) -> None:
        sut = Square(1, 2)
        actual = sut.translate(2, -7)
        expected = Square(3, -5)
        self.assertEqual(actual, expected)

    def test_translate_polyomino(self) -> None:
        coords = [(0, 0), (1, 0), (1, 1), (2, 1)]
        sut = Polyomino([Square(x, y) for (x, y) in coords])
        actual = sut.translate(-1, 2)
        expected = Polyomino([Square(-1, 2), Square(0, 2), Square(0, 3), Square(1, 3)])
        self.assertEqual(actual, expected)

    def test_rotate_square(self) -> None:
        sut = Square(-3, -5)
        actual = sut.rotate_anticlockwise()
        expected = Square(5, -3)
        self.assertEqual(actual, expected)

    def test_rotate_polyomino(self) -> None:
        coords = [(0, 0), (1, 0), (1, 1), (2, 1)]
        sut = Polyomino([Square(x, y) for (x, y) in coords])
        actual = sut.rotate_anticlockwise()
        expected = Polyomino([Square(0, 0), Square(0, 1), Square(-1, 1), Square(-1, 2)])
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
