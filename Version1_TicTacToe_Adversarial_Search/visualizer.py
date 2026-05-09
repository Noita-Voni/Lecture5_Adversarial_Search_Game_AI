"""Pygame visualizer for TicTacToe Adversarial Search - Version 1."""
import pygame
import sys

# -- Colour palette -----------------------------------------------------------
BG          = (15,  25,  50)
PANEL_BG    = (20,  35,  70)
GRID_COL    = (80, 120, 180)
X_COL       = (220,  60,  60)
O_COL       = (60, 130, 220)
WIN_HL      = (50, 200,  80)
WHITE       = (240, 240, 240)
GRAY        = (140, 140, 160)
LTGRAY      = (190, 200, 220)
YELLOW      = (230, 210,  50)
CYAN        = ( 50, 220, 210)
ORANGE      = (230, 140,  50)
GREEN       = ( 50, 200,  80)
TEAL        = (  0, 160, 150)
MAX_COL     = ( 50, 200,  80)   # MAX node colour in tree
MIN_COL     = (200,  60,  60)   # MIN node colour in tree
PRUNE_COL   = ( 80,  80,  80)

WINDOW_W, WINDOW_H = 900, 620
BOARD_W            = 380
PANEL_X            = BOARD_W + 10
PANEL_W            = WINDOW_W - PANEL_X - 8
BOARD_MARGIN       = 55
CELL               = (BOARD_W - 2 * BOARD_MARGIN) // 3   # ~90


class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("V1 - TicTacToe Adversarial Search")
        self.fnt_xl  = pygame.font.SysFont("monospace", 22, bold=True)
        self.fnt_lg  = pygame.font.SysFont("monospace", 18, bold=True)
        self.fnt_md  = pygame.font.SysFont("monospace", 15)
        self.fnt_sm  = pygame.font.SysFont("monospace", 13)
        self.fnt_xs  = pygame.font.SysFont("monospace", 11)
        self.clock   = pygame.time.Clock()
        self.show_tree = False
        self.tree_root = None

    # -- public ---------------------------------------------------------------

    def draw(self, game, stats, mode, algorithm, depth_limit,
             show_heuristic, heuristic_breakdown=None):
        self.screen.fill(BG)
        self._draw_board(game)
        self._draw_panel(game, stats, mode, algorithm, depth_limit,
                         show_heuristic, heuristic_breakdown)
        if self.show_tree and self.tree_root:
            self._draw_tree_panel(self.tree_root)
        pygame.display.flip()
        self.clock.tick(60)

    def get_cell_at(self, x, y):
        """Return (row, col) if (x,y) is inside the board grid, else None."""
        bx = BOARD_MARGIN
        by = BOARD_MARGIN
        if bx <= x < bx + 3 * CELL and by <= y < by + 3 * CELL:
            return int((y - by) // CELL), int((x - bx) // CELL)
        return None

    def set_tree_root(self, root):
        self.tree_root = root

    def handle_quit(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

    # -- board ----------------------------------------------------------------

    def _draw_board(self, game):
        bx, by = BOARD_MARGIN, BOARD_MARGIN
        sz = 3 * CELL
        pygame.draw.rect(self.screen, PANEL_BG, (bx-8, by-8, sz+16, sz+16), border_radius=10)

        wline = game.get_winning_line()

        for r in range(3):
            for c in range(3):
                cx = bx + c * CELL + CELL // 2
                cy = by + r * CELL + CELL // 2
                cell_rect = pygame.Rect(bx + c*CELL + 2, by + r*CELL + 2, CELL-4, CELL-4)
                if wline and (r, c) in wline:
                    pygame.draw.rect(self.screen, WIN_HL, cell_rect, border_radius=6)
                piece = game.board[r][c]
                if piece == 'X':
                    off = CELL // 3
                    pygame.draw.line(self.screen, X_COL, (cx-off, cy-off), (cx+off, cy+off), 5)
                    pygame.draw.line(self.screen, X_COL, (cx+off, cy-off), (cx-off, cy+off), 5)
                elif piece == 'O':
                    pygame.draw.circle(self.screen, O_COL, (cx, cy), CELL//3, 5)

        # Grid lines
        for i in range(4):
            pygame.draw.line(self.screen, GRID_COL, (bx+i*CELL, by), (bx+i*CELL, by+sz), 2)
            pygame.draw.line(self.screen, GRID_COL, (bx, by+i*CELL), (bx+sz, by+i*CELL), 2)

        # Title below board
        t = self.fnt_lg.render("TicTacToe  3x3", True, LTGRAY)
        self.screen.blit(t, (bx + sz//2 - t.get_width()//2, by + sz + 12))

    # -- panel ----------------------------------------------------------------

    def _draw_panel(self, game, stats, mode, algorithm, depth_limit,
                    show_heuristic, heuristic_breakdown):
        px, py = PANEL_X, 8
        lh = 21  # line height

        def ln(txt, colour=WHITE, font=None, indent=0):
            nonlocal py
            f = font or self.fnt_md
            s = f.render(txt, True, colour)
            self.screen.blit(s, (px + indent, py))
            py += lh

        def sep():
            nonlocal py
            pygame.draw.line(self.screen, GRID_COL, (px, py+2), (px+PANEL_W, py+2), 1)
            py += 8

        ln("[ ADVERSARIAL SEARCH ]", CYAN, self.fnt_xl)
        sep()

        mode_lbl = {0: "Human vs AI", 1: "AI vs AI", 2: "Human vs Human"}.get(mode, "?")
        ln(f"Mode      : {mode_lbl}", YELLOW)
        ln(f"Algorithm : {algorithm}", GREEN)
        ln(f"Depth Lim : {depth_limit}", LTGRAY)
        sep()

        if game.game_over:
            if game.winner:
                ln(f"Winner  :  {game.winner} !", YELLOW, self.fnt_lg)
            else:
                ln("Result  :  Draw", ORANGE, self.fnt_lg)
        else:
            col = X_COL if game.current_player == 'X' else O_COL
            ln(f"Turn    :  {game.current_player}", col, self.fnt_lg)
        sep()

        ln("-- Search Stats --", CYAN, self.fnt_sm)
        ln(f"  Nodes searched : {stats.get('nodes', 0)}", LTGRAY, self.fnt_sm)
        ln(f"  Branches pruned: {stats.get('pruned', 0)}", LTGRAY, self.fnt_sm)
        ln(f"  Best move      : {stats.get('best_move', 'N/A')}", LTGRAY, self.fnt_sm)
        ln(f"  Best score     : {stats.get('best_score', 'N/A')}", LTGRAY, self.fnt_sm)
        sep()

        if show_heuristic and heuristic_breakdown:
            ln("-- Heuristic --", CYAN, self.fnt_sm)
            for k, v in heuristic_breakdown.items():
                ln(f"  {k:<10}: {v}", GRAY, self.fnt_xs)
            sep()

        ln("-- Controls --", TEAL, self.fnt_sm)
        for ctrl in [
            "M=Minimax  A=Alpha-Beta",
            "D=Depth-Limited",
            "O=MoveOrder  H=Heuristic",
            "UP/DN=Depth  T=Tree",
            "R=Reset  SPACE=AI move",
            "C=AI vs AI  V=Hum vs AI",
            "B=Hum vs Hum  Click=Move",
        ]:
            ln(ctrl, GRAY, self.fnt_xs)

    # -- tree preview ---------------------------------------------------------

    def _draw_tree_panel(self, root):
        tx, ty, tw, th = 8, 360, BOARD_W - 16, WINDOW_H - 368
        pygame.draw.rect(self.screen, (18, 28, 55), (tx, ty, tw, th), border_radius=6)
        pygame.draw.rect(self.screen, TEAL, (tx, ty, tw, th), 1, border_radius=6)
        lbl = self.fnt_sm.render("Game Tree Preview (a-b)  MAX=green  MIN=red  pruned=gray", True, CYAN)
        self.screen.blit(lbl, (tx + tw//2 - lbl.get_width()//2, ty + 3))
        self._draw_node(root, tx + tw//2, ty + 30, tw // 2, 0, th + ty)

    def _draw_node(self, node, x, y, spread, depth, y_limit):
        if node is None or depth > 2 or y > y_limit:
            return
        col = PRUNE_COL if node.pruned else (MAX_COL if node.is_max else MIN_COL)
        r = 11
        pygame.draw.circle(self.screen, col, (x, y), r)
        pygame.draw.circle(self.screen, WHITE, (x, y), r, 1)
        if node.score is not None:
            lbl = self.fnt_xs.render(str(node.score), True, WHITE)
            self.screen.blit(lbl, (x - lbl.get_width()//2, y - 7))
        tag = self.fnt_xs.render("MAX" if node.is_max else "MIN", True, YELLOW)
        self.screen.blit(tag, (x - tag.get_width()//2, y + r + 1))

        if depth < 2 and node.children:
            child_y = y + 55
            n = len(node.children)
            show = node.children[:5]
            for i, child in enumerate(show):
                if n == 1:
                    cx = x
                else:
                    cx = x - spread//2 + i * spread // (n - 1)
                lc = PRUNE_COL if child.pruned else GRAY
                pygame.draw.line(self.screen, lc, (x, y+r), (cx, child_y-r), 1)
                if child.pruned:
                    mx, my = (x + cx)//2, (y + child_y)//2
                    pygame.draw.line(self.screen, (200,50,50),(mx-5,my-5),(mx+5,my+5),2)
                    pygame.draw.line(self.screen, (200,50,50),(mx+5,my-5),(mx-5,my+5),2)
                self._draw_node(child, cx, child_y, spread//2, depth+1, y_limit)
