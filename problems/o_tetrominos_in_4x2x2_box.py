from itertools import product

import polycube as polyc
import polycube_tiling as polyc_tiling


def o_tetrominos_in_4x2x2_box() -> polyc_tiling.PolycubeTilingProblem:
    box = polyc.Polycube(
        (polyc.Cube(x, y, z) for (x, y, z) in product(range(4), range(2), range(2)))
    )
    o_tetromino = polyc.Polycube(
        (polyc.Cube(x, y, 0) for (x, y) in ((0, 0), (0, 1), (1, 0), (1, 1)))
    )
    return polyc_tiling.prepare_problem(box, [o_tetromino])


def main() -> None:
    print("=== O tetrominos in 4x2x2 box ===")
    print("Initialising dancing links...")
    dancing_links = o_tetrominos_in_4x2x2_box()
    print("Solving...")
    solutions = dancing_links.solve()
    solutions.print()
    assert solutions.size == 11
    print("Finished.")


if __name__ == "__main__":
    main()
