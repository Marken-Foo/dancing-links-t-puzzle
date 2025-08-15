import functools
from collections.abc import Iterable

import dancing_links_root as dlinks
import polycube as polyc

PolycubeTilingProblem = dlinks.Root[tuple[int, int, int], polyc.Polycube]


def _define_all_piece_orientations(
    polycubes: Iterable[polyc.Polycube],
) -> set[polyc.Polycube]:
    res = set()

    orientation_transforms = []
    for i in range(4):
        orientation_transforms.append(["RX"] * i)
        orientation_transforms.append(["RZ", "RZ"] + ["RX"] * i)
        orientation_transforms.append(["RY"] + ["RZ"] * i)
        orientation_transforms.append(["RY", "RY", "RY"] + ["RZ"] * i)
        orientation_transforms.append(["RZ"] + ["RY"] * i)
        orientation_transforms.append(["RZ", "RZ", "RZ"] + ["RY"] * i)

    for polycube in polycubes:
        for transforms in orientation_transforms:
            p: polyc.Polycube = functools.reduce(
                polyc.Polycube.apply_transform,
                transforms,
                polycube.translate_to_origin(),
            )
            res.add(p.translate_to_origin())
    return res


def _generate_piece_positions(
    box: polyc.Polycube, pieces: Iterable[polyc.Polycube]
) -> set[polyc.Polycube]:
    positions: set[polyc.Polycube] = set()
    for piece in pieces:
        positions.update(polyc.generate_positions(box, piece))
    return positions


def _initialise_dancing_links(
    box: polyc.Polycube, piece_positions: Iterable[polyc.Polycube]
) -> PolycubeTilingProblem:
    dancing_links: PolycubeTilingProblem = dlinks.Root()
    for cube in box.cubes:
        dancing_links.add_constraint(cube.to_tuple())
    for piece in piece_positions:
        dancing_links.add_item(piece, [cube.to_tuple() for cube in piece.cubes])
    return dancing_links


def prepare_problem(
    box: polyc.Polycube, pieces: Iterable[polyc.Polycube]
) -> PolycubeTilingProblem:
    all_orientations = _define_all_piece_orientations(pieces)
    positions = _generate_piece_positions(box, all_orientations)
    return _initialise_dancing_links(box, positions)
