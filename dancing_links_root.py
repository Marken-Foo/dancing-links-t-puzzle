from itertools import chain, cycle, islice
from dancing_links_nodes import ColumnHeader


class Root:
    def __init__(self) -> None:
        self.left = self
        self.right = self
        self.constraints = {}
        self.items = []

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

    def add_constraint(self, constraint) -> None:
        new_column = ColumnHeader(constraint, self.left, self)
        self.left.right = new_column
        self.left = new_column
        self.constraints[constraint] = new_column

    def add_item(self, data, constraints) -> None:
        if len(constraints) == 0:
            return
        row_objects = []
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

    def solve(self):
        solutions = self._search([], [])
        return solutions

    def _search(self, partial_solution, solutions):
        # print(f"Entering search with partial solution: {partial_solution}")

        # print(f"Found solutions: {solutions}")

        # print(f"State: {self}")
        if len(solutions) > 0:
            return solutions

        if self._is_empty():
            # print("Found a solution")
            return solutions.append(partial_solution)

        column = self._find_smallest_column()
        assert column is not None
        column.cover()

        row = column.down
        while row is not column:
            # print(f"Choosing item: {row}")
            node = row.right
            while node is not row:
                node.column.cover()
                node = node.right
            _partial_solution = partial_solution + [row.data]
            self._search(_partial_solution, solutions)
            node = row.left
            while node is not row:
                node.column.uncover()
                node = node.left
            row = row.down
        column.uncover()
        return solutions

    def _is_empty(self):
        return self.left is self and self.right is self

    def _find_smallest_column(self):
        column = None
        next_column = self.right
        while next_column is not self:
            if column is None or next_column.size < column.size:
                column = next_column
            next_column = next_column.right
        return column
