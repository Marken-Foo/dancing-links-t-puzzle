from itertools import product

import polycube as polyc
import polycube_tiling as polyc_tiling


def t_puzzle() -> polyc_tiling.PolycubeTilingProblem:
    box = polyc.Polycube(
        (polyc.Cube(x, y, z) for (x, y, z) in product(range(6), range(6), range(6)))
    )
    t_tetromino = polyc.Polycube(
        (polyc.Cube(x, y, 0) for (x, y) in ((0, 0), (1, 0), (2, 0), (1, 1)))
    )
    return polyc_tiling.prepare_problem(box, [t_tetromino])


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
