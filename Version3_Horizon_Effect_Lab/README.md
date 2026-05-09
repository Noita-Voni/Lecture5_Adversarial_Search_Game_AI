# Version 3 – Horizon Effect Lab

## Purpose

This interactive lab demonstrates four core concepts from adversarial game-tree search:

1. **The Horizon Effect** – shallow depth-limited search causes an AI to make poor decisions because the decisive event (a fork, a winning move, a forced loss) lies just beyond its search horizon.
2. **Depth-Limited Minimax with Heuristic Cutoff** – the AI searches to a fixed depth and evaluates non-terminal states with a heuristic function.
3. **Alpha-Beta Pruning** – an optimisation that eliminates branches that cannot influence the final decision, reducing nodes searched without changing the result.
4. **Transposition Tables** – a memoisation cache that avoids re-evaluating board states reached via different move orders, demonstrating how cache hits reduce computation.

---

## What Is the Horizon Effect?

The horizon effect occurs when a depth-limited search engine cannot "see" a critical game event because it lies beyond the search depth. The AI reaches its horizon and evaluates the position with a heuristic that gives no indication of what is about to happen. As a result, the AI may:

- Defend against a minor threat while ignoring a winning fork just one move deeper.
- Choose a move that looks locally safe but leads to a forced loss at depth+1.
- Delay a losing move to push the bad outcome "over the horizon", creating an illusion of safety.

This lab uses preset scenarios to make the horizon effect clearly visible and measurable.

---

## The Game: Connect-3

- Players alternate placing pieces (X and O) on an empty cell.
- The first player to place WIN_LEN (3) pieces in a row — horizontally, vertically, or diagonally — wins.
- Boards are either 4x4 or 5x5 depending on the scenario.
- There is no gravity (pieces can be placed anywhere, unlike standard Connect Four).

---

## Four Preset Scenarios

### Scenario 1 – Horizon Effect: Classic Fork (`horizon_classic`, 4x4)
**Key teaching point:** The horizon effect caused by a fork threat.

X has pieces arranged so that it has two separate win threats that together form a fork. At search depth 1 or 2, the AI (O) evaluates the board shallowly and defends only one of the two threats. At depth 3, the AI sees both threats simultaneously and correctly identifies the fork-blocking move. Run this scenario, set depth to 1, press SPACE, then reset and repeat at depth 3 to see different moves chosen.

### Scenario 2 – Delayed Winning Threat (`delayed_threat`, 4x4)
**Key teaching point:** Immediate wins invisible to depth-0 heuristic evaluation.

O has an immediate winning move available. However, a depth-0 evaluation (pure heuristic, no lookahead) may score other moves higher based on positional features alone, missing the win. At depth 1 or higher, the winning move is always found. This illustrates why heuristic evaluation alone is insufficient and why even one ply of lookahead matters.

### Scenario 3 – 5x5 Deep Fork (`deep_fork`, 5x5)
**Key teaching point:** Deeper forks require proportionally deeper search.

On a larger 5x5 board, X has constructed a position where a fork threat only becomes apparent at depth 4 or above. At depths 1-3 the AI (O) cannot perceive the danger and will make locally reasonable but strategically poor moves. Switch between depth 2 and depth 4 to observe completely different AI behaviour. The node count also demonstrates the exponential cost of deeper search.

### Scenario 4 – Transposition Table Demo (`transposition_demo`, 4x4)
**Key teaching point:** Many move sequences lead to identical board states.

The starting position is symmetric, meaning many different move orders produce the same board configuration. Enable the transposition table (press T) and watch cache hits accumulate as the AI avoids re-evaluating identical positions. Compare nodes searched with the table on vs off to quantify the saving.

---

## Algorithms

### Depth-Limited Minimax (`algorithms/depth_limited_minimax.py`)
Standard minimax with a hard depth cutoff. At the cutoff, the heuristic evaluator scores the position instead of searching further. The horizon effect arises directly from this cutoff: events beyond depth N are invisible to the AI. Returns: best move, score, nodes searched, branches pruned, cache hits.

### Alpha-Beta with Cutoff (`algorithms/alpha_beta_cutoff.py`)
A named wrapper around depth-limited minimax with `use_pruning=True`. Alpha-beta maintains a window [alpha, beta]: any branch that cannot beat the current best is pruned without evaluation. This can reduce the search from O(b^d) to O(b^(d/2)) in the best case, effectively doubling the reachable depth for the same computation budget.

### Heuristic Evaluator (`algorithms/heuristic_eval.py`)
Scores a non-terminal position along two dimensions:
- **Line score**: for each win-length segment on the board, award points for partially-filled AI lines and deduct points for partially-filled opponent lines. Segments with two-of-three pieces score 10; single pieces score 1.
- **Centre bonus**: pieces closer to the board centre receive a small positional bonus, reflecting the strategic value of central control.

The evaluator exposes `last_breakdown` so the UI can display each component separately (press H).

### Transposition Table (`algorithms/transposition_table.py`)
A dictionary mapping board states (as tuples) to previously computed scores. An entry is only used if it was computed at a depth greater than or equal to the current search depth, ensuring correctness. The table tracks hits and stores for display in the stats panel.

### Horizon Effect Demo Helper (`algorithms/horizon_effect_demo.py`)
Provides `compare_depths()` which runs the AI at multiple depths and returns a list of results, and `detect_horizon_effect()` which returns True if the chosen move changes between shallow and deep search — confirming the horizon effect is active.

---

## How to Run

Ensure you have Python 3.8+ and Pygame installed:

```
pip install pygame
```

Navigate to the Version3 directory and run:

```
python main.py
```

The window is 1100x720. The left panel shows the game board; the right panel shows scenario info, search statistics, heuristic breakdown, and controls.

---

## Controls

| Key         | Action                                              |
|-------------|-----------------------------------------------------|
| E           | Load the currently selected scenario                |
| 1           | Load Scenario 1: Horizon Effect Classic Fork        |
| 2           | Load Scenario 2: Delayed Winning Threat             |
| 3           | Load Scenario 3: 5x5 Deep Fork                     |
| 4           | Load Scenario 4: Transposition Table Demo           |
| UP arrow    | Increase search depth limit (max 8)                 |
| DOWN arrow  | Decrease search depth limit (min 1)                 |
| SPACE       | AI makes one move at the current depth              |
| H           | Toggle heuristic breakdown display                  |
| P           | Toggle alpha-beta pruning on/off                    |
| O           | Toggle move ordering on/off                         |
| T           | Toggle transposition table on/off                   |
| R           | Reset to free-play on a blank 4x4 board             |
| Click       | Place a piece manually on any empty cell            |

---

## Recommended Observation: The Horizon Effect in Action

Follow these steps to clearly see the horizon effect:

1. Press **1** to load Scenario 1 (Horizon Classic Fork). The board loads with X in a fork-threatening position and O to move.
2. Press **DOWN** until Depth Limit shows **1**.
3. Press **SPACE** to let the AI (O) make a move. Note the cell it chooses and the score.
4. Press **1** again to reload the same scenario.
5. Press **UP** until Depth Limit shows **3**.
6. Press **SPACE** again. The AI now chooses a **different move** — one that blocks the fork.

At depth 1, the AI cannot see that X will win on the next move after a fork is established. At depth 3, it sees both threats and the inevitable loss if left unblocked, so it responds correctly.

The nodes-searched counter will jump dramatically between depth 1 and depth 3, illustrating the exponential cost of deeper search. Enabling alpha-beta pruning (P) will reduce this cost while producing the same move.

### Additional Experiments

- **Scenario 3 at depth 2 vs depth 4**: On the 5x5 board the fork is only visible at depth 4. The AI at depth 2 will play a positionally neutral move; at depth 4 it correctly identifies and blocks the threat.
- **Scenario 4 with T on vs off**: Enable the transposition table and watch cache hits accumulate. Disable it and compare total nodes searched to see the saving.
- **Pruning comparison**: Load any scenario, record nodes at depth 4 with P=ON, then press P to disable pruning and press SPACE again. Node count increases significantly with pruning off.
- **Heuristic inspection**: Press H to see the line score and centre score components that drive the depth-0 evaluation. Scenario 2 with depth=1 and H=ON shows how the immediate win raises the line score sharply.

---

## File Structure

```
Version3_Horizon_Effect_Lab/
    main.py                          Entry point and game loop
    game.py                          GameState: board logic for configurable Connect-N
    scenarios.py                     Four preset horizon-effect scenarios
    visualizer.py                    Pygame rendering: board and stats panel
    algorithms/
        __init__.py                  Package marker (empty)
        depth_limited_minimax.py     Core depth-limited minimax with optional alpha-beta
        alpha_beta_cutoff.py         Named wrapper: alpha-beta with cutoff
        heuristic_eval.py            Position evaluator (line score + centre bonus)
        transposition_table.py       Memoisation cache for board states
        horizon_effect_demo.py       Multi-depth comparison and detection helper
    README.md                        This file
```
