"""Market model for JSE Trading Duel - prices, events, asset management."""
import random

ASSETS = ['BANK', 'MINING', 'RETAIL']

BASE_PRICES = {'BANK': 200, 'MINING': 150, 'RETAIL': 120}

EVENTS = [
    {'name': 'BULL_BANK',    'desc': 'Banking sector surges',   'asset': 'BANK',   'pct': +0.20},
    {'name': 'BEAR_BANK',    'desc': 'Banking sector slumps',   'asset': 'BANK',   'pct': -0.15},
    {'name': 'BULL_MINING',  'desc': 'Mining boom',             'asset': 'MINING', 'pct': +0.25},
    {'name': 'BEAR_MINING',  'desc': 'Mining slump',            'asset': 'MINING', 'pct': -0.20},
    {'name': 'BULL_RETAIL',  'desc': 'Retail rally',            'asset': 'RETAIL', 'pct': +0.15},
    {'name': 'BEAR_RETAIL',  'desc': 'Retail sell-off',         'asset': 'RETAIL', 'pct': -0.10},
    {'name': 'NEUTRAL',      'desc': 'Markets steady',          'asset': None,     'pct': 0.0},
]

ACTIONS = ['BUY_BANK', 'BUY_MINING', 'BUY_RETAIL',
           'SELL_BANK', 'SELL_MINING', 'SELL_RETAIL', 'HOLD']

BUY_COST = 200   # fixed cost per unit purchased


class Market:
    def __init__(self, seed=None):
        self._rng = random.Random(seed)
        self.prices = dict(BASE_PRICES)
        # Pre-generate a fixed sequence of events for this game
        self.event_sequence = [self._rng.choice(EVENTS) for _ in range(5)]
        self.current_event = None

    def apply_event(self, turn):
        """Apply the event for this turn (0-indexed). Returns the event dict."""
        evt = self.event_sequence[turn]
        if evt['asset'] is not None:
            self.prices[evt['asset']] = max(
                10, int(self.prices[evt['asset']] * (1 + evt['pct']))
            )
        self.current_event = evt
        return evt

    def peek_event(self, turn):
        """Return event without applying it."""
        return self.event_sequence[turn] if turn < len(self.event_sequence) else EVENTS[-1]

    def portfolio_value(self, cash, holdings):
        """Compute total portfolio value."""
        return cash + sum(holdings.get(a, 0) * self.prices[a] for a in ASSETS)

    def simulate_event(self, prices, event):
        """Return new prices after applying event (non-destructive)."""
        new_p = dict(prices)
        if event['asset'] is not None:
            new_p[event['asset']] = max(10, int(new_p[event['asset']] * (1 + event['pct'])))
        return new_p

    def reset(self, seed=None):
        self._rng = random.Random(seed)
        self.prices = dict(BASE_PRICES)
        self.event_sequence = [self._rng.choice(EVENTS) for _ in range(5)]
        self.current_event = None
