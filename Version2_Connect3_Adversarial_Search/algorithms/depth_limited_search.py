"""Depth-limited minimax with alpha-beta for Connect-3."""

def depth_limited_minimax(game, ai_player, depth_limit, evaluator=None,
                          use_move_ordering=False, move_orderer=None):
    """Returns (best_move, best_score, nodes_searched, branches_pruned)."""
    nodes = [0]
    pruned = [0]

    def _search(state, depth, alpha, beta, is_max):
        nodes[0] += 1
        if state.is_terminal():
            return state.get_utility(ai_player) * 100, None
        if depth == 0:
            score = evaluator.evaluate(state) if evaluator else 0
            return score, None
        moves = state.get_valid_moves()
        if use_move_ordering and move_orderer:
            moves = move_orderer.order_moves(state, moves, is_max)
        best_move = None
        best = float('-inf') if is_max else float('inf')
        for mv in moves:
            state.make_move(*mv)
            score, _ = _search(state, depth - 1, alpha, beta, not is_max)
            state.undo_move(*mv)
            if is_max:
                if score > best: best, best_move = score, mv
                alpha = max(alpha, best)
                if beta <= alpha: pruned[0] += 1; break
            else:
                if score < best: best, best_move = score, mv
                beta = min(beta, best)
                if beta <= alpha: pruned[0] += 1; break
        return best, best_move

    is_max = (game.current_player == ai_player)
    score, move = _search(game, depth_limit, float('-inf'), float('inf'), is_max)
    return move, score, nodes[0], pruned[0]
