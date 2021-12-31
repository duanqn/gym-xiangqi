

class PositionDiff:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
    
    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def repeat(self, n):
        return PositionDiff(self.row * n, self.col * n)

class Position:
    def __init__(self, row, col):
        self._row = row
        self._col = col
    
    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def applyDiff(self, diff: PositionDiff):
        return Position(self.row + diff.row, self.col + diff.col)

    def diff(self, other) -> PositionDiff:
        return PositionDiff(self.row - other.row, self.col - other.col)
