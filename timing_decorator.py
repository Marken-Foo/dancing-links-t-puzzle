from collections.abc import Callable
from functools import wraps
from time import time
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def time_execution(f: Callable[P, R]) -> Callable[P, tuple[R, float]]:
    @wraps(f)
    def wrap(*args: P.args, **kwargs: P.kwargs) -> tuple[R, float]:
        start_time = time()
        result = f(*args, **kwargs)
        end_time = time()
        elapsed_time = end_time - start_time
        return (result, elapsed_time)

    return wrap
