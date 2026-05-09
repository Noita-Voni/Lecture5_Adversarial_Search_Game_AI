"""Heuristic evaluation of non-terminal TicTacToe board states."""

WIN_LINES = [
    [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],
]

class HeuristicEvaluator:
    def __init__(self, ai_player):
        self.ai_player = ai_player
        self.opp = 'O' if ai_player == 'X' else 'X'
        self.last_breakdown = {}

    def evaluate(self, state):
        bd = {}
        lines = self._score_lines(state)
        bd['lines'] = lines
        center = (3 if state.board[1][1] == self.ai_player
                  else -3 if state.board[1][1] == self.opp else 0)
        bd['center'] = center
        ai_c = sum(1 for r,c in [(0,0),(0,2),(2,0),(2,2)] if state.board[r][c] == self.ai_player)
        op_c = sum(1 for r,c in [(0,0),(0,2),(2,0),(2,2)] if state.board[r][c] == self.opp)
        bd['corners'] = ai_c - op_c
        self.last_breakdown = bd
        return sum(bd.values())

    def _score_lines(self, state):
        total = 0
        for line in WIN_LINES:
            vals = [state.board[r][c] for r, c in line]
            ai_n = vals.count(self.ai_player)
            op_n = vals.count(self.opp)
            if op_n == 0:
                if ai_n == 2: total += 10
                elif ai_n == 1: total += 1
            elif ai_n == 0:
                if op_n == 2: total -= 10
                elif op_n == 1: total -= 1
        return total
