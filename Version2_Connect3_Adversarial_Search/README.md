# Version 2 – Connect-3 Adversarial Search (4x4 Board)

## Purpose

This version applies **exactly the same Lecture 5 adversarial search algorithms** from Version 1 (TicTacToe) to a larger 4x4 Connect-3 board. The goal is to demonstrate concretely how **search complexity scales** with board size and branching factor, and why optimisations like alpha-beta pruning, move ordering, and heuristic evaluation become not just helpful but *essential*.

### Comparison with Version 1 (TicTacToe 3x3)
| Metric                 | V1 TicTacToe (3x3) | V2 Connect-3 (4x4) |
|------------------------|--------------------|--------------------|
| Board cells            | 9                  | 16                 |
| Max branching factor   | 9                  | 16                 |
| Depth of game tree     | up to 9            | up to 16           |
| Terminal nodes (naive) | ~362,880           | ~20,922,789,888,000|
| Pure Minimax usable?   | Yes, fast          | Very slow / hangs  |
| Alpha-Beta needed?     | Helpful            | Essential          |
| Heuristic cutoff?      | Optional           | Required for speed |

The 4x4 board has a branching factor nearly double that of TicTacToe. Without pruning, the full minimax tree for Connect-3 is computationally intractable at early moves. This version makes that cost visible in the "Nodes searched" stat panel.

---

## Game Rules

- **Grid**: 4 rows x 4 columns (16 cells total)
- **Placement**: Players alternate placing their piece (X or O) in **any empty cell** – there is no gravity; this is not Connect Four
- **Win condition**: First player to connect **3 pieces in a row** horizontally, vertically, or diagonally wins
- **Draw**: If all 16 cells are filled with no winner, the game is a draw
- **Players**: Human vs AI, AI vs AI, or Human vs Human

### Win Lines
There are 22 possible winning lines on a 4x4 board:
- 8 horizontal (2 per row x 4 rows)
- 8 vertical (2 per column x 4 columns)
- 4 diagonal down-right
- 4 diagonal down-left (anti-diagonal)

---

## Algorithms

### 1. Pure Minimax (`M`)
The foundational adversarial search algorithm. Explores the **entire game tree** to find the optimal move. No pruning, no depth limit.

- **Teaches**: How the minimax principle works – MAX player maximises, MIN player minimises
- **Problem on 4x4**: At the start of the game, there are 16 possible first moves, 15 second moves, etc. The tree explodes. Minimax may take many seconds or even hang at early game states
- **Node count**: Expect tens of thousands to millions of nodes even mid-game

### 2. Alpha-Beta Pruning (`A`)
Minimax with alpha-beta cutoffs. Prunes branches that cannot possibly affect the final decision.

- **Teaches**: How maintaining alpha (best MAX found) and beta (best MIN found) windows allows entire subtrees to be skipped
- **Effect on 4x4**: Reduces node count dramatically – often by 60–90% with good move ordering
- **Branches pruned stat**: Watch this counter increase; each pruned branch is a subtree skipped entirely
- **Best case**: Reduces effective branching factor from b to sqrt(b), making depth d search cost b^(d/2) instead of b^d

### 3. Depth-Limited Search with Heuristic Evaluation (`D`)
Alpha-beta with a depth cutoff. When the search reaches the depth limit, a **heuristic function** evaluates the board instead of continuing to a terminal state.

- **Teaches**: How to make AI practical when full tree search is intractable; the tradeoff between search depth and evaluation quality
- **Depth limit**: Adjust with UP/DOWN arrow keys (1–9)
- **Heuristic**: Scores lines (2-in-a-row = +10, 1-in-a-row = +1 for AI; negatives for opponent) plus center control bonus
- **Essential for this board**: At depth 5+ with full minimax this would be impossibly slow; depth-limited search makes it interactive

### 4. Move Ordering (`O`)
Sorts candidate moves before searching – center cells are tried first.

- **Teaches**: Why the order in which branches are explored affects alpha-beta efficiency enormously
- **Logic**: Center cells (1,1), (1,2), (2,1), (2,2) have the lowest priority distance score, so they are tried first. These tend to be stronger moves, causing better alpha-beta cutoffs
- **Effect**: Toggle ON/OFF with `O` and observe the difference in nodes searched and branches pruned

### 5. Game Tree Preview (`T`)
Toggles a visual mini-tree at the bottom of the board showing MAX nodes (green), MIN nodes (red), and pruned branches (grey with X marks).

- **Teaches**: Visual intuition for how the tree expands and where pruning occurs
- **Depth shown**: 2 levels for clarity

### 6. Heuristic Breakdown (`H`)
When enabled, the stats panel shows a breakdown of the heuristic score components:
- `lines`: Score from counting 2-in-a-row and 1-in-a-row patterns across all 22 win lines
- `center`: Bonus/penalty for center cell control

---

## How to Run

### Requirements
```
pip install pygame
```

### Launch
```
cd Version2_Connect3_Adversarial_Search
python main.py
```

The game opens a 1000x680 window. The left side shows the 4x4 board; the right panel shows mode, algorithm, and live search statistics.

---

## Controls

| Key        | Action                                      |
|------------|---------------------------------------------|
| `M`        | Switch to Pure Minimax                      |
| `A`        | Switch to Alpha-Beta Pruning                |
| `D`        | Switch to Depth-Limited Search              |
| `O`        | Toggle move ordering ON/OFF                 |
| `H`        | Toggle heuristic score breakdown            |
| `UP`       | Increase depth limit (max 9)                |
| `DOWN`     | Decrease depth limit (min 1)                |
| `T`        | Toggle game tree preview panel              |
| `R`        | Reset the board                             |
| `SPACE`    | Trigger one AI move manually                |
| `C`        | Switch to AI vs AI mode                     |
| `V`        | Switch to Human vs AI mode                  |
| `B`        | Switch to Human vs Human mode               |
| `Click`    | Place a piece (human turns)                 |

---

## File Structure

```
Version2_Connect3_Adversarial_Search/
├── main.py                        # Entry point, game loop, event handling
├── game.py                        # GameState: board, moves, win detection, clone
├── visualizer.py                  # Pygame rendering: board, stats panel, tree panel
├── algorithms/
│   ├── __init__.py
│   ├── minimax.py                 # Pure minimax (no pruning)
│   ├── alpha_beta.py              # Alpha-beta pruning with optional move ordering
│   ├── depth_limited_search.py    # Depth-limited minimax + alpha-beta + heuristic
│   ├── move_ordering.py           # Center-first move ordering heuristic
│   ├── heuristic_eval.py          # Board evaluation: line scoring + center control
│   └── game_tree.py               # Tree builder for visual preview
└── README.md
```

---

## What to Observe

### Node Count Explosion
- Press `M` (Minimax) early in the game and press `SPACE`. Watch the "Nodes searched" counter. On a fresh board it may reach hundreds of thousands or more, and the AI will pause noticeably
- Compare: in Version 1 TicTacToe, the same Minimax is near-instant because the tree is tiny

### Alpha-Beta is Essential Here
- Press `A` (Alpha-Beta) and notice the dramatic drop in nodes searched vs Minimax
- Watch "Branches pruned" climb – each pruned branch is an entire subtree avoided
- Enable move ordering (`O`) and observe further reduction in nodes and more branches pruned

### Move Ordering Amplifies Pruning
- Toggle `O` ON and OFF while running Alpha-Beta
- With ordering ON, the AI tends to consider stronger moves first, which sets tighter alpha/beta windows earlier, causing more pruning
- The difference in node count is most visible early in the game when branching factor is highest

### Depth Limit and Heuristic Quality
- Switch to Depth-Limited (`D`) and try depth 2 vs depth 5 vs depth 8
- At low depth, AI may miss obvious threats because they are beyond the horizon
- Enable heuristic display (`H`) to see how the evaluator breaks down the board score
- Higher depth = stronger AI but more nodes; lower depth = faster but weaker play

### Game Tree Visualization
- Press `T` to see the live tree after each AI move
- Green nodes = MAX (AI maximising), Red nodes = MIN (opponent minimising)
- Grey nodes with X = pruned – the search never explored their subtrees
- Notice more grey nodes when move ordering is enabled

### Center Control
- The heuristic gives bonus points for controlling the 4 center cells (1,1), (1,2), (2,1), (2,2)
- These cells participate in the most win lines, making them strategically valuable
- Watch the AI prioritise these cells, especially in Depth-Limited mode

---

## Key Takeaway

Version 2 demonstrates the central lesson of Lecture 5: **adversarial search is only practical with aggressive optimisation**. The same algorithms that run instantly on TicTacToe become bottlenecks on a slightly larger board. Alpha-beta pruning, move ordering, and heuristic evaluation are not academic extras – they are what make game AI feasible in practice. Every real game AI (chess engines, Go programs, etc.) builds on exactly these principles.
