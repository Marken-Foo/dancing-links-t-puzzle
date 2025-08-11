import problems.knuth_example as knuth_example
from time_solving import time_n_solves


def main() -> None:
    print("See other files for example problems.")
    knuth_example.main()
    print("=======")
    time_n_solves("Knuth's example", knuth_example.knuth_example, 1000)


if __name__ == "__main__":
    main()
