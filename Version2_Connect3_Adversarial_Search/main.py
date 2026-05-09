"""
Version 2 - Connect-3 4x4 Adversarial Search
Run: python main.py
Controls
--------
M          Minimax
A          Alpha-Beta
D          Depth-Limited
O          Toggle move ordering
H          Toggle heuristic breakdown
UP / DOWN  Depth limit
T          Toggle game tree preview
R          Reset
C          AI vs AI
V          Human vs AI
B          Human vs Human
SPACE      One AI move
Click      Human move
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from game import GameState
from visualizer import Visualizer
from algorithms.minimax import minimax
from algorithms.alpha_beta import alpha_beta
from algorithms.depth_limited_search import depth_limited_minimax
from algorithms.move_ordering import MoveOrderer
from algorithms.heuristic_eval import HeuristicEvaluator
from algorithms.game_tree import GameTreeBuilder

MODE_HUMAN_AI  = 0
MODE_AI_AI     = 1
MODE_HUMAN_HUM = 2
ALG_MINIMAX   = "Minimax"
ALG_AB        = "Alpha-Beta"
ALG_DEPTH     = "Depth-Limited"
AI_PLAYER     = 'X'
HUMAN_PLAYER  = 'O'


def get_ai_move(game, algorithm, depth_limit, use_ordering, evaluator, orderer):
    stats = {'nodes':0,'pruned':0,'best_move':None,'best_score':0,'ordering':use_ordering}
    ai_p = game.current_player
    if algorithm == ALG_MINIMAX:
        mv, sc, nd = minimax(game, ai_p)
        stats.update(nodes=nd, best_move=mv, best_score=sc)
    elif algorithm == ALG_AB:
        mv, sc, nd, pr = alpha_beta(game, ai_p, use_ordering, orderer)
        stats.update(nodes=nd, pruned=pr, best_move=mv, best_score=sc)
    else:
        mv, sc, nd, pr = depth_limited_minimax(game, ai_p, depth_limit, evaluator,
                                                use_ordering, orderer)
        stats.update(nodes=nd, pruned=pr, best_move=mv, best_score=sc)
    return mv, stats


def main():
    game      = GameState()
    vis       = Visualizer()
    orderer   = MoveOrderer()
    evaluator = HeuristicEvaluator(AI_PLAYER)
    tree_bldr = GameTreeBuilder(max_depth=2)

    mode           = MODE_HUMAN_AI
    algorithm      = ALG_AB
    depth_limit    = 5
    use_ordering   = True
    show_heuristic = False

    stats  = {'nodes':0,'pruned':0,'best_move':None,'best_score':0,'ordering':True}
    heur_bd = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_r:
                    game.reset()
                    stats = {'nodes':0,'pruned':0,'best_move':None,'best_score':0,'ordering':use_ordering}
                    heur_bd = None; vis.tree_root = None
                elif k == pygame.K_m: algorithm = ALG_MINIMAX
                elif k == pygame.K_a: algorithm = ALG_AB
                elif k == pygame.K_d: algorithm = ALG_DEPTH
                elif k == pygame.K_o: use_ordering = not use_ordering
                elif k == pygame.K_h: show_heuristic = not show_heuristic
                elif k == pygame.K_t: vis.show_tree = not vis.show_tree
                elif k == pygame.K_UP:   depth_limit = min(9, depth_limit+1)
                elif k == pygame.K_DOWN: depth_limit = max(1, depth_limit-1)
                elif k == pygame.K_c: mode = MODE_AI_AI
                elif k == pygame.K_v: mode = MODE_HUMAN_AI
                elif k == pygame.K_b: mode = MODE_HUMAN_HUM
                elif k == pygame.K_SPACE:
                    if not game.game_over:
                        mv, stats = get_ai_move(game, algorithm, depth_limit,
                                                 use_ordering, evaluator, orderer)
                        if mv: game.make_move(*mv)
                        if show_heuristic:
                            evaluator.evaluate(game); heur_bd = dict(evaluator.last_breakdown)
                        if vis.show_tree:
                            vis.tree_root = tree_bldr.build(game, game.current_player)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game.game_over:
                    cell = vis.get_cell_at(*event.pos)
                    if cell:
                        human_turn = (mode == MODE_HUMAN_HUM or
                                      (mode == MODE_HUMAN_AI and game.current_player == HUMAN_PLAYER))
                        if human_turn:
                            game.make_move(*cell)
                            if vis.show_tree:
                                vis.tree_root = tree_bldr.build(game, game.current_player)

        if not game.game_over and mode in (MODE_AI_AI, MODE_HUMAN_AI):
            is_ai = (mode == MODE_AI_AI or
                     (mode == MODE_HUMAN_AI and game.current_player == AI_PLAYER))
            if is_ai:
                mv, stats = get_ai_move(game, algorithm, depth_limit,
                                         use_ordering, evaluator, orderer)
                if mv: game.make_move(*mv)
                if show_heuristic:
                    evaluator.evaluate(game); heur_bd = dict(evaluator.last_breakdown)
                if vis.show_tree:
                    vis.tree_root = tree_bldr.build(game, game.current_player)
                pygame.time.delay(350)

        vis.draw(game, stats, mode, algorithm, depth_limit, show_heuristic, heur_bd)

    pygame.quit(); sys.exit()


if __name__ == "__main__":
    main()
