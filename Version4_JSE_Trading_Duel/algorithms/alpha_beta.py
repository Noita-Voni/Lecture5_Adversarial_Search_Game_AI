"""Alpha-Beta pruning for JSE Trading Duel."""
import copy


def alpha_beta(game, depth_limit=None, use_move_ordering=False, move_orderer=None):
    """
    Returns (best_action, score, nodes_searched, branches_pruned).
    """
    nodes  = [0]
    pruned = [0]

    def _search_ai(g, depth, alpha, beta):
        nodes[0] += 1
        if g.is_terminal():
            return g.get_utility(), None
        if depth_limit is not None and depth >= depth_limit:
            return g.get_utility(), None

        actions = g.get_valid_actions(0)
        if use_move_ordering and move_orderer:
            actions = move_orderer.order_actions(g, actions, is_max=True)

        best, best_act = float('-inf'), None
        for act in actions:
            p = g.players[0]
            prev_cash, prev_h = p.cash, dict(p.holdings)
            g.apply_action(0, act)
            score, _ = _search_human(g, depth, alpha, beta)
            g.undo_action(0, act, prev_cash, prev_h)
            if score > best:
                best, best_act = score, act
            alpha = max(alpha, best)
            if beta <= alpha:
                pruned[0] += 1
                break
        return best, best_act

    def _search_human(g, depth, alpha, beta):
        nodes[0] += 1
        actions = g.get_valid_actions(1)
        if use_move_ordering and move_orderer:
            actions = move_orderer.order_actions(g, actions, is_max=False)

        best, best_act = float('inf'), None
        for act in actions:
            p = g.players[1]
            prev_cash, prev_h = p.cash, dict(p.holdings)
            g.apply_action(1, act)
            g2 = g.clone()
            g2.advance_turn()
            if not g2.is_terminal():
                g2.advance_event()
            score, _ = _search_ai(g2, depth + 1, alpha, beta)
            g.undo_action(1, act, prev_cash, prev_h)
            if score < best:
                best, best_act = score, act
            beta = min(beta, best)
            if beta <= alpha:
                pruned[0] += 1
                break
        return best, best_act

    score, action = _search_ai(game, 0, float('-inf'), float('inf'))
    return action, score, nodes[0], pruned[0]
