from collections.abc import Iterable
from itertools import product

import dancing_links_root as dlinks
import polyomino as polym


def define_board() -> polym.Polyomino:
    return polym.Polyomino(
        (polym.Square(x, y) for (x, y) in product(range(4), range(4)))
    ).translate_to_origin()


def define_pieces() -> list[polym.Polyomino]:
    l_tetromino = polym.Polyomino(
        (polym.Square(x, y) for (x, y) in ((0, 0), (1, 0), (2, 0), (0, 1)))
    ).translate_to_origin()

    return [
        piece.translate_to_origin()
        for piece in (
            l_tetromino,
            l_tetromino.reflect_about_x_axis(),
            l_tetromino.rotate_anticlockwise(),
            l_tetromino.reflect_about_x_axis().rotate_anticlockwise(),
            l_tetromino.rotate_anticlockwise().rotate_anticlockwise(),
            l_tetromino.reflect_about_x_axis()
            .rotate_anticlockwise()
            .rotate_anticlockwise(),
            l_tetromino.rotate_anticlockwise()
            .rotate_anticlockwise()
            .rotate_anticlockwise(),
            l_tetromino.reflect_about_x_axis()
            .rotate_anticlockwise()
            .rotate_anticlockwise()
            .rotate_anticlockwise(),
        )
    ]


def generate_piece_positions(
    board: polym.Polyomino, pieces: Iterable[polym.Polyomino]
) -> set[polym.Polyomino]:
    positions: set[polym.Polyomino] = set()
    for piece in pieces:
        positions.update(polym.generate_positions(board, piece))
    return positions


def initialise_dancing_links(
    board: polym.Polyomino, piece_positions: Iterable[polym.Polyomino]
) -> dlinks.Root:
    dancing_links = dlinks.Root()
    for sq in board.squares:
        dancing_links.add_constraint((sq.x, sq.y))
    for piece in piece_positions:
        dancing_links.add_item(piece, [(sq.x, sq.y) for sq in piece.squares])
    return dancing_links


def l_tetrominos_in_4x4_board() -> dlinks.Root:
    board = define_board()
    pieces = define_pieces()
    positions = generate_piece_positions(board, pieces)
    return initialise_dancing_links(board, positions)


def main() -> None:
    print("=== L tetrominos in 4x4 board ===")
    print("Initialising dancing links...")
    dancing_links = l_tetrominos_in_4x4_board()
    print("Solving...")
    solutions = dancing_links.solve()
    dlinks.print_solutions(solutions)
    assert len(solutions) == 10
    print("Finished.")


if __name__ == "__main__":
    main()
