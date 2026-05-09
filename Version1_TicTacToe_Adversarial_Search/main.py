"""
Version 1 - TicTacToe Adversarial Search
Entry point: run `python main.py` from this directory.
Controls
--------
M          Minimax
A          Alpha-Beta
D          Depth-Limited (uses heuristic at cutoff)
O          Toggle move ordering
H          Toggle heuristic breakdown display
UP / DOWN  Increase / decrease depth limit
T          Toggle game-tree preview
R          Reset game
C          AI vs AI mode
V          Human vs AI mode
B          Human vs Human mode
SPACE      Trigger one AI move
Click      Human move (on board)
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

# -- constants ----------------------------------------------------------------
MODE_HUMAN_AI  = 0
MODE_AI_AI     = 1
MODE_HUMAN_HUM = 2

ALG_MINIMAX    = "Minimax"
ALG_ALPHABETA  = "Alpha-Beta"
ALG_DEPTH      = "Depth-Limited"

AI_PLAYER      = 'X'   # AI is X in Human vs AI mode
HUMAN_PLAYER   = 'O'


def get_ai_move(game, algorithm, depth_limit, use_ordering, evaluator, orderer):
    """Call the selected algorithm and return (move, stats_dict)."""
    stats = {'nodes': 0, 'pruned': 0, 'best_move': None, 'best_score': 0}
    ai_p = game.current_player
    if algorithm == ALG_MINIMAX:
        mv, sc, nd = minimax(game, ai_p)
        stats.update(nodes=nd, best_move=mv, best_score=sc)
    elif algorithm == ALG_ALPHABETA:
        mv, sc, nd, pr = alpha_beta(game, ai_p, use_ordering, orderer)
        stats.update(nodes=nd, pruned=pr, best_move=mv, best_score=sc)
    else:  # Depth-Limited
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
    algorithm      = ALG_ALPHABETA
    depth_limit    = 9
    use_ordering   = True
    show_heuristic = False

    stats = {'nodes': 0, 'pruned': 0, 'best_move': None, 'best_score': 0}
    heur_bd = None

    ai_move_pending = False   # for AI vs AI pacing

    running = True
    while running:
        # -- events -----------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_r:
                    game.reset()
                    stats = {'nodes':0,'pruned':0,'best_move':None,'best_score':0}
                    heur_bd = None
                    vis.tree_root = None
                elif k == pygame.K_m:  algorithm = ALG_MINIMAX
                elif k == pygame.K_a:  algorithm = ALG_ALPHABETA
                elif k == pygame.K_d:  algorithm = ALG_DEPTH
                elif k == pygame.K_o:  use_ordering = not use_ordering
                elif k == pygame.K_h:
                    show_heuristic = not show_heuristic
                elif k == pygame.K_t:  vis.show_tree = not vis.show_tree
                elif k == pygame.K_UP:
                    depth_limit = min(9, depth_limit + 1)
                elif k == pygame.K_DOWN:
                    depth_limit = max(1, depth_limit - 1)
                elif k == pygame.K_c:  mode = MODE_AI_AI
                elif k == pygame.K_v:  mode = MODE_HUMAN_AI
                elif k == pygame.K_b:  mode = MODE_HUMAN_HUM
                elif k == pygame.K_SPACE:
                    if not game.game_over:
                        mv, stats = get_ai_move(game, algorithm, depth_limit,
                                                 use_ordering, evaluator, orderer)
                        if mv:
                            game.make_move(*mv)
                        if show_heuristic:
                            evaluator.evaluate(game)
                            heur_bd = evaluator.last_breakdown.copy()
                        if vis.show_tree:
                            vis.tree_root = tree_bldr.build(game, game.current_player)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Human move
                can_move = (
                    not game.game_over and
                    mode == MODE_HUMAN_HUM or
                    (mode == MODE_HUMAN_AI and game.current_player == HUMAN_PLAYER)
                )
                if not game.game_over:
                    cell = vis.get_cell_at(*event.pos)
                    if cell:
                        human_turn = (
                            mode == MODE_HUMAN_HUM or
                            (mode == MODE_HUMAN_AI and game.current_player == HUMAN_PLAYER)
                        )
                        if human_turn:
                            game.make_move(*cell)
                            if vis.show_tree:
                                vis.tree_root = tree_bldr.build(game, game.current_player)

        # -- auto AI move -----------------------------------------------------
        if not game.game_over and mode in (MODE_AI_AI, MODE_HUMAN_AI):
            is_ai_turn = (
                mode == MODE_AI_AI or
                (mode == MODE_HUMAN_AI and game.current_player == AI_PLAYER)
            )
            if is_ai_turn:
                mv, stats = get_ai_move(game, algorithm, depth_limit,
                                         use_ordering, evaluator, orderer)
                if mv:
                    game.make_move(*mv)
                if show_heuristic:
                    evaluator.evaluate(game)
                    heur_bd = evaluator.last_breakdown.copy()
                if vis.show_tree:
                    vis.tree_root = tree_bldr.build(game, game.current_player)
                pygame.time.delay(300)   # pace AI vs AI

        # -- render -----------------------------------------------------------
        vis.draw(game, stats, mode, algorithm, depth_limit, show_heuristic, heur_bd)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
