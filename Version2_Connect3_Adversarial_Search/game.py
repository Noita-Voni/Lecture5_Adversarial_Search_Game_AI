"""Connect-3 on a 4x4 board - Version 2."""

class GameState:
    ROWS, COLS = 4, 4

    WIN_LINES = []
    # Build all win lines: horizontal, vertical, diagonal (length 3)
    # Horizontal
    for r in range(4):
        for c in range(2):  # 0,1,2 -> cols 0-2, 1-3
            WIN_LINES.append([(r,c),(r,c+1),(r,c+2)])
    # Vertical
    for r in range(2):
        for c in range(4):
            WIN_LINES.append([(r,c),(r+1,c),(r+2,c)])
    # Diagonal ↘
    for r in range(2):
        for c in range(2):
            WIN_LINES.append([(r,c),(r+1,c+1),(r+2,c+2)])
    # Diagonal ↙
    for r in range(2):
        for c in range(2, 4):
            WIN_LINES.append([(r,c),(r+1,c-1),(r+2,c-2)])

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None]*self.COLS for _ in range(self.ROWS)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.move_count = 0
        self.move_history = []
        self.winning_line = None

    def get_valid_moves(self):
        if self.game_over:
            return []
        return [(r, c) for r in range(self.ROWS) for c in range(self.COLS)
                if self.board[r][c] is None]

    def make_move(self, row, col):
        if self.board[row][col] is not None or self.game_over:
            return False
        self.board[row][col] = self.current_player
        self.move_count += 1
        self.move_history.append((row, col, self.current_player))
        self._check_terminal()
        if not self.game_over:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def undo_move(self, row, col):
        player = self.board[row][col]
        self.board[row][col] = None
        self.move_count -= 1
        if self.move_history and self.move_history[-1][:2] == (row, col):
            self.move_history.pop()
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.current_player = player

    def _check_terminal(self):
        for line in self.WIN_LINES:
            vals = [self.board[r][c] for r, c in line]
            if vals[0] is not None and all(v == vals[0] for v in vals):
                self.winner = vals[0]
                self.winning_line = line
                self.game_over = True
                return
        if self.move_count == self.ROWS * self.COLS:
            self.game_over = True

    def is_terminal(self):
        return self.game_over

    def get_utility(self, ai_player):
        if self.winner == ai_player:
            return 1
        elif self.winner is None:
            return 0
        else:
            return -1

    def get_winning_line(self):
        return self.winning_line

    def clone(self):
        s = GameState()
        s.board = [row[:] for row in self.board]
        s.current_player = self.current_player
        s.winner = self.winner
        s.game_over = self.game_over
        s.move_count = self.move_count
        s.move_history = list(self.move_history)
        s.winning_line = self.winning_line
        return s
