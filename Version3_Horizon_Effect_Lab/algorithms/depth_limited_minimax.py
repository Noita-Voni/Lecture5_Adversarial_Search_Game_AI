"""Depth-limited minimax for Horizon Effect Lab."""

def depth_limited_minimax(game, ai_player, depth_limit, evaluator=None,
                          use_move_ordering=False, move_orderer=None,
                          use_pruning=True, transposition_table=None):
    """
    Returns (best_move, best_score, nodes_searched, branches_pruned, cache_hits).
    use_pruning: if False, runs pure minimax (no alpha-beta).
    transposition_table: optional TranspositionTable instance.
    """
    nodes   = [0]
    pruned  = [0]
    hits    = [0]

    def board_key(state):
        return tuple(tuple(row) for row in state.board) + (state.current_player,)

    def _search(state, depth, alpha, beta, is_max):
        nodes[0] += 1

        # Transposition table lookup
        if transposition_table is not None:
            key = board_key(state)
            cached = transposition_table.get(key, depth)
            if cached is not None:
                hits[0] += 1
                return cached, None

        if state.is_terminal():
            score = state.get_utility(ai_player) * 100
            if transposition_table is not None:
                transposition_table.put(board_key(state), depth, score)
            return score, None

        if depth == 0:
            score = evaluator.evaluate(state) if evaluator else 0
            if transposition_table is not None:
                transposition_table.put(board_key(state), depth, score)
            return score, None

        moves = state.get_valid_moves()
        if use_move_ordering and move_orderer:
            moves = move_orderer.order_moves(state, moves, is_max)

        best_move = None
        best = float('-inf') if is_max else float('inf')

        for mv in moves:
            state.make_move(*mv)
            score, _ = _search(state, depth-1, alpha, beta, not is_max)
            state.undo_move(*mv)

            if is_max:
                if score > best: best, best_move = score, mv
                if use_pruning:
                    alpha = max(alpha, best)
                    if beta <= alpha: pruned[0] += 1; break
            else:
                if score < best: best, best_move = score, mv
                if use_pruning:
                    beta = min(beta, best)
                    if beta <= alpha: pruned[0] += 1; break

        if transposition_table is not None:
            transposition_table.put(board_key(state), depth, best)
        return best, best_move

    is_max = (game.current_player == ai_player)
    score, move = _search(game, depth_limit, float('-inf'), float('inf'), is_max)
    return move, score, nodes[0], pruned[0], hits[0]
