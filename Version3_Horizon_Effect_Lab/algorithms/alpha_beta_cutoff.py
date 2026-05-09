"""Alpha-beta with configurable cutoff depth - wrapper for the lab."""

from algorithms.depth_limited_minimax import depth_limited_minimax


def alpha_beta_cutoff(game, ai_player, depth_limit, evaluator=None,
                      use_move_ordering=False, move_orderer=None,
                      transposition_table=None):
    """
    Explicitly named alpha-beta-with-cutoff for the lab.
    Returns (best_move, best_score, nodes, pruned, cache_hits).
    """
    return depth_limited_minimax(
        game, ai_player, depth_limit, evaluator,
        use_move_ordering, move_orderer,
        use_pruning=True,
        transposition_table=transposition_table
    )
