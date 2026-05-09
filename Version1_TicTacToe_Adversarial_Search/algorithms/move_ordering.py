"""Move ordering heuristics to improve alpha-beta pruning efficiency."""

class MoveOrderer:
    def order_moves(self, state, moves, is_maximizing):
        """Order: center first, then corners, then edges."""
        def priority(mv):
            r, c = mv
            if (r, c) == (1, 1): return 0
            if (r, c) in [(0,0),(0,2),(2,0),(2,2)]: return 1
            return 2
        return sorted(moves, key=priority)
