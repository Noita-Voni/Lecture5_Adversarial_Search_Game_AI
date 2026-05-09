"""
Heuristic evaluation for JSE Trading Duel at non-terminal states.
Considers: portfolio value, cash reserve, diversification, risk exposure,
upcoming event effect, and opponent comparison.
"""
from market import ASSETS


class HeuristicEvaluator:
    def __init__(self):
        self.last_breakdown = {}

    def evaluate(self, game, ai_idx=0):
        """Return heuristic score from AI perspective."""
        bd = {}
        opp_idx = 1 - ai_idx

        ai_val  = game.portfolio_value(ai_idx)
        opp_val = game.portfolio_value(opp_idx)
        bd['portfolio_diff'] = ai_val - opp_val

        # Cash reserve bonus (having cash gives flexibility)
        ai_cash = game.players[ai_idx].cash
        bd['cash_reserve'] = ai_cash * 0.05

        # Diversification bonus
        ai_h = game.players[ai_idx].holdings
        held = sum(1 for a in ASSETS if ai_h[a] > 0)
        bd['diversification'] = held * 20

        # Upcoming event bonus: do we hold the rising asset?
        if game.turn < 5:
            next_evt = game.market.peek_event(game.turn)
            if next_evt['asset'] and next_evt['pct'] > 0:
                bonus = ai_h.get(next_evt['asset'], 0) * next_evt['pct'] * game.market.prices[next_evt['asset']]
                bd['event_advantage'] = bonus
            else:
                bd['event_advantage'] = 0
        else:
            bd['event_advantage'] = 0

        # Risk: penalise over-concentration
        total_h = sum(ai_h.values())
        if total_h > 2:
            max_single = max(ai_h.values())
            concentration = max_single / total_h
            bd['risk_penalty'] = -(concentration - 0.5) * 30
        else:
            bd['risk_penalty'] = 0

        self.last_breakdown = bd
        return sum(bd.values())
