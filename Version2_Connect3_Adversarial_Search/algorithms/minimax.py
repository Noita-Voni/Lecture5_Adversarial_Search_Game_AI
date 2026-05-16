"""
Pure Minimax for Connect-3 4x4.

NOTE: Unlimited minimax on a 4x4 board can search millions of nodes
and will freeze. A depth limit is enforced (default 4) so it stays
responsive. This is intentional — it demonstrates why unlimited
minimax is impractical on larger games.
"""

def minimax(game, ai_player, max_depth=4):
    """Returns (best_move, best_score, nodes_searched)."""
    nodes = [0]

    def _search(state, is_max, depth):
        nodes[0] += 1
        if state.is_terminal():
            return state.get_utility(ai_player), None
        if depth == 0:
            return 0, None   # no heuristic — raw minimax stops here
        moves = state.get_valid_moves()
        best_move = None
        best = float('-inf') if is_max else float('inf')
        for mv in moves:
            state.make_move(*mv)
            score, _ = _search(state, not is_max, depth - 1)
            state.undo_move(*mv)
            if is_max and score > best:
                best, best_move = score, mv
            elif not is_max and score < best:
                best, best_move = score, mv
        return best, best_move

    is_max = (game.current_player == ai_player)
    score, move = _search(game, is_max, max_depth)
    return move, score, nodes[0]
