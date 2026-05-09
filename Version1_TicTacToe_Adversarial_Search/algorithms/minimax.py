"""Pure Minimax - explores the full game tree with no pruning."""

def minimax(game, ai_player):
    """Returns (best_move, best_score, nodes_searched)."""
    nodes = [0]

    def _search(state, is_max):
        nodes[0] += 1
        if state.is_terminal():
            return state.get_utility(ai_player), None
        moves = state.get_valid_moves()
        best_move = None
        best = float('-inf') if is_max else float('inf')
        for mv in moves:
            state.make_move(*mv)
            score, _ = _search(state, not is_max)
            state.undo_move(*mv)
            if is_max and score > best:
                best, best_move = score, mv
            elif not is_max and score < best:
                best, best_move = score, mv
        return best, best_move

    is_max = (game.current_player == ai_player)
    score, move = _search(game, is_max)
    return move, score, nodes[0]
