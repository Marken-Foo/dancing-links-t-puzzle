import problems.t_puzzle as t_puzzle
import polycube_drawing


def main() -> None:
    solutions = t_puzzle.t_puzzle().solve(1)
    if not solutions:
        print("No solutions found.")
        return
    solution = solutions[0]
    polycube_drawing.print_polycube_tiling_layers(solution.solution)
    polycube_drawing.draw_polycubes_tiling(solution.solution)


if __name__ == "__main__":
    main()
