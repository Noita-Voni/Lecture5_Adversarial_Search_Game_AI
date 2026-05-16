"""
Version 4 – JSE Trading Duel
Run: python main.py

Controls
--------
Click btn  Human action (shown on board when it's your turn)
A          AI makes its move
M          Minimax algorithm
P          Alpha-Beta algorithm
L          Depth-Limited + heuristic
UP/DOWN    Change depth limit
H          Toggle heuristic breakdown
SPACE      Advance turn (apply event, prompt next actions)
R          Reset game
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from market import Market
from game import GameState, AI_IDX, HUMAN_IDX
from visualizer import Visualizer
from algorithms.minimax import minimax
from algorithms.alpha_beta import alpha_beta
from algorithms.depth_limited_search import depth_limited_search
from algorithms.heuristic_eval import HeuristicEvaluator
from algorithms.move_ordering import MoveOrderer

ALG_MINIMAX = "Minimax"
ALG_AB      = "Alpha-Beta"
ALG_DEPTH   = "Depth-Limited"


def compute_ai_move(game, algorithm, depth_limit, evaluator, orderer, use_ordering):
    stats = {'nodes':0,'pruned':0,'ai_action':None,'score':0}
    if algorithm == ALG_MINIMAX:
        act, sc, nd = minimax(game, depth_limit)
        stats.update(ai_action=act, score=sc, nodes=nd)
    elif algorithm == ALG_AB:
        act, sc, nd, pr = alpha_beta(game, depth_limit, use_ordering, orderer)
        stats.update(ai_action=act, score=sc, nodes=nd, pruned=pr)
    else:
        act, sc, nd, pr = depth_limited_search(game, depth_limit, evaluator,
                                                use_ordering, orderer)
        stats.update(ai_action=act, score=sc, nodes=nd, pruned=pr)
    return act, stats


def main():
    market    = Market(seed=42)
    game      = GameState(market)
    vis       = Visualizer()
    evaluator = HeuristicEvaluator()
    orderer   = MoveOrderer()

    algorithm    = ALG_AB
    depth_limit  = 3
    use_ordering = True
    show_heuristic = False

    stats   = {'nodes':0,'pruned':0,'ai_action':None,'score':0}
    heur_bd = None

    # Turn phases: 'apply_event' -> 'ai_move' -> 'human_move' -> 'end_turn'
    phase = 'apply_event'
    waiting_human = False
    selected_action = None
    ai_done    = False
    human_done = False
    pending_ai_action = None

    # Apply first event
    game.advance_event()
    phase = 'ai_move'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_r:
                    market    = Market(seed=42)
                    game      = GameState(market)
                    game.advance_event()
                    phase     = 'ai_move'
                    ai_done   = False
                    human_done = False
                    waiting_human = False
                    stats     = {'nodes':0,'pruned':0,'ai_action':None,'score':0}
                    heur_bd   = None
                    pending_ai_action = None
                elif k == pygame.K_m:  algorithm = ALG_MINIMAX
                elif k == pygame.K_p:  algorithm = ALG_AB
                elif k == pygame.K_l:  algorithm = ALG_DEPTH
                elif k == pygame.K_UP:   depth_limit = min(5, depth_limit+1)
                elif k == pygame.K_DOWN: depth_limit = max(1, depth_limit-1)
                elif k == pygame.K_h:
                    show_heuristic = not show_heuristic
                    if show_heuristic:
                        evaluator.evaluate(game)
                        heur_bd = dict(evaluator.last_breakdown)

                elif k == pygame.K_a:
                    # AI makes move now
                    if not game.is_terminal() and phase == 'ai_move':
                        act, stats = compute_ai_move(game, algorithm, depth_limit,
                                                      evaluator, orderer, use_ordering)
                        if act:
                            game.apply_action(AI_IDX, act)
                            game.ai_last_action = act
                        if show_heuristic:
                            evaluator.evaluate(game)
                            heur_bd = dict(evaluator.last_breakdown)
                        ai_done = True
                        phase = 'human_move'
                        waiting_human = True

                elif k == pygame.K_SPACE:
                    # Advance: apply event for next turn or move to next phase
                    if phase == 'apply_event' and not game.is_terminal():
                        game.advance_event()
                        phase = 'ai_move'
                        ai_done = False
                        human_done = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if waiting_human and not game.is_terminal():
                    act = vis.get_button_action(*event.pos)
                    if act:
                        valid = game.get_valid_actions(HUMAN_IDX)
                        if act in valid:
                            game.apply_action(HUMAN_IDX, act)
                            game.human_last_action = act
                            human_done = True
                            waiting_human = False
                            # End turn
                            game.advance_turn()
                            if not game.is_terminal():
                                game.advance_event()
                                ai_done = False
                                human_done = False
                                phase = 'ai_move'
                            else:
                                phase = 'done'

        # Auto AI move in ai_move phase
        if not game.is_terminal() and phase == 'ai_move' and not ai_done:
            act, stats = compute_ai_move(game, algorithm, depth_limit,
                                          evaluator, orderer, use_ordering)
            if act:
                game.apply_action(AI_IDX, act)
                game.ai_last_action = act
            if show_heuristic:
                evaluator.evaluate(game)
                heur_bd = dict(evaluator.last_breakdown)
            ai_done = True
            phase = 'human_move'
            waiting_human = True
            pygame.time.delay(400)

        valid_hu = game.get_valid_actions(HUMAN_IDX) if waiting_human else []
        vis.draw(game, stats, algorithm, depth_limit, show_heuristic, heur_bd,
                 valid_hu, selected_action, waiting_human)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
