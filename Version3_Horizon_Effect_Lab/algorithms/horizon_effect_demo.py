"""
Horizon Effect demonstration helper.
Compares AI decisions at different depths to show when the horizon effect
causes the AI to play a suboptimal move.
"""

from algorithms.depth_limited_minimax import depth_limited_minimax


def compare_depths(game, ai_player, evaluator, depths=(1, 2, 3, 4)):
    """
    Run depth-limited minimax at each depth and return comparison data.
    Returns list of dicts: {depth, move, score, nodes, pruned}
    """
    results = []
    for d in depths:
        mv, sc, nd, pr, _ = depth_limited_minimax(
            game, ai_player, d, evaluator,
            use_move_ordering=False, move_orderer=None,
            use_pruning=True, transposition_table=None
        )
        results.append({'depth': d, 'move': mv, 'score': sc,
                        'nodes': nd, 'pruned': pr})
    return results


def detect_horizon_effect(results):
    """
    Returns True if the best move changes between shallow and deep search,
    suggesting the horizon effect is active.
    """
    if len(results) < 2:
        return False
    moves = [r['move'] for r in results if r['move'] is not None]
    return len(set(moves)) > 1
