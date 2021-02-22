from dataclasses import dataclass

from typing import List


@dataclass
class TableRow:
    pass


class Table:
    def __init__(self, rows: List[TableRow]):
        self.idx = 0
        self.rows = rows

    def __next__(self):
        self.idx += 1
        try:
            return self.rows[self.idx - 1]
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)
