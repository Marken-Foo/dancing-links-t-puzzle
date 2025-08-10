from itertools import product

from typing import TypeVar

import dancing_links_root as dlinks
import polyomino as polym
import polycube as polyc


T = TypeVar("T")


def t_puzzle() -> None:
    box = polyc.Polycube(
        (polyc.Cube(x, y, z) for (x, y, z) in product(range(6), range(6), range(6)))
    ).translate_to_origin()
    t_tetromino = polyc.Polycube(
        (polyc.Cube(x, y, 0) for (x, y) in ((0, 0), (1, 0), (2, 0), (1, 1)))
    ).translate_to_origin()

    transformations = [
        t_tetromino,
        t_tetromino.apply_rotations("X"),
        t_tetromino.apply_rotations("XX"),
        t_tetromino.apply_rotations("XXX"),
        t_tetromino.apply_rotations("Z"),
        t_tetromino.apply_rotations("ZY"),
        t_tetromino.apply_rotations("ZYY"),
        t_tetromino.apply_rotations("ZYYY"),
        t_tetromino.apply_rotations("Y"),
        t_tetromino.apply_rotations("YZ"),
        t_tetromino.apply_rotations("YZZ"),
        t_tetromino.apply_rotations("YZZZ"),
    ]

    all_positions: set[polyc.Polycube] = set()
    for transformation in transformations:
        all_positions.update(
            polyc.generate_positions(box, transformation.translate_to_origin())
        )

    dancing_links = dlinks.Root()
    for cube in box.cubes:
        dancing_links.add_constraint((cube.x, cube.y, cube.z))
    for piece in all_positions:
        dancing_links.add_item(
            piece, [(cube.x, cube.y, cube.z) for cube in piece.cubes]
        )
    solutions = dancing_links.solve()
    print_solutions(solutions)


def tile_4x2x2_box_with_o_tetrominos() -> None:
    box = polyc.Polycube(
        (polyc.Cube(x, y, z) for (x, y, z) in product(range(4), range(2), range(2)))
    ).translate_to_origin()
    o_tetromino = polyc.Polycube(
        (polyc.Cube(x, y, 0) for (x, y) in ((0, 0), (0, 1), (1, 0), (1, 1)))
    ).translate_to_origin()

    transformations = [
        o_tetromino,
        o_tetromino.apply_rotations("X"),
        o_tetromino.apply_rotations("Y"),
    ]

    all_positions: set[polyc.Polycube] = set()
    for transformation in transformations:
        all_positions.update(
            polyc.generate_positions(box, transformation.translate_to_origin())
        )

    dancing_links = dlinks.Root()
    for cube in box.cubes:
        dancing_links.add_constraint((cube.x, cube.y, cube.z))
    for piece in all_positions:
        dancing_links.add_item(
            piece, [(cube.x, cube.y, cube.z) for cube in piece.cubes]
        )

    solutions: list[list[polyc.Polycube]] = dancing_links.solve()
    print_solutions(solutions)


def tile_4x4_square_with_l_tetrominos() -> None:
    board = polym.Polyomino(
        (polym.Square(x, y) for (x, y) in product(range(4), range(4)))
    ).translate_to_origin()
    l_tetromino = polym.Polyomino(
        (polym.Square(x, y) for (x, y) in ((0, 0), (1, 0), (2, 0), (0, 1)))
    ).translate_to_origin()

    all_positions: set[polym.Polyomino] = set()
    mino = l_tetromino
    for _ in range(4):
        reflected_mino = mino.reflect_about_x_axis().translate_to_origin()
        all_positions.update(polym.generate_positions(board, mino))
        all_positions.update(polym.generate_positions(board, reflected_mino))
        mino = mino.rotate_anticlockwise().translate_to_origin()

    dancing_links = dlinks.Root()
    for sq in board.squares:
        dancing_links.add_constraint((sq.x, sq.y))
    for piece in all_positions:
        dancing_links.add_item(piece, [(sq.x, sq.y) for sq in piece.squares])

    solutions: list[list[polym.Polyomino]] = dancing_links.solve()
    print_solutions(solutions)


def simple() -> None:
    dancing_links = dlinks.Root()
    universe = "ABCDEFG"
    elements = ("CEF", "ADG", "BCF", "AD", "BG", "DEG")
    for c in universe:
        dancing_links.add_constraint(c)
    for e in elements:
        dancing_links.add_item(e, e)
    solutions = dancing_links.solve()
    assert len(solutions) == 1
    assert set(solutions[0]) == {"AD", "BG", "CEF"}
    print_solutions(solutions)


def print_solutions(solutions: list[list[T]]) -> None:
    print(f"Found {len(solutions)} solutions.")
    for i, solution in enumerate(solutions):
        print(f"Solution {i}: {solution_to_string(solution)}")


def solution_to_string(solution: list[T]) -> str:
    return ", ".join((str(item) for item in solution))


def main() -> None:
    print("Starting...")
    t_puzzle()
    print("Finished.")


if __name__ == "__main__":
    main()
