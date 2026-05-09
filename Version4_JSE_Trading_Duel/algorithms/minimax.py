"""
Minimax for JSE Trading Duel.
Each node = (turn, prices, AI_portfolio, Human_portfolio).
Both players make one action per turn. We treat it as:
  - AI is MAX player
  - Human is MIN player
  - They alternate: AI picks first each turn, then Human
  - After both pick, apply next turn's event and recurse
"""
import copy
from market import ASSETS, BUY_COST


def minimax(game, depth_limit=None):
    """
    Returns (best_action_for_current_player, score, nodes_searched).
    Call when it's the AI's turn to choose its action for the current turn.
    The search alternates AI->Human->next_turn_event->AI->...
    """
    nodes = [0]

    def _terminal_score(g):
        return g.get_utility()

    def _search_ai(g, depth):
        """AI picks its action (MAX)."""
        nodes[0] += 1
        if g.is_terminal():
            return _terminal_score(g), None
        if depth_limit is not None and depth >= depth_limit:
            return _terminal_score(g), None   # use exact utility at cutoff for simplicity

        actions = g.get_valid_actions(0)   # AI = player 0
        best, best_act = float('-inf'), None
        for act in actions:
            p = g.players[0]
            prev_cash, prev_h = p.cash, dict(p.holdings)
            g.apply_action(0, act)
            score, _ = _search_human(g, depth)
            g.undo_action(0, act, prev_cash, prev_h)
            if score > best:
                best, best_act = score, act
        return best, best_act

    def _search_human(g, depth):
        """Human picks its action (MIN)."""
        nodes[0] += 1
        actions = g.get_valid_actions(1)   # Human = player 1
        best, best_act = float('inf'), None
        for act in actions:
            p = g.players[1]
            prev_cash, prev_h = p.cash, dict(p.holdings)
            g.apply_action(1, act)
            # After both pick, advance to next turn
            g2 = g.clone()
            g2.advance_turn()
            if not g2.is_terminal():
                g2.advance_event()
            score, _ = _search_ai(g2, depth + 1)
            g.undo_action(1, act, prev_cash, prev_h)
            if score < best:
                best, best_act = score, act
        return best, best_act

    score, action = _search_ai(game, 0)
    return action, score, nodes[0]
