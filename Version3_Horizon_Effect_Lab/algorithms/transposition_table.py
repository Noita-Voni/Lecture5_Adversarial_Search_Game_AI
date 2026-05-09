"""Transposition table (memoisation cache) for game states."""

class TranspositionTable:
    """
    Stores previously evaluated positions to avoid re-computation.
    Key: tuple board state.  Value: (depth, score).
    Only valid if stored depth >= requested depth.
    """
    def __init__(self):
        self._table = {}
        self.hits   = 0
        self.stores = 0

    def get(self, key, depth):
        entry = self._table.get(key)
        if entry is not None:
            stored_depth, score = entry
            if stored_depth >= depth:
                self.hits += 1
                return score
        return None

    def put(self, key, depth, score):
        existing = self._table.get(key)
        if existing is None or existing[0] <= depth:
            self._table[key] = (depth, score)
            self.stores += 1

    def clear(self):
        self._table.clear()
        self.hits   = 0
        self.stores = 0

    def size(self):
        return len(self._table)
