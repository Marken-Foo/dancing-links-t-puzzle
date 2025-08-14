from itertools import product
from collections.abc import Iterable

import polycube as polyc
import dancing_links_root as dlinks


def define_box() -> polyc.Polycube:
    return polyc.Polycube(
        (polyc.Cube(x, y, z) for (x, y, z) in product(range(6), range(6), range(6)))
    ).translate_to_origin()


def define_pieces() -> list[polyc.Polycube]:
    t_tetromino = polyc.Polycube(
        (polyc.Cube(x, y, 0) for (x, y) in ((0, 0), (1, 0), (2, 0), (1, 1)))
    ).translate_to_origin()

    return [
        piece.translate_to_origin()
        for piece in (
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
        )
    ]


def generate_piece_positions(
    box: polyc.Polycube, pieces: Iterable[polyc.Polycube]
) -> set[polyc.Polycube]:
    positions: set[polyc.Polycube] = set()
    for piece in pieces:
        positions.update(polyc.generate_positions(box, piece))
    return positions


def initialise_dancing_links(
    box: polyc.Polycube, piece_positions: Iterable[polyc.Polycube]
) -> dlinks.Root:
    dancing_links: dlinks.Root[tuple[int, int, int], polyc.Polycube] = dlinks.Root()
    for cube in box.cubes:
        dancing_links.add_constraint((cube.x, cube.y, cube.z))
    for piece in piece_positions:
        dancing_links.add_item(
            piece, [(cube.x, cube.y, cube.z) for cube in piece.cubes]
        )
    return dancing_links


def t_puzzle() -> dlinks.Root:
    box = define_box()
    pieces = define_pieces()
    positions = generate_piece_positions(box, pieces)
    return initialise_dancing_links(box, positions)


def main() -> None:
    print("=== T puzzle ===")
    print("Initialising dancing links...")
    dancing_links = t_puzzle()
    print("Solving...")
    solutions = dancing_links.solve(1)
    solutions.print()
    print("Finished.")


if __name__ == "__main__":
    main()
