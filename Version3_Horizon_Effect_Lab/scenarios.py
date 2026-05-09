"""
Preset horizon-effect scenarios.
Each scenario has a board state where a threat exists just beyond shallow depth.
"""

SCENARIOS = {}

# ─────────────────────────────────────────────────────────────
# Scenario 1 (4x4): Horizon Effect Classic
# X has a winning fork threat at depth 3 but shallow search misses it.
# At depth=1, AI (O) defends the wrong threat; at depth=3 it sees the fork.
SCENARIOS['horizon_classic'] = {
    'name':        "Horizon Effect – Classic Fork",
    'description': (
        "X has two threats that together form a fork. "
        "At depth<=2 the AI (O) defends only one threat. "
        "At depth>=3 it sees both and finds the fork-blocking move."
    ),
    'rows': 4, 'cols': 4, 'win_len': 3,
    'board': [
        ['X',  None, 'X',  None],
        [None, 'X',  None, None],
        ['O',  None, 'O',  None],
        [None, None, None, None],
    ],
    'current_player': 'O',
    'warning': "Depth <= 2 misses X's diagonal fork! Try depth 1 vs depth 3.",
}

# ─────────────────────────────────────────────────────────────
# Scenario 2 (4x4): Delayed Threat
# O is one move from winning but the winning move is at position (3,3).
# A very shallow AI might block an unimportant threat instead.
SCENARIOS['delayed_threat'] = {
    'name':        "Delayed Winning Threat",
    'description': (
        "O can win in 1 move at (3,3), but depth=0 heuristic "
        "might score other moves higher. Watch heuristic vs exact."
    ),
    'rows': 4, 'cols': 4, 'win_len': 3,
    'board': [
        ['X',  'X',  None, None],
        ['O',  'O',  None, None],
        ['X',  None, 'X',  None],
        ['O',  None, None, None],
    ],
    'current_player': 'O',
    'warning': "O wins immediately at (1,2)! Depth=0 heuristic may not see it.",
}

# ─────────────────────────────────────────────────────────────
# Scenario 3 (5x5): Deep Fork
# 5x5 board with a fork threat at depth=4 — unreachable at shallow search.
SCENARIOS['deep_fork'] = {
    'name':        "5x5 Deep Fork (Horizon>=4)",
    'description': (
        "On a 5x5 board X has built a position with a fork "
        "that only becomes visible at depth 4+. "
        "Shallow AI misses it completely."
    ),
    'rows': 5, 'cols': 5, 'win_len': 3,
    'board': [
        ['X',  None, 'X',  None, None],
        [None, 'X',  None, None, None],
        ['O',  None, 'O',  None, None],
        [None, None, None, 'X',  None],
        [None, None, None, None, None],
    ],
    'current_player': 'O',
    'warning': "Fork only visible at depth >= 4! Compare depth 2 vs 4.",
}

# ─────────────────────────────────────────────────────────────
# Scenario 4 (4x4): Transposition Table Demo
# Repeated position reachable via multiple move orders — cache hits visible.
SCENARIOS['transposition_demo'] = {
    'name':        "Transposition Table Demo",
    'description': (
        "Several paths lead to the same board state. "
        "Enable the transposition table (T) and watch cache hits increase."
    ),
    'rows': 4, 'cols': 4, 'win_len': 3,
    'board': [
        [None, None, None, None],
        [None, 'X',  'O',  None],
        [None, 'O',  'X',  None],
        [None, None, None, None],
    ],
    'current_player': 'X',
    'warning': "Enable transposition table to see cache hit savings.",
}


def load_scenario(name, game):
    """Apply a scenario to an existing GameState, resizing if needed."""
    sc = SCENARIOS[name]
    from game import GameState
    new_game = GameState(sc['rows'], sc['cols'], sc['win_len'])
    new_game.set_board(sc['board'], sc['current_player'])
    return new_game, sc
