from __future__ import annotations


class Board:
    def __init__(self, rows: int, columns: int, layout: list):
        self.rows = rows
        self.columns = columns
        self.layout = layout

    @classmethod
    def empty(cls) -> Board:
        return Board(0, 0, [])

    def __eq__(self, other):
        if isinstance(other, Board):
            return self.rows == other.rows and self.columns == other.columns and self.layout == other.layout
        return False
