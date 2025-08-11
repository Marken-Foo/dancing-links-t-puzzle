from collections.abc import Iterable
from itertools import product

import dancing_links_root as dlinks
import polycube as polyc


def define_box() -> polyc.Polycube:
    return polyc.Polycube(
        (polyc.Cube(x, y, z) for (x, y, z) in product(range(4), range(2), range(2)))
    ).translate_to_origin()


def define_pieces() -> list[polyc.Polycube]:
    o_tetromino = polyc.Polycube(
        (polyc.Cube(x, y, 0) for (x, y) in ((0, 0), (0, 1), (1, 0), (1, 1)))
    ).translate_to_origin()

    return [
        piece.translate_to_origin()
        for piece in (
            o_tetromino,
            o_tetromino.apply_rotations("X"),
            o_tetromino.apply_rotations("Y"),
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
    dancing_links = dlinks.Root()
    for cube in box.cubes:
        dancing_links.add_constraint((cube.x, cube.y, cube.z))
    for piece in piece_positions:
        dancing_links.add_item(
            piece, [(cube.x, cube.y, cube.z) for cube in piece.cubes]
        )
    return dancing_links


def o_tetrominos_in_4x2x2_box() -> dlinks.Root:
    box = define_box()
    pieces = define_pieces()
    positions = generate_piece_positions(box, pieces)
    return initialise_dancing_links(box, positions)


def main() -> None:
    print("=== O tetrominos in 4x2x2 box ===")
    print("Initialising dancing links...")
    dancing_links = o_tetrominos_in_4x2x2_box()
    print("Solving...")
    solutions = dancing_links.solve()
    dlinks.print_solutions(solutions)
    assert len(solutions) == 11
    print("Finished.")


if __name__ == "__main__":
    main()
