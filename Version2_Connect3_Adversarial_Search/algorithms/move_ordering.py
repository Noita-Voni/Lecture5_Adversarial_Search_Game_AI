"""Move ordering for Connect-3 4x4 - center cells first."""

class MoveOrderer:
    # Priority: center cells > inner ring > outer ring
    _PRIORITY = {}
    for _r in range(4):
        for _c in range(4):
            _center_dist = abs(_r - 1.5) + abs(_c - 1.5)
            _PRIORITY[(_r, _c)] = _center_dist

    def order_moves(self, state, moves, is_maximizing):
        return sorted(moves, key=lambda m: self._PRIORITY.get(m, 9))

    def score_move_quick(self, state, move):
        return -self._PRIORITY.get(move, 9)
