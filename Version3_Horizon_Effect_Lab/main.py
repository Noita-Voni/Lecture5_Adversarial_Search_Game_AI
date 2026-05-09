"""
Version 3 – Horizon Effect Lab
Run: python main.py
Controls
--------
E          Load current scenario (cycle with 1-4)
1          Scenario: Horizon Classic Fork
2          Scenario: Delayed Winning Threat
3          Scenario: 5x5 Deep Fork
4          Scenario: Transposition Demo
UP/DOWN    Change depth limit
H          Toggle heuristic breakdown
P          Toggle alpha-beta pruning on/off
O          Toggle move ordering
T          Toggle transposition table
R          Reset (free play on default board)
SPACE      AI makes one move
Click      Manual piece placement
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from game import GameState
from scenarios import SCENARIOS, load_scenario
from visualizer import Visualizer
from algorithms.depth_limited_minimax import depth_limited_minimax
from algorithms.heuristic_eval import HeuristicEvaluator
from algorithms.transposition_table import TranspositionTable

AI_PLAYER = 'X'

SCENARIO_KEYS = ['horizon_classic', 'delayed_threat', 'deep_fork', 'transposition_demo']


def make_evaluator(game):
    return HeuristicEvaluator(AI_PLAYER, game.WIN_LINES)


def get_ai_move(game, depth_limit, evaluator, use_pruning, use_ordering, tt_instance):
    orderer = None
    if use_ordering:
        from algorithms.depth_limited_minimax import depth_limited_minimax
        class SimpleOrderer:
            def order_moves(self, state, moves, is_max):
                rows, cols = state.ROWS, state.COLS
                cr, cc = (rows-1)/2.0, (cols-1)/2.0
                return sorted(moves, key=lambda m: abs(m[0]-cr)+abs(m[1]-cc))
        orderer = SimpleOrderer()

    mv, sc, nd, pr, hits = depth_limited_minimax(
        game, game.current_player, depth_limit, evaluator,
        use_move_ordering=use_ordering, move_orderer=orderer,
        use_pruning=use_pruning,
        transposition_table=tt_instance if tt_instance else None
    )
    return mv, {'nodes': nd, 'pruned': pr, 'cache_hits': hits,
                'best_move': mv, 'best_score': sc}


def main():
    game         = GameState(4, 4, 3)
    vis          = Visualizer()
    evaluator    = make_evaluator(game)
    tt           = TranspositionTable()

    depth_limit    = 3
    use_pruning    = True
    use_ordering   = True
    use_tt         = False
    show_heuristic = False
    current_sc_idx = 0
    scenario_info  = None
    warning_active = False

    stats   = {'nodes':0,'pruned':0,'cache_hits':0,'best_move':None,'best_score':0}
    heur_bd = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                k = event.key

                if k == pygame.K_r:
                    game = GameState(4, 4, 3)
                    evaluator = make_evaluator(game)
                    tt.clear()
                    stats = {'nodes':0,'pruned':0,'cache_hits':0,'best_move':None,'best_score':0}
                    heur_bd = None; scenario_info = None; warning_active = False

                elif k in (pygame.K_e,):
                    sc_key = SCENARIO_KEYS[current_sc_idx]
                    game, scenario_info = load_scenario(sc_key, game)
                    evaluator = make_evaluator(game)
                    tt.clear()
                    warning_active = True
                    stats = {'nodes':0,'pruned':0,'cache_hits':0,'best_move':None,'best_score':0}

                elif k == pygame.K_1:
                    current_sc_idx = 0
                    sc_key = SCENARIO_KEYS[0]
                    game, scenario_info = load_scenario(sc_key, game)
                    evaluator = make_evaluator(game); tt.clear(); warning_active = True
                elif k == pygame.K_2:
                    current_sc_idx = 1
                    sc_key = SCENARIO_KEYS[1]
                    game, scenario_info = load_scenario(sc_key, game)
                    evaluator = make_evaluator(game); tt.clear(); warning_active = True
                elif k == pygame.K_3:
                    current_sc_idx = 2
                    sc_key = SCENARIO_KEYS[2]
                    game, scenario_info = load_scenario(sc_key, game)
                    evaluator = make_evaluator(game); tt.clear(); warning_active = True
                elif k == pygame.K_4:
                    current_sc_idx = 3
                    sc_key = SCENARIO_KEYS[3]
                    game, scenario_info = load_scenario(sc_key, game)
                    evaluator = make_evaluator(game); tt.clear(); warning_active = True

                elif k == pygame.K_UP:   depth_limit = min(8, depth_limit+1)
                elif k == pygame.K_DOWN: depth_limit = max(1, depth_limit-1)
                elif k == pygame.K_h:    show_heuristic = not show_heuristic
                elif k == pygame.K_p:    use_pruning  = not use_pruning
                elif k == pygame.K_o:    use_ordering = not use_ordering
                elif k == pygame.K_t:
                    use_tt = not use_tt
                    if use_tt: tt.clear()

                elif k == pygame.K_SPACE:
                    if not game.game_over:
                        tt_arg = tt if use_tt else None
                        mv, stats = get_ai_move(game, depth_limit, evaluator,
                                                use_pruning, use_ordering, tt_arg)
                        if mv: game.make_move(*mv)
                        if show_heuristic:
                            evaluator.evaluate(game)
                            heur_bd = dict(evaluator.last_breakdown)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game.game_over:
                    cell = vis.get_cell_at(*event.pos, game)
                    if cell:
                        game.make_move(*cell)

        vis.draw(game, stats, scenario_info, depth_limit, show_heuristic,
                 heur_bd, use_pruning, use_ordering, use_tt, warning_active)

    pygame.quit(); sys.exit()


if __name__ == "__main__":
    main()
