# Lecture 5 – Adversarial Search & Game AI
### Pygame Demonstration Suite

A four-version interactive Pygame project demonstrating every major concept
from Lecture 5: Adversarial Search.

---

## Quick Start

```bash
pip install pygame==2.5.2

python Version1_TicTacToe_Adversarial_Search/main.py
python Version2_Connect3_Adversarial_Search/main.py
python Version3_Horizon_Effect_Lab/main.py
python Version4_JSE_Trading_Duel/main.py
```

---

## Project Structure

```
L5_Adversarial_Search_Game_AI/
│
├── Version1_TicTacToe_Adversarial_Search/   ← Small game, full tree search
├── Version2_Connect3_Adversarial_Search/    ← Larger game, same algorithms
├── Version3_Horizon_Effect_Lab/             ← Horizon effect demonstration
├── Version4_JSE_Trading_Duel/               ← Finance-inspired adversarial game
├── requirements.txt
└── README.md  (this file)
```

---

## Screenshots & What They Show

### Version 1 — TicTacToe Adversarial Search

![V1 TicTacToe – Minimax, AI wins](<Version1_TicTacToe_Adversarial_Search/ver1 image.png>)

**What is happening:**
- Algorithm: **Minimax** at depth 9 (full tree, no pruning)
- The AI (X) has just played move **(2, 2)** — the bottom-right corner — to complete the diagonal
- The winning line from (0,0) → (1,1) → (2,2) is **highlighted in green**
- **Nodes searched: 10** — only 10 nodes remained to explore because the game was nearly over; earlier in the game minimax searches up to ~549,000 nodes from an empty board
- **Branches pruned: 0** — pure Minimax never prunes; it explores every child
- **Best score: 1** — the algorithm confirmed this move guarantees a win (+1 utility)

**Key learning:** On a 3×3 board Minimax is feasible — the entire game tree has at most 362,880 nodes. This makes TicTacToe a perfect demonstration of exact adversarial search.

---

### Version 2 — Connect-3 4×4 (Alpha-Beta vs Minimax comparison)

![V2 Connect3 – Alpha-Beta, 284 nodes, 96 pruned](<Version2_Connect3_Adversarial_Search/ver2 image.png>)

**What is happening (Alpha-Beta):**
- Algorithm: **Alpha-Beta Pruning** at depth 5
- The AI (X) won by connecting three diagonally; winning cells are highlighted in green
- **Nodes searched: 284** — alpha-beta explored only 284 nodes
- **Branches pruned: 96** — 96 branches were cut because they could not improve on the already-known best score
- **Best move: (0, 2)** — top-right area was the decisive play
- **Best score: 1** — exact win confirmed

---

![V2 Connect3 – Minimax same game, 344 nodes, 0 pruned](<Version2_Connect3_Adversarial_Search/ver2.2 image.png>)

**What is happening (Minimax — same board, same depth):**
- Algorithm: **Minimax** (no pruning) at depth 5
- **Nodes searched: 344** — 21% more nodes than alpha-beta (344 vs 284)
- **Branches pruned: 0** — Minimax cannot prune; it evaluates every branch
- **Best move: (1, 2)** — a different move is chosen because without pruning the search order affects which equally-good move appears first

**Key learning:** This side-by-side comparison is the core of Lecture 5. Same game, same depth, same result — but Alpha-Beta searched 21% fewer nodes. On a full board from move 1 the difference grows to over 10× fewer nodes, which is why alpha-beta is essential for larger games.

---

### Version 3 — Horizon Effect Lab

![V3 Horizon Lab – Free Play mode](<Version3_Horizon_Effect_Lab/ver3 image.png>)

**What is happening (Free Play):**
- Mode: **Free Play** (no scenario loaded)
- Winner: O — the human player out-played the AI with no depth advantage
- Search stats are all zero because no AI search was triggered in this state
- The board shows a completed game with O connecting three vertically on the left column

---

![V3 Horizon Lab – Classic Fork scenario, horizon warning active](<Version3_Horizon_Effect_Lab/ver3.2 image.png>)

**What is happening (Horizon Effect – Classic Fork):**
- Scenario **"Horizon Effect – Classic Fork"** is loaded (press `1` then `E`)
- The board is a preset position where **X has built a diagonal fork threat**
- The orange warning reads:  
  *"Depth ≤ 2 misses X's diagonal fork! Try depth 1 vs depth 3."*
- At **depth 1 or 2** the AI (O) cannot see far enough to detect both fork arms simultaneously — it defends one and X completes the other
- At **depth 3** the AI sees both arms and correctly blocks the fork
- Winner: X — the scenario deliberately shows a position where shallow search loses

**Key learning:** The horizon effect occurs when a decisive threat exists just beyond the search depth. The AI is not "stupid" — it is playing optimally within its depth limit. The limit itself is the problem. This is why heuristic cutoffs must be chosen carefully.

---

### Version 4 — JSE Trading Duel

![V4 JSE Trading Duel – Alpha-Beta, both players draw at R1440](<Version4_JSE_Trading_Duel/ver4 image.png>)

**What is happening:**
- Algorithm: **Alpha-Beta** at depth 3
- Game is over (Turn 6/5 means all 5 turns have completed)
- Result: **DRAW — both portfolios at R1440**
- The market event on the final turn was **BULL_MINING (+25%)** but it was too late to matter
- The **Turn Log** (bottom-right) shows the full game history:
  ```
  T1  AI: BUY_BANK    HU: BUY_BANK
  T2  AI: BUY_BANK    HU: BUY_BANK
  T3  AI: BUY_BANK    HU: BUY_BANK
  T4  AI: BUY_BANK    HU: BUY_BANK
  T5  AI: BUY_BANK    HU: BUY_BANK
  ```
  Both players bought BANK every single turn — the AI correctly identified this as optimal and the human matched it

**Heuristic breakdown (right panel, H key):**
| Component | Value | Meaning |
|-----------|-------|---------|
| `portfolio_diff` | +88 | AI portfolio slightly ahead mid-game |
| `cash_reserve` | 0.0 | No cash left (all invested) |
| `diversification` | +20 | Holding 1 asset type |
| `event_advantage` | 0.0 | Next event does not favour held assets |
| `risk_penalty` | −18 | Concentration penalty for all-in on one asset |

**Why R1440?** Both started with R1000. BANK starts at R200 (break-even buy price).
- 5 buys × R200 = R1000 spent, 0 cash left, 5 units of BANK
- BANK price after two BULL_BANK events: R200 × 1.20 × 1.20 = R288
- Final value: 5 units × R288 = **R1440**

**Key learning:** Adversarial search works in non-traditional games. The AI treats the opponent as a MIN player who minimises the AI's advantage, applies alpha-beta across 5 turns, and arrives at a principled strategy. The heuristic panel makes the AI's reasoning transparent.

---

## Lecture 5 Concepts Explained

### What Is Adversarial Search?

Adversarial search is search in a **two-player zero-sum game** where one
player's gain is the other's loss. Unlike single-agent search (finding a
path), adversarial search must account for an opponent who is trying to
defeat you.

---

### Game Trees

A **game tree** is a tree where:
- The **root** is the current game state
- Each **edge** represents one legal move
- Each **leaf** is a terminal state (win / loss / draw)
- **Branching factor** b = number of legal moves from any state
- **Depth** d = number of plies (half-moves) searched

Total nodes = O(b^d)

---

### MAX and MIN Nodes

| Node type | Player   | Chooses the child with... |
|-----------|----------|---------------------------|
| MAX node  | AI       | **highest** utility score |
| MIN node  | Opponent | **lowest** utility score  |

Levels alternate: MAX → MIN → MAX → MIN → …

---

### Utility Values

```
AI wins  → +1   (or +100 in depth-limited versions)
Draw     →  0
AI loses → −1   (or −100)
```

---

### Minimax Algorithm

```
function MINIMAX(state, is_max):
    if TERMINAL(state):
        return UTILITY(state)
    if is_max:
        return max(MINIMAX(child, False) for child in CHILDREN(state))
    else:
        return min(MINIMAX(child, True) for child in CHILDREN(state))
```

**Properties:** Complete and optimal against a perfect opponent. Time O(b^d).  
**Weakness:** Explores every node — too slow for large games (see V2 comparison screenshot above).

---

### Alpha-Beta Pruning

Cuts branches that cannot affect the final decision.

- **α (alpha):** best value MAX can guarantee so far
- **β (beta):**  best value MIN can guarantee so far
- If **β ≤ α** at any node → prune remaining children

**Savings:** Up to O(b^(d/2)) nodes — effectively doubles the searchable depth.  
**Demonstrated:** V2 screenshot shows 344 nodes (Minimax) vs 284 nodes (Alpha-Beta) at the same depth.

---

### Move Ordering

Alpha-beta prunes most when the **best move is tried first**.

- TicTacToe / Connect-3: centre cells first, then corners, then edges
- JSE Duel: buy the asset whose sector just had a bull event first

Good ordering can reduce node count by another 2–5× on top of basic alpha-beta.

---

### Heuristic Evaluation

When the tree is too large to search to terminal states, a **heuristic function**
estimates the value of non-terminal positions at the depth cutoff.

**Connect-3 heuristic components:**
- Lines with only AI pieces: +10 per two-in-a-row, +1 per one-in-a-row
- Lines with only opponent pieces: −10 / −1
- Centre control bonus

**JSE Duel heuristic components (visible in V4 screenshot):**
- Portfolio value difference
- Cash reserve flexibility
- Diversification bonus
- Upcoming event advantage
- Concentration risk penalty

---

### Depth Cutoffs & The Horizon Effect

Stopping search at depth d and calling the heuristic is called a **depth cutoff**.

The **horizon effect** occurs when a decisive event lies just beyond depth d —
the AI cannot see it, and may even make moves that push the problem past its
own horizon. Demonstrated in V3: at depth ≤ 2 the AI misses X's fork; at
depth 3 it sees and blocks both arms.

---

### Transposition Tables

The same board position can be reached via different move sequences.
A **transposition table** caches evaluated positions so they are not
re-computed. Toggle with `T` in Version 3 and watch Cache Hits increase.

---

## How Lecture 5 Differs from Lectures 3 and 4

| Feature          | Lecture 3 (Uninformed) | Lecture 4 (Informed) | Lecture 5 (Adversarial) |
|------------------|------------------------|----------------------|-------------------------|
| Environment      | Single agent           | Single agent         | Two-player zero-sum     |
| Search goal      | Find a path            | Find optimal path    | Maximise against opponent |
| Opponent model   | None                   | None                 | MIN player              |
| Algorithm        | BFS / DFS / UCS        | A*, Greedy           | Minimax, Alpha-Beta     |
| Heuristic role   | —                      | Guides search        | Evaluates at cutoff     |
| Depth limit need | No                     | No                   | Yes (for large games)   |

---

## Version Summary

| Version | Game              | Key Concepts Shown |
|---------|-------------------|--------------------|
| 1       | 3×3 TicTacToe     | Full Minimax tree, Alpha-Beta, Game Tree Preview |
| 2       | 4×4 Connect-3     | Node count explosion, Alpha-Beta essential, Move Ordering |
| 3       | Horizon Effect Lab| Depth cutoffs, Horizon Effect, Transposition Table |
| 4       | JSE Trading Duel  | Adversarial search in a finance turn-based game, Heuristic |

---

## Requirements

- Python 3.8+
- `pygame==2.5.2`

```bash
pip install pygame==2.5.2
```

Each version is self-contained — run its `main.py` directly from its folder.
