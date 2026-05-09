"""Pygame visualizer for JSE Trading Duel - Version 4."""
import pygame
import sys
from market import ASSETS, ACTIONS

BG       = (10,  18,  38)
PANELBG  = (16,  28,  58)
WHITE    = (240, 240, 240)
GRAY     = (140, 140, 160)
LTGRAY   = (185, 200, 220)
YELLOW   = (230, 210,  50)
CYAN     = ( 50, 220, 210)
ORANGE   = (230, 140,  50)
GREEN    = ( 50, 200,  80)
TEAL     = (  0, 155, 145)
RED      = (220,  55,  55)
BLUE     = ( 55, 125, 220)
GOLD     = (230, 190,  50)
PURPLE   = (150,  80, 210)
LINE_C   = ( 60, 100, 160)

WINDOW_W, WINDOW_H = 1100, 700
GAME_W   = 490
PANEL_X  = GAME_W + 12
PANEL_W  = WINDOW_W - PANEL_X - 8

# Action button layout
BTN_W, BTN_H = 135, 36
BTN_COLS     = 3
BTN_START_X  = 12
BTN_START_Y  = 490


class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("V4 – JSE Trading Duel")
        self.fnt_xl  = pygame.font.SysFont("monospace", 21, bold=True)
        self.fnt_lg  = pygame.font.SysFont("monospace", 17, bold=True)
        self.fnt_md  = pygame.font.SysFont("monospace", 14)
        self.fnt_sm  = pygame.font.SysFont("monospace", 12)
        self.fnt_xs  = pygame.font.SysFont("monospace", 10)
        self.clock   = pygame.time.Clock()
        self._buttons = []  # list of (rect, action_str)

    def draw(self, game, stats, algorithm, depth_limit, show_heuristic, heur_bd,
             valid_human_actions, selected_action, waiting_human):
        self.screen.fill(BG)
        self._draw_game_area(game, valid_human_actions, selected_action, waiting_human)
        self._draw_panel(game, stats, algorithm, depth_limit, show_heuristic, heur_bd)
        pygame.display.flip()
        self.clock.tick(60)

    def get_button_action(self, x, y):
        for rect, action in self._buttons:
            if rect.collidepoint(x, y):
                return action
        return None

    # ─── game area ────────────────────────────────────────────────────────────

    def _draw_game_area(self, game, valid_human_actions, selected_action, waiting_human):
        # Background card
        pygame.draw.rect(self.screen, PANELBG, (8, 8, GAME_W-16, WINDOW_H-16), border_radius=10)

        py = 14
        lh = 21

        def ln(txt, colour=WHITE, font=None, x=16):
            nonlocal py
            f = font or self.fnt_md
            s = f.render(txt, True, colour)
            self.screen.blit(s, (x, py))
            py += lh

        def sep():
            nonlocal py
            pygame.draw.line(self.screen, LINE_C, (16, py+2), (GAME_W-24, py+2), 1)
            py += 7

        ln("JSE TRADING DUEL", CYAN, self.fnt_xl)
        sep()

        # Turn & event
        ln(f"Turn : {game.turn + 1} / 5", YELLOW, self.fnt_lg)
        evt = game.current_event
        if evt:
            e_col = GREEN if evt['pct'] > 0 else (RED if evt['pct'] < 0 else GRAY)
            ln(f"Event: {evt['desc']}", e_col)
            ln(f"       {evt['name']}  ({'+' if evt['pct']>=0 else ''}{evt['pct']*100:.0f}%)", e_col, self.fnt_sm)
        else:
            ln("Event: (awaiting)", GRAY)
        sep()

        # Asset prices
        ln("── Asset Prices ──", CYAN, self.fnt_sm)
        for asset in ASSETS:
            pr = game.market.prices[asset]
            ln(f"  {asset:<8}: R{pr:>6}", LTGRAY, self.fnt_sm)
        sep()

        # Portfolios side by side
        py_save = py
        ln("── AI Portfolio ──", CYAN, self.fnt_sm)
        ai = game.players[0]
        ln(f"  Cash    : R{ai.cash:>6}", LTGRAY, self.fnt_sm)
        for asset in ASSETS:
            ln(f"  {asset:<6} : {ai.holdings[asset]:>2} unit(s)", LTGRAY, self.fnt_sm)
        ln(f"  VALUE   : R{game.portfolio_value(0):>6}", GREEN, self.fnt_sm)
        ai_py = py

        py = py_save
        col_x = 255
        s = self.fnt_sm.render("── Human Portfolio ──", True, CYAN)
        self.screen.blit(s, (col_x, py)); py += lh
        hu = game.players[1]
        for txt, col in [
            (f"  Cash    : R{hu.cash:>6}", LTGRAY),
            (f"  BANK  : {hu.holdings['BANK']:>2} unit(s)", LTGRAY),
            (f"  MINING: {hu.holdings['MINING']:>2} unit(s)", LTGRAY),
            (f"  RETAIL: {hu.holdings['RETAIL']:>2} unit(s)", LTGRAY),
            (f"  VALUE   : R{game.portfolio_value(1):>6}", BLUE),
        ]:
            s2 = self.fnt_sm.render(txt, True, col)
            self.screen.blit(s2, (col_x, py)); py += lh

        py = max(ai_py, py)
        sep()

        # Last actions
        if game.ai_last_action:
            ln(f"AI did    : {game.ai_last_action}", GREEN, self.fnt_sm)
        if game.human_last_action:
            ln(f"Human did : {game.human_last_action}", BLUE, self.fnt_sm)

        # Game over message
        if game.is_terminal():
            util = game.get_utility()
            if util > 0:
                ln("AI WINS!", GREEN, self.fnt_lg)
            elif util < 0:
                ln("HUMAN WINS!", BLUE, self.fnt_lg)
            else:
                ln("DRAW!", YELLOW, self.fnt_lg)
            ln(f"AI portfolio  : R{game.portfolio_value(0)}", GREEN, self.fnt_sm)
            ln(f"HUM portfolio : R{game.portfolio_value(1)}", BLUE, self.fnt_sm)
        elif waiting_human:
            ln(">> Your turn — pick an action:", YELLOW, self.fnt_md)

        # Action buttons (human turn only)
        self._buttons = []
        if waiting_human and not game.is_terminal():
            self._draw_action_buttons(valid_human_actions, selected_action)

    def _draw_action_buttons(self, valid_actions, selected):
        all_actions = ['BUY_BANK','BUY_MINING','BUY_RETAIL',
                       'SELL_BANK','SELL_MINING','SELL_RETAIL','HOLD']
        gap = 6
        for i, act in enumerate(all_actions):
            col_i = i % BTN_COLS
            row_i = i // BTN_COLS
            bx = BTN_START_X + col_i * (BTN_W + gap)
            by = BTN_START_Y + row_i * (BTN_H + gap)
            rect = pygame.Rect(bx, by, BTN_W, BTN_H)
            enabled = act in valid_actions
            is_sel  = act == selected
            if is_sel:
                bg_col = TEAL
            elif enabled:
                bg_col = (30, 60, 110)
            else:
                bg_col = (25, 30, 50)
            pygame.draw.rect(self.screen, bg_col, rect, border_radius=5)
            border = CYAN if is_sel else (GRAY if enabled else (40, 45, 65))
            pygame.draw.rect(self.screen, border, rect, 1, border_radius=5)
            txt_col = WHITE if enabled else (70, 75, 90)
            lbl = self.fnt_sm.render(act, True, txt_col)
            self.screen.blit(lbl, (bx + BTN_W//2 - lbl.get_width()//2,
                                   by + BTN_H//2 - lbl.get_height()//2))
            if enabled:
                self._buttons.append((rect, act))

    # ─── stats panel ──────────────────────────────────────────────────────────

    def _draw_panel(self, game, stats, algorithm, depth_limit, show_heuristic, heur_bd):
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
            pygame.draw.line(self.screen, LINE_C,(px,py+2),(px+PANEL_W,py+2),1)
            py += 7

        ln("[ TRADING DUEL AI ]", CYAN, self.fnt_xl)
        sep()
        ln(f"Algorithm : {algorithm}", GREEN)
        ln(f"Depth Lim : {depth_limit}", LTGRAY)
        sep()
        ln("── Search Stats ──", CYAN, self.fnt_sm)
        ln(f"  Nodes   : {stats.get('nodes',0)}", LTGRAY, self.fnt_sm)
        ln(f"  Pruned  : {stats.get('pruned',0)}", LTGRAY, self.fnt_sm)
        ln(f"  AI act  : {stats.get('ai_action','N/A')}", LTGRAY, self.fnt_sm)
        ln(f"  Utility : {stats.get('score','N/A')}", LTGRAY, self.fnt_sm)
        sep()
        if show_heuristic and heur_bd:
            ln("── Heuristic ──", CYAN, self.fnt_sm)
            for k, v in heur_bd.items():
                ln(f"  {k:<18}: {v:.1f}", GRAY, self.fnt_xs)
            sep()
        ln("── Controls ──", TEAL, self.fnt_sm)
        for ctrl in [
            "Click btn = human action",
            "A  = AI makes move",
            "M  = Minimax",
            "P  = Alpha-Beta",
            "L  = Depth-Limited",
            "UP/DN = depth limit",
            "H  = Heuristic panel",
            "SPACE = advance turn",
            "R  = Reset game",
        ]:
            ln(ctrl, GRAY, self.fnt_xs)
        sep()
        ln("── Turn Log ──", CYAN, self.fnt_sm)
        ai_hist  = game.players[0].history
        hum_hist = game.players[1].history
        for i in range(min(len(ai_hist), len(hum_hist))):
            ln(f"T{i+1} AI:{ai_hist[i][:10]}  HU:{hum_hist[i][:10]}", GRAY, self.fnt_xs)
