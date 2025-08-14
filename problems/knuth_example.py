import dancing_links_root as dlinks


def knuth_example() -> dlinks.Root:
    dancing_links: dlinks.Root[str, str] = dlinks.Root()
    universe = "ABCDEFG"
    elements = ("CEF", "ADG", "BCF", "AD", "BG", "DEG")
    for c in universe:
        dancing_links.add_constraint(c)
    for e in elements:
        dancing_links.add_item(e, e)
    return dancing_links


def main() -> None:
    print("=== Knuth's example problem ===")
    print("Initialising dancing links...")
    problem = knuth_example()
    print("Solving...")
    solutions = problem.solve()
    solutions.print
    assert solutions.size == 1
    assert set(solutions[0]) == {"AD", "BG", "CEF"}
    print("Finished.")


if __name__ == "__main__":
    main()
