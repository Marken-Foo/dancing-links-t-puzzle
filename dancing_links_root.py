from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from itertools import chain, cycle, islice
from typing import Generic, TypeVar

from dancing_links_nodes import ColumnHeader, DataObject


C = TypeVar("C")
T = TypeVar("T")


class Root(Generic[C, T]):
    def __init__(self) -> None:
        self.left: ColumnHeader | Root[C, T] = self
        self.right: ColumnHeader | Root[C, T] = self
        self.constraints: dict[C, ColumnHeader] = {}
        self.items: list[T] = []

    def __str__(self) -> str:
        column = self.right
        columns = []
        while column is not self:
            columns.append(column)
            column = column.right
        return (
            "Constraints(\n  "
            + "\n  ".join((str(col) for col in columns))
            + "\n)\n"
            + f"Items: {self.items}"
        )

    def add_constraint(self, constraint: C) -> None:
        new_column = ColumnHeader(constraint, self.left, self)
        self.left.right = new_column
        self.left = new_column
        self.constraints[constraint] = new_column

    def add_item(self, data: T, constraints: Sequence[C]) -> None:
        if len(constraints) == 0:
            return
        row_objects: list[DataObject] = []
        for constraint in constraints:
            # Ensure constraint has been defined
            column = self.constraints.get(constraint, None)
            if column is None:
                self.add_constraint(constraint)
                column = self.constraints[constraint]
            row_objects.append(column.add_item(data))
        assert len(row_objects) > 0
        # No guarantee, nor need, for different rows to have the same order of constraints.
        for left, obj, right in zip(
            chain((row_objects[-1],), cycle(row_objects)),
            row_objects,
            cycle(chain(islice(row_objects, 1, None), (row_objects[0],))),
        ):
            obj.link_horizontal(left=left, right=right)
        self.items.append(data)

    def solve(self, max_num_solutions=None) -> Solutions[T]:
        solutions = self._search([], [], max_num_solutions)
        return Solutions((Solution(s) for s in solutions))

    def _search(
        self,
        partial_solution: list[T],
        solutions: list[list[T]],
        max_num_solutions: int | None = None,
    ) -> list[list[T]]:
        if max_num_solutions is not None and len(solutions) >= max_num_solutions:
            return solutions

        if self._is_empty():
            solutions.append(partial_solution)
            return solutions

        column = self._find_smallest_column()
        assert column is not None
        column.cover()

        row = column.down
        while row is not column:
            # Choose item corresponding to row
            node = row.right
            while node is not row:
                node.column.cover()
                node = node.right
            _partial_solution = partial_solution + [row.data]
            self._search(_partial_solution, solutions, max_num_solutions)
            # Unchoose item corresponding to row
            node = row.left
            while node is not row:
                node.column.uncover()
                node = node.left
            row = row.down
        column.uncover()
        return solutions

    def _is_empty(self) -> bool:
        return self.left is self and self.right is self

    def _find_smallest_column(self):
        column = None
        next_column = self.right
        while next_column is not self:
            if column is None or next_column.size < column.size:
                column = next_column
            next_column = next_column.right
        return column


class Solution(Generic[T]):
    def __init__(self, solution: Iterable[T]) -> None:
        self.solution: list[T] = list(solution)

    def __str__(self) -> str:
        return ", ".join((str(item) for item in self.solution))

    def __iter__(self) -> Iterator[T]:
        return self.solution.__iter__()


class Solutions(Generic[T]):
    def __init__(self, solutions: Iterable[Solution[T]]) -> None:
        self.solutions: list[Solution[T]] = list(solutions)

    @property
    def size(self) -> int:
        return len(self.solutions)

    def print(self) -> None:
        print(f"Found {len(self.solutions)} solutions.")
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i}: {solution}")

    def __iter__(self) -> Iterator[Solution[T]]:
        return self.solutions.__iter__()

    def __getitem__(self, key):
        return self.solutions.__getitem__(key)
