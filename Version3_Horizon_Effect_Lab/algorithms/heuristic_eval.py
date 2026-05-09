"""Heuristic evaluation for configurable Connect-N boards."""

class HeuristicEvaluator:
    def __init__(self, ai_player, win_lines):
        self.ai  = ai_player
        self.opp = 'O' if ai_player == 'X' else 'X'
        self.win_lines = win_lines
        self.last_breakdown = {}

    def evaluate(self, state):
        bd = {}
        bd['lines']  = self._score_lines(state)
        # Centre bonus — weight cells near the board centre
        rows, cols = state.ROWS, state.COLS
        cr, cc = (rows-1)/2, (cols-1)/2
        centre_score = 0
        for r in range(rows):
            for c in range(cols):
                p = state.board[r][c]
                if p is None: continue
                dist = abs(r - cr) + abs(c - cc)
                weight = max(0, 3 - int(dist))
                centre_score += weight if p == self.ai else -weight
        bd['centre'] = centre_score
        self.last_breakdown = bd
        return sum(bd.values())

    def _score_lines(self, state):
        total = 0
        win_len = state.WIN_LEN
        for line in self.win_lines:
            vals = [state.board[r][c] for r, c in line]
            ai_n = vals.count(self.ai)
            op_n = vals.count(self.opp)
            if op_n == 0:
                if ai_n == win_len - 1: total += 10
                elif ai_n > 0:          total += ai_n
            elif ai_n == 0:
                if op_n == win_len - 1: total -= 10
                elif op_n > 0:          total -= op_n
        return total
