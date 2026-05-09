# Lecture 5 – Adversarial Search & Game AI
### Pygame Demonstration Suite

A four-version interactive Pygame project demonstrating every major concept
from Lecture 5: Adversarial Search.

---

## Quick Start

```bash
pip install pygame==2.5.2

# Run any version
python Version1_TicTacToe_Adversarial_Search/main.py
python Version2_Connect3_Adversarial_Search/main.py
python Version3_Horizon_Effect_Lab/main.py
python Version4_JSE_Trading_Duel/main.py
```

---

## Project Structure

```
Lecture5_Adversarial_Search_Game_AI/
│
├── Version1_TicTacToe_Adversarial_Search/   ← Small game, full tree search
├── Version2_Connect3_Adversarial_Search/    ← Larger game, same algorithms
├── Version3_Horizon_Effect_Lab/             ← Horizon effect demonstration
├── Version4_JSE_Trading_Duel/               ← Finance-inspired adversarial game
├── requirements.txt
└── README.md  (this file)
```

---

## Lecture 5 Concepts Explained

### What Is Adversarial Search?

Adversarial search is search in a **two-player zero-sum game** where one
player's gain is the other's loss.  Unlike single-agent search (finding a
path), adversarial search must account for an opponent who is trying to
defeat you.

Examples: Chess, TicTacToe, Connect 4, Poker (with full information).

---

### Game Trees

A **game tree** is a tree where:
- The **root** is the current game state.
- Each **edge** represents one legal move.
- Each **leaf** is a terminal state (win/loss/draw).
- **Branching factor** = number of legal moves from any state.
- **Depth** = number of plies (half-moves) searched.

The total number of nodes = O(b^d) where b = branching factor, d = depth.

---

### MAX and MIN Nodes

The two players have opposite goals:

| Node type | Player   | Chooses the child with... |
|-----------|----------|---------------------------|
| MAX node  | AI       | **highest** utility score |
| MIN node  | Opponent | **lowest** utility score  |

Levels alternate: MAX, MIN, MAX, MIN, …

---

### Utility Values

A **utility function** assigns a numeric score to terminal states:

```
AI wins  → +1   (or +100 in depth-limited versions)
Draw     →  0
AI loses → -1   (or -100)
```

For heuristic evaluation at non-terminal states, the utility is estimated
by a **heuristic function** that scores the position without fully solving it.

---

### Minimax Algorithm

Minimax is the foundational adversarial search algorithm.

```
function MINIMAX(state, is_max):
    if TERMINAL(state):
        return UTILITY(state)
    if is_max:
        return max(MINIMAX(child, False) for child in CHILDREN(state))
    else:
        return min(MINIMAX(child, True) for child in CHILDREN(state))
```

**Properties:**
- Complete: yes (finite games)
- Optimal: yes (against a perfect opponent)
- Time: O(b^d)
- Space: O(bd)

**Weakness:** Explores every node — very slow for large games.

---

### Alpha-Beta Pruning

Alpha-beta pruning **cuts** branches that cannot affect the final decision.

- **α (alpha):** best value MAX can guarantee (lower bound)
- **β (beta):**  best value MIN can guarantee (upper bound)

If β ≤ α at any node, prune all remaining children of that node.

```
if is_max:
    alpha = max(alpha, score)
    if beta <= alpha: PRUNE (break)
else:
    beta = min(beta, score)
    if beta <= alpha: PRUNE (break)
```

**Savings:** Up to O(b^(d/2)) — effectively doubles searchable depth.
Best case (perfect move ordering): √(b^d) nodes instead of b^d.

---

### Move Ordering

Alpha-beta pruning is most effective when the **best moves are searched first**,
because that causes cutoffs as early as possible.

**Heuristics for ordering:**
- Centre cells before edges (TicTacToe, Connect-3)
- Buy rising assets before falling ones (JSE Duel)
- Moves that immediately threaten a win

Well-ordered alpha-beta performs as well as or better than plain minimax
searching the same depth, with far fewer nodes.

---

### Heuristic Evaluation

When the game tree is too large to search completely, we use a
**heuristic evaluation function** to estimate the value of non-terminal states.

Good heuristics are:
1. **Cheap to compute** (must be called millions of times)
2. **Correlated with winning** (positions that look good should be good)
3. **Consistent** (similar positions get similar scores)

Example (TicTacToe / Connect-3):
- Lines with only AI pieces: +10 per two-in-a-row, +1 per one-in-a-row
- Lines with only opponent pieces: -10 / -1
- Centre control: +3
- Corner control: +1 per corner

The heuristic replaces the exact utility at **depth cutoff nodes**.

---

### Depth Cutoffs (Depth-Limited Search)

Instead of searching to the true terminal states, we stop at a fixed depth d
and apply the heuristic evaluation function.

```
function DLS(state, depth, alpha, beta, is_max):
    if TERMINAL(state): return UTILITY(state)
    if depth == 0:      return HEURISTIC(state)    ← cutoff
    ...
```

**Trade-off:** Deeper search = better decisions, slower computation.
This makes the **horizon effect** possible.

---

### The Horizon Effect

The **horizon effect** occurs when:
1. A decisive event (winning move, losing position) lies just beyond the
   search depth.
2. The AI cannot see it.
3. The AI may "push" a loss just beyond its search horizon rather than
   addressing it.

**Example:** At depth=2, the AI does not see that the opponent has a fork
attack building at depth=3.  It plays a locally good move that is globally
catastrophic.

**Version 3** of this suite is dedicated entirely to demonstrating this effect
with preset scenarios.

---

### Transposition Tables

Many game trees contain **transpositions** — the same board state reachable
via different move sequences.

A **transposition table** (hash map from board state → evaluated score) avoids
re-evaluating the same position twice.

```
key = hash(board_state)
if key in table and table[key].depth >= current_depth:
    return table[key].score          ← cache hit!
...
table[key] = (depth, score)          ← store result
```

Transposition tables can cut search time dramatically in games with high
transposition rates (like Connect-N where pieces are placed anywhere).

---

## How Lecture 5 Differs from Lectures 3 and 4

| Feature          | Lecture 3 (Uninformed) | Lecture 4 (Informed) | Lecture 5 (Adversarial) |
|------------------|------------------------|----------------------|-------------------------|
| Environment      | Single agent           | Single agent         | Two-player zero-sum     |
| Search goal      | Find a path            | Find optimal path    | Maximise against opponent |
| Opponent model   | None                   | None                 | MIN player               |
| Algorithm        | BFS / DFS / UCS        | A*, Greedy           | Minimax, Alpha-Beta      |
| Heuristic role   | —                      | Guides search        | Evaluates positions at cutoff |
| Completeness     | Yes (BFS)              | Yes (A*)             | Yes (finite, full search) |
| Depth limit need | No (exact)             | No (exact)           | Yes (for large games)    |

---

## Version Summary

| Version | Game              | Key Concepts |
|---------|-------------------|--------------|
| 1       | 3×3 TicTacToe     | Minimax, Alpha-Beta, Move Ordering, Heuristic, Game Tree |
| 2       | 4×4 Connect-3     | Same algorithms on larger board — shows complexity growth |
| 3       | Horizon Effect Lab| Depth limits, Horizon Effect, Transposition Table |
| 4       | JSE Trading Duel  | Adversarial search in a finance-inspired turn-based game |

---

## Requirements

- Python 3.8+
- `pygame==2.5.2`  (`pip install pygame==2.5.2`)

Each version is self-contained — run its `main.py` directly.
