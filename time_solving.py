from collections.abc import Callable
from typing import Any

import dancing_links_root as dlinks
from timing_decorator import time_execution


@time_execution
def measure_solve_time(problem: dlinks.Root) -> Any:
    return problem.solve()


def time_n_solves(
    label: str, initialise_problem: Callable[..., dlinks.Root], num_iterations: int
) -> None:
    solve_times = []
    for _ in range(num_iterations):
        problem = initialise_problem()
        (_, t) = measure_solve_time(problem)
        solve_times.append(t)
    total_time = sum(solve_times)
    print(f"Solved {label} {num_iterations} times.")
    print(f"Total time: {total_time:.4f}")
    print(f"Average time: {(total_time / num_iterations):.4f}")
