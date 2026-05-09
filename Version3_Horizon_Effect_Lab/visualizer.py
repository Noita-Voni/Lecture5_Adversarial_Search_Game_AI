"""Pygame visualizer for Horizon Effect Lab - Version 3."""
import pygame
import sys

BG       = (10,  20,  45)
PANELBG  = (18,  32,  65)
GRID_C   = (60, 100, 160)
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
RED      = (220,  50,  50)
WARN_COL = (255, 160,   0)

WINDOW_W, WINDOW_H = 1100, 720
BOARD_AREA_W = 430
PANEL_X      = BOARD_AREA_W + 12
PANEL_W      = WINDOW_W - PANEL_X - 8
MARGIN       = 45


class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("V3 – Horizon Effect Lab")
        self.fnt_xl = pygame.font.SysFont("monospace", 21, bold=True)
        self.fnt_lg = pygame.font.SysFont("monospace", 17, bold=True)
        self.fnt_md = pygame.font.SysFont("monospace", 14)
        self.fnt_sm = pygame.font.SysFont("monospace", 12)
        self.fnt_xs = pygame.font.SysFont("monospace", 11)
        self.clock  = pygame.time.Clock()

    def draw(self, game, stats, scenario_info, depth_limit, show_heuristic,
             heuristic_breakdown, use_pruning, use_ordering, use_tt, warning_active):
        self.screen.fill(BG)
        self._draw_board(game)
        self._draw_panel(game, stats, scenario_info, depth_limit, show_heuristic,
                         heuristic_breakdown, use_pruning, use_ordering, use_tt,
                         warning_active)
        pygame.display.flip()
        self.clock.tick(60)

    def get_cell_at(self, x, y, game):
        cell_size = (BOARD_AREA_W - 2*MARGIN) // max(game.ROWS, game.COLS)
        bx, by = MARGIN, MARGIN
        board_w = game.COLS * cell_size
        board_h = game.ROWS * cell_size
        if bx <= x < bx + board_w and by <= y < by + board_h:
            return int((y - by) // cell_size), int((x - bx) // cell_size)
        return None

    def _draw_board(self, game):
        cell = (BOARD_AREA_W - 2*MARGIN) // max(game.ROWS, game.COLS)
        bx, by = MARGIN, MARGIN
        bw, bh = game.COLS * cell, game.ROWS * cell
        pygame.draw.rect(self.screen, PANELBG, (bx-8, by-8, bw+16, bh+16), border_radius=10)
        wline = game.get_winning_line()
        for r in range(game.ROWS):
            for c in range(game.COLS):
                cx = bx + c*cell + cell//2
                cy = by + r*cell + cell//2
                if wline and (r, c) in wline:
                    pygame.draw.rect(self.screen, WIN_HL,
                                     pygame.Rect(bx+c*cell+2, by+r*cell+2, cell-4, cell-4),
                                     border_radius=5)
                piece = game.board[r][c]
                if piece == 'X':
                    off = cell//3
                    pygame.draw.line(self.screen, X_COL, (cx-off,cy-off),(cx+off,cy+off),4)
                    pygame.draw.line(self.screen, X_COL, (cx+off,cy-off),(cx-off,cy+off),4)
                elif piece == 'O':
                    pygame.draw.circle(self.screen, O_COL, (cx, cy), cell//3, 4)
        for i in range(game.COLS+1):
            pygame.draw.line(self.screen, GRID_C,(bx+i*cell,by),(bx+i*cell,by+bh),2)
        for i in range(game.ROWS+1):
            pygame.draw.line(self.screen, GRID_C,(bx,by+i*cell),(bx+bw,by+i*cell),2)
        lbl = self.fnt_sm.render(f"{game.ROWS}x{game.COLS} Connect-{game.WIN_LEN}", True, LTGRAY)
        self.screen.blit(lbl, (bx + bw//2 - lbl.get_width()//2, by+bh+8))

    def _draw_panel(self, game, stats, scenario_info, depth_limit, show_heuristic,
                    heuristic_breakdown, use_pruning, use_ordering, use_tt, warning_active):
        px, py = PANEL_X, 8
        lh = 20

        def ln(txt, colour=WHITE, font=None, indent=0):
            nonlocal py
            f = font or self.fnt_md
            s = f.render(txt, True, colour)
            self.screen.blit(s, (px+indent, py))
            py += lh

        def sep():
            nonlocal py
            pygame.draw.line(self.screen, GRID_C,(px,py+2),(px+PANEL_W,py+2),1)
            py += 7

        ln("[ HORIZON EFFECT LAB ]", CYAN, self.fnt_xl)
        sep()

        sc_name = scenario_info.get('name','Free Play') if scenario_info else "Free Play"
        ln(f"Scenario  : {sc_name}", YELLOW)
        ln(f"Depth Lim : {depth_limit}", LTGRAY)
        ln(f"Pruning   : {'ON' if use_pruning else 'OFF'}", GREEN if use_pruning else ORANGE)
        ln(f"Move Order: {'ON' if use_ordering else 'OFF'}", GREEN if use_ordering else GRAY)
        ln(f"Trans.Tbl : {'ON' if use_tt else 'OFF'}", GREEN if use_tt else GRAY)
        sep()

        if game.game_over:
            if game.winner:
                ln(f"Winner : {game.winner}!", YELLOW, self.fnt_lg)
            else:
                ln("Result : Draw", ORANGE, self.fnt_lg)
        else:
            col = X_COL if game.current_player=='X' else O_COL
            ln(f"Turn   : {game.current_player}", col, self.fnt_lg)
        sep()

        ln("-- Search Stats --", CYAN, self.fnt_sm)
        ln(f"  Nodes searched  : {stats.get('nodes',0)}", LTGRAY, self.fnt_sm)
        ln(f"  Branches pruned : {stats.get('pruned',0)}", LTGRAY, self.fnt_sm)
        ln(f"  Cache hits      : {stats.get('cache_hits',0)}", LTGRAY, self.fnt_sm)
        ln(f"  AI move         : {stats.get('best_move','N/A')}", LTGRAY, self.fnt_sm)
        ln(f"  Score           : {stats.get('best_score','N/A')}", LTGRAY, self.fnt_sm)
        sep()

        if show_heuristic and heuristic_breakdown:
            ln("-- Heuristic --", CYAN, self.fnt_sm)
            for k, v in heuristic_breakdown.items():
                ln(f"  {k:<10}: {v}", GRAY, self.fnt_xs)
            sep()

        if warning_active and scenario_info and scenario_info.get('warning'):
            ln("! HORIZON EFFECT:", WARN_COL, self.fnt_sm)
            # word-wrap warning text
            warn = scenario_info['warning']
            words = warn.split()
            line_buf = []
            for w in words:
                line_buf.append(w)
                if len(' '.join(line_buf)) > 38:
                    ln('  '+' '.join(line_buf[:-1]), WARN_COL, self.fnt_xs)
                    line_buf = [w]
            if line_buf:
                ln('  '+' '.join(line_buf), WARN_COL, self.fnt_xs)
            sep()

        ln("-- Controls --", TEAL, self.fnt_sm)
        for ctrl in [
            "E=Load Horizon Scenario",
            "1-4=Select Scenario",
            "UP/DN=Depth  H=Heuristic",
            "P=Toggle Pruning",
            "O=Move Order  T=Trans.Tbl",
            "R=Reset  SPACE=AI move",
            "Click=Manual move",
        ]:
            ln(ctrl, GRAY, self.fnt_xs)
