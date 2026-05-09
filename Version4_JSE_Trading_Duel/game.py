"""JSE Trading Duel game state and rules."""
import copy
from market import Market, ASSETS, ACTIONS, BUY_COST

MAX_TURNS   = 5
AI_IDX      = 0   # player index
HUMAN_IDX   = 1


class PlayerState:
    def __init__(self):
        self.cash     = 1000
        self.holdings = {a: 0 for a in ASSETS}
        self.history  = []   # list of action strings

    def clone(self):
        ps = PlayerState()
        ps.cash     = self.cash
        ps.holdings = dict(self.holdings)
        ps.history  = list(self.history)
        return ps


class GameState:
    def __init__(self, market=None):
        self.market  = market or Market()
        self.turn    = 0          # 0..4 (5 turns total)
        self.phase   = 'event'    # 'event' -> apply event, then 'ai_move' -> 'human_move' -> next turn
        self.players = [PlayerState(), PlayerState()]   # [AI, Human]
        self.current_event = None
        self.game_over = False
        self.winner    = None   # 0=AI wins, 1=Human wins, None=draw
        self.ai_last_action    = None
        self.human_last_action = None

    # ── utility helpers ───────────────────────────────────────────────────────

    def portfolio_value(self, player_idx):
        p = self.players[player_idx]
        return self.market.portfolio_value(p.cash, p.holdings)

    def get_utility(self, ai_player_idx=AI_IDX):
        return self.portfolio_value(ai_player_idx) - self.portfolio_value(1 - ai_player_idx)

    # ── valid actions ─────────────────────────────────────────────────────────

    def get_valid_actions(self, player_idx):
        p   = self.players[player_idx]
        act = ['HOLD']
        for asset in ASSETS:
            if p.cash >= BUY_COST:
                act.append(f'BUY_{asset}')
            if p.holdings[asset] > 0:
                act.append(f'SELL_{asset}')
        return act

    # ── apply / undo ──────────────────────────────────────────────────────────

    def apply_action(self, player_idx, action):
        p = self.players[player_idx]
        p.history.append(action)
        if action.startswith('BUY_'):
            asset = action[4:]
            if p.cash >= BUY_COST:
                p.cash -= BUY_COST
                p.holdings[asset] += 1
        elif action.startswith('SELL_'):
            asset = action[5:]
            if p.holdings[asset] > 0:
                p.cash += self.market.prices[asset]
                p.holdings[asset] -= 1
        # HOLD: nothing

    def undo_action(self, player_idx, action, prev_cash, prev_holdings):
        p = self.players[player_idx]
        p.cash     = prev_cash
        p.holdings = prev_holdings
        if p.history:
            p.history.pop()

    # ── event ─────────────────────────────────────────────────────────────────

    def advance_event(self):
        """Apply the market event for current turn. Call once per turn."""
        self.current_event = self.market.apply_event(self.turn)

    # ── turn management ───────────────────────────────────────────────────────

    def advance_turn(self):
        self.turn += 1
        if self.turn >= MAX_TURNS:
            self.game_over = True
            diff = self.get_utility()
            if diff > 0:   self.winner = AI_IDX
            elif diff < 0: self.winner = HUMAN_IDX
            else:          self.winner = None

    def is_terminal(self):
        return self.game_over

    # ── cloning ───────────────────────────────────────────────────────────────

    def clone(self):
        g = GameState.__new__(GameState)
        g.market   = copy.deepcopy(self.market)
        g.turn     = self.turn
        g.phase    = self.phase
        g.players  = [p.clone() for p in self.players]
        g.current_event  = self.current_event
        g.game_over      = self.game_over
        g.winner         = self.winner
        g.ai_last_action    = self.ai_last_action
        g.human_last_action = self.human_last_action
        return g
