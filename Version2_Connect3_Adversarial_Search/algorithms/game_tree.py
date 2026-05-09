"""Game tree builder for Connect-3 visualization."""

class TreeNode:
    def __init__(self, state, move=None, depth=0, score=None, is_max=True, pruned=False):
        self.state = state.clone()
        self.move = move
        self.depth = depth
        self.score = score
        self.is_max = is_max
        self.pruned = pruned
        self.children = []

class GameTreeBuilder:
    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def build(self, game, ai_player):
        is_max = (game.current_player == ai_player)
        root = TreeNode(game, depth=0, is_max=is_max)
        self._expand(root, game, self.max_depth, ai_player, float('-inf'), float('inf'))
        return root

    def _expand(self, node, state, depth, ai_player, alpha, beta):
        if state.is_terminal() or depth == 0:
            node.score = state.get_utility(ai_player) if state.is_terminal() else 0
            return node.score
        moves = state.get_valid_moves()[:8]  # limit branching for display
        best = float('-inf') if node.is_max else float('inf')
        for mv in moves:
            state.make_move(*mv)
            child = TreeNode(state, move=mv, depth=node.depth+1, is_max=not node.is_max)
            score = self._expand(child, state, depth-1, ai_player, alpha, beta)
            state.undo_move(*mv)
            node.children.append(child)
            if node.is_max:
                if score > best: best = score
                alpha = max(alpha, best)
                if beta <= alpha: child.pruned = True; break
            else:
                if score < best: best = score
                beta = min(beta, best)
                if beta <= alpha: child.pruned = True; break
        node.score = best
        return best
