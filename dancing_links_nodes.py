class ColumnHeader:
    def __init__(self, constraint, left, right, up=None, down=None):
        self.constraint = constraint
        self.left = left
        self.right = right
        self.up = self if up is None else up
        self.down = self if down is None else down
        self.size = 0

    def __str__(self) -> str:
        return f"Column({self.constraint}, size: {self.size})"

    def _coords(self):
        return f"Column header {self.constraint}"

    def add_item(self, data):
        obj = DataObject(column=self, data=data, up=self.up, down=self)
        self.up.down = obj
        self.up = obj
        self.size += 1
        return obj

    def cover(self) -> None:
        # print(f"Covering column: {self.constraint}")
        self.right.left = self.left
        self.left.right = self.right

        row = self.down
        while row is not self:
            node = row.right
            while node is not row:
                node.unlink_vertical()
                node = node.right
            row = row.down

    def uncover(self) -> None:
        # print(f"Uncovering column: {self.constraint}")
        row = self.up
        while row is not self:
            node = row.left
            while node is not row:
                node.relink_vertical()
                node = node.left
            row = row.up

        self.left.right = self
        self.right.left = self


class DataObject:
    def __init__(self, column, data, up=None, down=None):
        self.up = self if up is None else up
        self.down = self if down is None else down
        self.left = self
        self.right = self
        self.column = column
        self.data = data

    def __str__(self):
        return f"{self._coords()} |U:{self.up._coords()}|D:{self.down._coords()}|L:{self.left._coords()}|R:{self.right._coords()}|"

    def _coords(self):
        return f"{self.column.constraint} of {self.data}"

    def link_horizontal(self, left, right) -> None:
        self.left = left
        self.right = right
        left.right = self
        right.left = self

    def unlink_vertical(self) -> None:
        # print(f"Unlinking {self}")
        self.down.up = self.up
        self.up.down = self.down
        self.column.size -= 1

    def relink_vertical(self) -> None:
        # print(f"Relinking {self}")
        self.column.size += 1
        self.up.down = self
        self.down.up = self
