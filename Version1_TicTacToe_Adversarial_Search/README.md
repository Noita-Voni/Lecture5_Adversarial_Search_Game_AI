# Version 1 - TicTacToe Adversarial Search

## What This Version Demonstrates

This version uses the classic 3x3 TicTacToe game as a teaching vehicle for **adversarial search** -
the family of algorithms used when two competing agents (MAX and MIN) alternate decisions in a
zero-sum game. Because TicTacToe has a small, fully enumerable game tree (~255,168 terminal leaf
nodes from an empty board), it is the ideal sandbox for:

- Seeing the **complete** game tree explored by pure Minimax.
- Watching Alpha-Beta Pruning **cut branches** without changing the result.
- Understanding why **move ordering** matters (best-first ordering maximises pruning).
- Exploring how a **heuristic evaluation function** lets the agent stop before the leaves
  (depth-limited search), trading exactness for speed.
- Visualising the tree live, with MAX/MIN labels and pruned branches highlighted.


## The Game: 3x3 TicTacToe

- Two players: **X** and **O**, alternating turns.
- A player wins by placing three marks in a row (horizontal, vertical, or diagonal).
- The game is a **draw** if all 9 cells are filled with no winner.
- The state space is small enough that Minimax solves it **perfectly** in milliseconds.


## Algorithms Implemented

### 1. Pure Minimax (`algorithms/minimax.py`)
Performs a complete depth-first traversal of the game tree. At every MAX node the agent
picks the move with the highest score; at every MIN node it picks the lowest. Because no
pruning is applied, every reachable state is visited. On an empty board this visits
**~5,478 nodes** (with early terminal detection).

**What it teaches:** The foundational adversarial search principle - back-propagating utility
values from terminal states through alternating MAX/MIN layers.

### 2. Alpha-Beta Pruning (`algorithms/alpha_beta.py`)
Extends Minimax with two window parameters, **alpha** (best MAX has found) and **beta**
(best MIN has found). Any subtree that cannot improve the current bound is pruned. The
algorithm is **provably equivalent** to Minimax but explores far fewer nodes.

- Best case: O(b^(d/2)) nodes instead of O(b^d).
- With perfect move ordering, Alpha-Beta on TicTacToe visits as few as ~50-200 nodes
  from the first move.

**What it teaches:** That you can safely ignore entire subtrees - the "if MIN will never
let MAX get here, stop searching" intuition.

### 3. Move Ordering (`algorithms/move_ordering.py`)
Sorts candidate moves before expanding them: **centre first, then corners, then edges**.
Better moves evaluated first means tighter alpha/beta bounds earlier, which prunes more
branches. Toggle with **O** during play to see the node count difference.

**What it teaches:** The practical impact of exploration order on pruning efficiency.

### 4. Heuristic Evaluation (`algorithms/heuristic_eval.py`)
Scores a **non-terminal** board by:
- **Lines score**: +10 for two-in-a-row (open), +1 for one-in-a-row; mirror negatives for
  the opponent.
- **Centre bonus**: +3/-3 for controlling/losing the centre cell.
- **Corner bonus**: +1 per corner owned minus opponent corners.

Used as the leaf evaluator when depth-limited search hits its cutoff.

**What it teaches:** Domain-specific knowledge encoding; how heuristic scores differ from
exact minimax values, and why evaluation quality determines playing strength.

### 5. Depth-Limited Minimax (`algorithms/depth_limited_search.py`)
Runs Alpha-Beta but cuts the search off at a configurable depth and calls the heuristic
evaluator at the frontier. Terminal wins/losses are still scored exactly (x100 to dominate
heuristic noise). Adjust depth with **UP/DOWN** arrow keys.

**What it teaches:** The tradeoff between search depth and computational budget; how
shallow heuristic search can differ from full-tree perfect play.

### 6. Game Tree Preview (`algorithms/game_tree.py` + visualizer)
Builds a shallow (depth-2) Alpha-Beta tree rooted at the current position and renders it
at the bottom of the board area. Nodes are colour-coded:
- **Green** = MAX node
- **Red** = MIN node
- **Gray + X mark** = pruned subtree

**What it teaches:** Visual intuition for how the search tree expands and where pruning
fires.


## How to Run

1. Install the dependency:
   ```
   pip install pygame==2.5.2
   ```

2. Navigate to this directory and launch:
   ```
   python main.py
   ```

No other dependencies beyond the Python standard library are required.


## Controls

| Key           | Action                                         |
|---------------|------------------------------------------------|
| M             | Switch to pure Minimax                         |
| A             | Switch to Alpha-Beta Pruning                   |
| D             | Switch to Depth-Limited search                 |
| O             | Toggle move ordering on/off                    |
| H             | Toggle heuristic breakdown display             |
| UP arrow      | Increase depth limit (max 9)                   |
| DOWN arrow    | Decrease depth limit (min 1)                   |
| T             | Toggle game-tree preview panel                 |
| R             | Reset the board                                |
| C             | AI vs AI mode (watch two AIs play)             |
| V             | Human vs AI mode (you play O, AI plays X)      |
| B             | Human vs Human mode                            |
| SPACE         | Force one AI move (useful in Human vs Human)   |
| Left click    | Place your piece on a board cell               |


## What to Observe While It Runs

### Nodes searched drop dramatically with Alpha-Beta
Switch between **M** (Minimax) and **A** (Alpha-Beta) at the start of a game and watch the
"Nodes searched" counter. Alpha-Beta typically visits 5-20x fewer nodes from an empty board,
and the gap widens further when move ordering (**O**) is also enabled.

### Move ordering amplifies pruning
Enable Alpha-Beta, then toggle **O** off and on while resetting. With ordering disabled the
pruned-branches count drops noticeably, illustrating that Alpha-Beta's efficiency is
order-dependent.

### Depth limit changes AI quality
Switch to **Depth-Limited** (**D**) and press DOWN to set depth to 1 or 2. The AI will
occasionally make suboptimal moves because the heuristic at the cutoff does not perfectly
reflect game outcome. Raise depth back to 9 and it plays perfectly again. Toggle **H** to
see the live heuristic breakdown (lines/center/corners scores).

### Pruned branches visible in the tree preview
Press **T** to open the tree preview. The gray nodes with X marks are subtrees Alpha-Beta
determined it was safe to skip. Earlier/better move ordering produces more gray nodes.

### AI vs AI shows perfect play
Press **C** to watch two AI instances (both using the current algorithm) play each other.
With any exact algorithm (Minimax or full-depth Alpha-Beta) every game will end in a draw -
TicTacToe is a solved game and perfect play by both sides always draws.
