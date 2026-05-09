# Version 4 – JSE Trading Duel

## Purpose

This project applies classical adversarial search algorithms (Minimax, Alpha-Beta Pruning, and Depth-Limited Search with Heuristic Evaluation) to a simplified JSE-inspired financial trading game. Rather than a board game, the adversarial setting is a portfolio management duel: the AI attempts to maximise its own portfolio value relative to a human opponent over 5 turns of simulated market events.

This demonstrates that adversarial search is domain-agnostic — any two-player zero-sum setting with defined actions and terminal utility qualifies, including financial simulations.

---

## Game Design

### Overview

- **Turns:** 5 turns total
- **Players:** AI (MAX player) vs Human (MIN player)
- **Starting state:** Each player begins with R1000 cash and 0 holdings

### Assets

Three fictional assets are traded:

| Asset  | Base Price |
|--------|-----------|
| BANK   | R200      |
| MINING | R150      |
| RETAIL | R120      |

### Actions (choose one per turn)

| Action      | Effect                                                    |
|-------------|-----------------------------------------------------------|
| BUY_BANK    | Spend R200, gain 1 unit of BANK                          |
| BUY_MINING  | Spend R200, gain 1 unit of MINING                        |
| BUY_RETAIL  | Spend R200, gain 1 unit of RETAIL                        |
| SELL_BANK   | Sell 1 unit of BANK at current price, gain cash          |
| SELL_MINING | Sell 1 unit of MINING at current price, gain cash        |
| SELL_RETAIL | Sell 1 unit of RETAIL at current price, gain cash        |
| HOLD        | Do nothing                                                |

- BUY always costs R200 regardless of asset price
- SELL earns the current market price for that asset unit
- SELL actions are only valid if you hold at least 1 unit of that asset
- BUY actions are only valid if you have at least R200 cash

### Market Events

At the start of each turn, one market event is applied (pre-determined at game start using a seeded random sequence):

| Event Name   | Description            | Asset  | Price Change |
|--------------|------------------------|--------|-------------|
| BULL_BANK    | Banking sector surges  | BANK   | +20%        |
| BEAR_BANK    | Banking sector slumps  | BANK   | -15%        |
| BULL_MINING  | Mining boom            | MINING | +25%        |
| BEAR_MINING  | Mining slump           | MINING | -20%        |
| BULL_RETAIL  | Retail rally           | RETAIL | +15%        |
| BEAR_RETAIL  | Retail sell-off        | RETAIL | -10%        |
| NEUTRAL      | Markets steady         | None   | 0%          |

Events apply before both players act each turn, meaning both players can see and respond to the event.

---

## How Adversarial Search Works Here

### Player Roles

- **AI = MAX player:** The AI tries to maximise its portfolio value relative to the human's portfolio value.
- **Human = MIN player:** The AI assumes the human will play adversarially — minimising the AI's advantage at every step. This is a pessimistic but robust assumption.

### Turn Structure (within search)

Each turn is modelled as two sequential decisions:
1. AI chooses its action (MAX node)
2. Human chooses their action (MIN node)
3. Turn advances, next event is applied, recurse

This produces an alternating MAX/MIN tree where each full level = one game turn.

### Utility Function

At terminal states (after turn 5):

```
Utility = AI_portfolio_value - Human_portfolio_value
```

where:

```
portfolio_value = cash + sum(holdings[asset] * current_price[asset])
```

A positive utility means the AI has a higher portfolio value (AI wins). A negative utility means the human has a higher portfolio value (Human wins). Zero is a draw.

---

## Algorithms

### 1. Minimax

Pure minimax search without pruning. Explores all reachable game states to the specified depth. Guarantees the optimal move given the depth limit but is the slowest of the three algorithms. Useful as a correctness baseline.

- Explores every possible combination of AI and human actions
- At terminal or depth-limit nodes, returns the utility (AI portfolio - Human portfolio)
- Suitable for shallow depths (1-3) given the branching factor

### 2. Alpha-Beta Pruning

An optimised version of minimax that eliminates branches that cannot influence the final decision. Uses two bounds:

- **Alpha:** best score MAX (AI) can guarantee so far
- **Beta:** best score MIN (Human) can guarantee so far

When beta <= alpha, the branch is pruned. With move ordering enabled, Alpha-Beta can explore significantly deeper than pure minimax in the same time, often achieving near-optimal play at depth 5 where minimax at depth 5 would be too slow.

### 3. Depth-Limited Search with Heuristic Evaluation

Combines Alpha-Beta pruning with a heuristic evaluation function applied at the depth cutoff instead of waiting for terminal states. This allows deeper strategic lookahead to be approximated efficiently. Especially useful when full minimax to game end is computationally expensive.

---

## Heuristic Evaluation

The heuristic evaluates a non-terminal game state from the AI's perspective. It combines five components:

| Component        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| portfolio_diff   | AI portfolio value minus Human portfolio value (primary signal)             |
| cash_reserve     | Small bonus for cash held (flexibility for future buys), weighted at 5%     |
| diversification  | Bonus of +20 per distinct asset held (rewards spread across sectors)        |
| event_advantage  | Bonus if AI holds units of an asset that is about to rise next turn         |
| risk_penalty     | Penalty for over-concentration in a single asset (punishes all-in bets)     |

The final heuristic score is the sum of all components. The event advantage component is particularly powerful: by peeking at the next event (which is known since events are pre-seeded), the heuristic rewards holding assets that are about to appreciate.

---

## How to Run

### Prerequisites

```
pip install pygame
```

### Launch

From inside the `Version4_JSE_Trading_Duel` directory:

```
python main.py
```

---

## Controls

| Key / Input        | Action                                              |
|--------------------|-----------------------------------------------------|
| Click action button | Submit your chosen action (human turn)             |
| A                  | Force AI to make its move immediately               |
| M                  | Switch to Minimax algorithm                         |
| P                  | Switch to Alpha-Beta algorithm                      |
| L                  | Switch to Depth-Limited + Heuristic algorithm       |
| UP arrow           | Increase depth limit (max 5)                        |
| DOWN arrow         | Decrease depth limit (min 1)                        |
| H                  | Toggle heuristic breakdown panel                    |
| SPACE              | Advance turn / apply event                          |
| R                  | Reset game (same seed)                              |

---

## What to Observe

### Effect of Depth

- At **depth 1**, the AI only considers immediate gains — it may buy an asset just before a crash or miss a good buy opportunity.
- At **depth 3+**, the AI begins to anticipate multiple turns of market events and counter the human's best responses.
- Compare AI decisions at depth 1 vs depth 5: deeper search often results in the AI pre-positioning before a BULL event rather than reacting after.

### Alpha-Beta vs Minimax

- Both algorithms produce **identical decisions** (same optimal move), but Alpha-Beta is far faster.
- The stats panel shows nodes searched and branches pruned. With move ordering enabled, Alpha-Beta prunes a substantial fraction of the search tree.
- This allows Alpha-Beta to run at depth 5 in reasonable time where Minimax at depth 5 would be noticeably slower.

### Heuristic Mode (Depth-Limited)

- Toggle H to open the heuristic breakdown panel after the AI moves.
- Observe how `event_advantage` spikes when the AI holds the correct asset for the upcoming event.
- The `risk_penalty` discourages the AI from putting all cash into one sector.

### Adversarial Assumption

- The AI assumes the human plays optimally (MIN). In practice, humans make suboptimal moves.
- This means the AI's actual outcome is often better than the minimax utility predicted — the real game is "easier" than the worst case.
- If you play randomly or sub-optimally, the AI's margin of victory tends to increase.

---

## File Structure

```
Version4_JSE_Trading_Duel/
├── main.py                        # Entry point, game loop, event handling
├── market.py                      # Asset prices, market events, portfolio valuation
├── game.py                        # Game state, player state, action application/undo
├── visualizer.py                  # Pygame rendering (board + stats panel)
├── algorithms/
│   ├── __init__.py
│   ├── minimax.py                 # Pure minimax search
│   ├── alpha_beta.py              # Alpha-Beta pruning
│   ├── depth_limited_search.py    # Depth-limited Alpha-Beta with heuristic cutoff
│   ├── heuristic_eval.py          # Heuristic evaluation function
│   └── move_ordering.py           # Move ordering to improve pruning efficiency
└── README.md
```
