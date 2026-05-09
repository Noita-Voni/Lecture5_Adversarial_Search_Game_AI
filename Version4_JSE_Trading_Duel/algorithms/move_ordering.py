"""Move ordering for JSE Trading Duel - rank actions by expected value."""
from market import ASSETS


class MoveOrderer:
    def order_actions(self, game, actions, is_max):
        """Sort: BUY rising asset first, SELL falling asset first, HOLD last."""
        turn = game.turn
        evt  = game.market.peek_event(turn) if turn < 5 else None

        def score(act):
            if evt and evt['asset']:
                rising  = evt['pct'] > 0
                falling = evt['pct'] < 0
                asset   = evt['asset']
                if is_max:
                    if rising  and act == f'BUY_{asset}':  return 0
                    if falling and act == f'SELL_{asset}': return 1
                else:
                    if falling and act == f'BUY_{asset}':  return 0
                    if rising  and act == f'SELL_{asset}': return 1
            if act.startswith('BUY'):   return 3
            if act.startswith('SELL'):  return 4
            return 5  # HOLD last
        return sorted(actions, key=score)
