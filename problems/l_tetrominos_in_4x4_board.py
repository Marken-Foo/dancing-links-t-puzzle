from itertools import product

import polyomino as polym
import polyomino_tiling as polym_tiling


def l_tetrominos_in_4x4_board() -> polym_tiling.PolyominoTilingProblem:
    board = polym.Polyomino(
        (polym.Square(x, y) for (x, y) in product(range(4), range(4)))
    )
    l_tetromino = polym.Polyomino(
        (polym.Square(x, y) for (x, y) in ((0, 0), (1, 0), (2, 0), (0, 1)))
    )
    return polym_tiling.prepare_problem(board, [l_tetromino])


def main() -> None:
    print("=== L tetrominos in 4x4 board ===")
    print("Initialising dancing links...")
    dancing_links = l_tetrominos_in_4x4_board()
    print("Solving...")
    solutions = dancing_links.solve()
    solutions.print()
    assert solutions.size == 10
    print("Finished.")


if __name__ == "__main__":
    main()
