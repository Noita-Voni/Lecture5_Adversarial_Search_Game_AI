"""TicTacToe game state and rules - Version 1."""

class GameState:
    WIN_LINES = [
        [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None]*3 for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.move_count = 0
        self.move_history = []

    def get_valid_moves(self):
        if self.game_over:
            return []
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] is None]

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
        self.current_player = player

    def _check_terminal(self):
        for line in self.WIN_LINES:
            vals = [self.board[r][c] for r, c in line]
            if vals[0] is not None and all(v == vals[0] for v in vals):
                self.winner = vals[0]
                self.game_over = True
                return
        if self.move_count == 9:
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
        for line in self.WIN_LINES:
            vals = [self.board[r][c] for r, c in line]
            if vals[0] is not None and all(v == vals[0] for v in vals):
                return line
        return None

    def clone(self):
        s = GameState()
        s.board = [row[:] for row in self.board]
        s.current_player = self.current_player
        s.winner = self.winner
        s.game_over = self.game_over
        s.move_count = self.move_count
        s.move_history = list(self.move_history)
        return s
