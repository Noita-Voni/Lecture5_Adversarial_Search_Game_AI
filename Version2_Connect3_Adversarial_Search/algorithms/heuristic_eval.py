"""Heuristic evaluation of non-terminal Connect-3 4x4 states."""

class HeuristicEvaluator:
    WIN_LINES = []
    for _r in range(4):
        for _c in range(2):
            WIN_LINES.append([(_r,_c),(_r,_c+1),(_r,_c+2)])
    for _r in range(2):
        for _c in range(4):
            WIN_LINES.append([(_r,_c),(_r+1,_c),(_r+2,_c)])
    for _r in range(2):
        for _c in range(2):
            WIN_LINES.append([(_r,_c),(_r+1,_c+1),(_r+2,_c+2)])
    for _r in range(2):
        for _c in range(2, 4):
            WIN_LINES.append([(_r,_c),(_r+1,_c-1),(_r+2,_c-2)])

    def __init__(self, ai_player):
        self.ai = ai_player
        self.opp = 'O' if ai_player == 'X' else 'X'
        self.last_breakdown = {}

    def evaluate(self, state):
        bd = {}
        lines = self._score_lines(state)
        bd['lines'] = lines
        # Center control (cells (1,1),(1,2),(2,1),(2,2))
        center_cells = [(1,1),(1,2),(2,1),(2,2)]
        ai_c = sum(1 for r,c in center_cells if state.board[r][c] == self.ai)
        op_c = sum(1 for r,c in center_cells if state.board[r][c] == self.opp)
        bd['center'] = (ai_c - op_c) * 2
        self.last_breakdown = bd
        return sum(bd.values())

    def _score_lines(self, state):
        total = 0
        for line in self.WIN_LINES:
            vals = [state.board[r][c] for r, c in line]
            ai_n = vals.count(self.ai)
            op_n = vals.count(self.opp)
            if op_n == 0:
                if ai_n == 2: total += 10
                elif ai_n == 1: total += 1
            elif ai_n == 0:
                if op_n == 2: total -= 10
                elif op_n == 1: total -= 1
        return total
