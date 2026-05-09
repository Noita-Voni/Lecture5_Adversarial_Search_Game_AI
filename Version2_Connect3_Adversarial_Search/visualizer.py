"""Pygame visualizer for Connect-3 Adversarial Search - Version 2."""
import pygame
import sys

# -- palette ------------------------------------------------------------------
BG       = (15,  25,  50)
PANELBG  = (20,  35,  70)
GRID_C   = (70, 110, 170)
X_COL    = (220,  60,  60)
O_COL    = ( 60, 130, 220)
WIN_HL   = ( 50, 200,  80)
WHITE    = (240, 240, 240)
GRAY     = (140, 140, 160)
LTGRAY   = (190, 200, 220)
YELLOW   = (230, 210,  50)
CYAN     = ( 50, 220, 210)
ORANGE   = (230, 140,  50)
GREEN    = ( 50, 200,  80)
TEAL     = (  0, 160, 150)
MAX_COL  = ( 50, 200,  80)
MIN_COL  = (200,  60,  60)
PRUNE_C  = ( 80,  80,  80)

WINDOW_W, WINDOW_H = 1000, 680
BOARD_W   = 400
PANEL_X   = BOARD_W + 12
PANEL_W   = WINDOW_W - PANEL_X - 8
MARGIN    = 50
CELL      = (BOARD_W - 2 * MARGIN) // 4   # ~75


class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("V2 - Connect-3  4x4 Adversarial Search")
        self.fnt_xl = pygame.font.SysFont("monospace", 22, bold=True)
        self.fnt_lg = pygame.font.SysFont("monospace", 18, bold=True)
        self.fnt_md = pygame.font.SysFont("monospace", 15)
        self.fnt_sm = pygame.font.SysFont("monospace", 13)
        self.fnt_xs = pygame.font.SysFont("monospace", 11)
        self.clock  = pygame.time.Clock()
        self.show_tree = False
        self.tree_root = None

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
        bx, by = MARGIN, MARGIN
        if bx <= x < bx + 4*CELL and by <= y < by + 4*CELL:
            return int((y - by) // CELL), int((x - bx) // CELL)
        return None

    def set_tree_root(self, root):
        self.tree_root = root

    def handle_quit(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

    def _draw_board(self, game):
        bx, by = MARGIN, MARGIN
        sz = 4 * CELL
        pygame.draw.rect(self.screen, PANELBG, (bx-8, by-8, sz+16, sz+16), border_radius=10)
        wline = game.get_winning_line()
        for r in range(4):
            for c in range(4):
                cx = bx + c*CELL + CELL//2
                cy = by + r*CELL + CELL//2
                if wline and (r, c) in wline:
                    pygame.draw.rect(self.screen, WIN_HL,
                                     pygame.Rect(bx+c*CELL+2, by+r*CELL+2, CELL-4, CELL-4),
                                     border_radius=6)
                piece = game.board[r][c]
                if piece == 'X':
                    off = CELL//3
                    pygame.draw.line(self.screen, X_COL, (cx-off, cy-off), (cx+off, cy+off), 5)
                    pygame.draw.line(self.screen, X_COL, (cx+off, cy-off), (cx-off, cy+off), 5)
                elif piece == 'O':
                    pygame.draw.circle(self.screen, O_COL, (cx, cy), CELL//3, 5)
        for i in range(5):
            pygame.draw.line(self.screen, GRID_C, (bx+i*CELL, by), (bx+i*CELL, by+sz), 2)
            pygame.draw.line(self.screen, GRID_C, (bx, by+i*CELL), (bx+sz, by+i*CELL), 2)
        t = self.fnt_lg.render("Connect-3  4x4", True, LTGRAY)
        self.screen.blit(t, (bx + sz//2 - t.get_width()//2, by + sz + 12))

    def _draw_panel(self, game, stats, mode, algorithm, depth_limit,
                    show_heuristic, heuristic_breakdown):
        px, py = PANEL_X, 8
        lh = 21

        def ln(txt, colour=WHITE, font=None, indent=0):
            nonlocal py
            f = font or self.fnt_md
            s = f.render(txt, True, colour)
            self.screen.blit(s, (px+indent, py))
            py += lh

        def sep():
            nonlocal py
            pygame.draw.line(self.screen, GRID_C, (px, py+2), (px+PANEL_W, py+2), 1)
            py += 8

        ln("[ CONNECT-3  4x4 ]", CYAN, self.fnt_xl)
        sep()
        mode_lbl = {0:"Human vs AI", 1:"AI vs AI", 2:"Human vs Human"}.get(mode,"?")
        ln(f"Mode      : {mode_lbl}", YELLOW)
        ln(f"Algorithm : {algorithm}", GREEN)
        ln(f"Depth Lim : {depth_limit}", LTGRAY)
        ln(f"Move Order: {'ON' if stats.get('ordering') else 'OFF'}", LTGRAY)
        sep()
        if game.game_over:
            if game.winner:
                ln(f"Winner : {game.winner} !", YELLOW, self.fnt_lg)
            else:
                ln("Result : Draw", ORANGE, self.fnt_lg)
        else:
            col = X_COL if game.current_player=='X' else O_COL
            ln(f"Turn   : {game.current_player}", col, self.fnt_lg)
        sep()
        ln("-- Search Stats --", CYAN, self.fnt_sm)
        ln(f"  Nodes searched : {stats.get('nodes',0)}", LTGRAY, self.fnt_sm)
        ln(f"  Branches pruned: {stats.get('pruned',0)}", LTGRAY, self.fnt_sm)
        ln(f"  Best move      : {stats.get('best_move','N/A')}", LTGRAY, self.fnt_sm)
        ln(f"  Best score     : {stats.get('best_score','N/A')}", LTGRAY, self.fnt_sm)
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

    def _draw_tree_panel(self, root):
        tx, ty = 8, 420
        tw, th = BOARD_W - 16, WINDOW_H - 428
        pygame.draw.rect(self.screen, (18,28,55), (tx, ty, tw, th), border_radius=6)
        pygame.draw.rect(self.screen, TEAL, (tx, ty, tw, th), 1, border_radius=6)
        lbl = self.fnt_sm.render("Game Tree  MAX=green  MIN=red  pruned=gray", True, CYAN)
        self.screen.blit(lbl, (tx + tw//2 - lbl.get_width()//2, ty+3))
        self._draw_node(root, tx+tw//2, ty+30, tw//2, 0, ty+th)

    def _draw_node(self, node, x, y, spread, depth, y_limit):
        if node is None or depth > 2 or y > y_limit:
            return
        col = PRUNE_C if node.pruned else (MAX_COL if node.is_max else MIN_COL)
        r = 10
        pygame.draw.circle(self.screen, col, (x, y), r)
        pygame.draw.circle(self.screen, WHITE, (x, y), r, 1)
        if node.score is not None:
            lbl = self.fnt_xs.render(str(node.score), True, WHITE)
            self.screen.blit(lbl, (x - lbl.get_width()//2, y-7))
        tag = self.fnt_xs.render("M" if node.is_max else "m", True, YELLOW)
        self.screen.blit(tag, (x - tag.get_width()//2, y+r+1))
        if depth < 2 and node.children:
            cy2 = y + 50
            n = len(node.children)
            show = node.children[:6]
            for i, child in enumerate(show):
                cx = x - spread//2 + i*spread//max(n-1,1) if n > 1 else x
                lc = PRUNE_C if child.pruned else GRAY
                pygame.draw.line(self.screen, lc, (x, y+r), (cx, cy2-r), 1)
                if child.pruned:
                    mx2, my2 = (x+cx)//2, (y+cy2)//2
                    pygame.draw.line(self.screen,(200,50,50),(mx2-5,my2-5),(mx2+5,my2+5),2)
                    pygame.draw.line(self.screen,(200,50,50),(mx2+5,my2-5),(mx2-5,my2+5),2)
                self._draw_node(child, cx, cy2, spread//2, depth+1, y_limit)
