import functools
from collections.abc import Iterable

import dancing_links_root as dlinks
import polyomino as polym

PolyominoTilingProblem = dlinks.Root[tuple[int, int], polym.Polyomino]


def _define_all_piece_orientations(
    polyominos: Iterable[polym.Polyomino],
) -> set[polym.Polyomino]:
    res = set()
    orientation_transforms: list[list[str]] = [
        [],
        ["R+"],
        ["R+", "R+"],
        ["R-"],
        ["MX"],
        ["MX", "R+"],
        ["MX", "R+", "R+"],
        ["MX", "R-"],
    ]
    for polyomino in polyominos:
        for transforms in orientation_transforms:
            p: polym.Polyomino = functools.reduce(
                polym.Polyomino.apply_transform,
                transforms,
                polyomino.translate_to_origin(),
            )
            res.add(p.translate_to_origin())
    return res


def _generate_piece_positions(
    board: polym.Polyomino, pieces: Iterable[polym.Polyomino]
) -> set[polym.Polyomino]:
    positions: set[polym.Polyomino] = set()
    for piece in pieces:
        positions.update(polym.generate_positions(board, piece))
    return positions


def _initialise_dancing_links(
    board: polym.Polyomino, piece_positions: Iterable[polym.Polyomino]
) -> PolyominoTilingProblem:
    dancing_links: PolyominoTilingProblem = dlinks.Root()
    for sq in board.squares:
        dancing_links.add_constraint(sq.to_tuple())
    for piece in piece_positions:
        dancing_links.add_item(piece, [sq.to_tuple() for sq in piece.squares])
    return dancing_links


def prepare_problem(
    board: polym.Polyomino, pieces: Iterable[polym.Polyomino]
) -> PolyominoTilingProblem:
    all_orientations = _define_all_piece_orientations(pieces)
    positions = _generate_piece_positions(board, all_orientations)
    return _initialise_dancing_links(board, positions)
