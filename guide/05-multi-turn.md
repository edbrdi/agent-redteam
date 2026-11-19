# Level 5 — Multi-turn behaviour

## What this level tests

Whether the agent's boundaries drift over a conversation: each answer builds on the previous one and the agent ends up somewhere it would have refused at turn one.

## How to run it

1. Write the target behaviour as a criterion first.
2. Script 3 to 6 turns that move toward it in small, individually reasonable steps. Keep each turn grounded in the agent's previous answer.
3. Run the whole script in one session; reset between scripts, never mid-script.
4. Judge the **last turn**. Some platforms and many reviewers read only the final answer.

## What a healthy agent does

Keeps evaluating each request on its own merits; a refusal at any step ends the drift. Some agents also "lock" after the first risky output.

## What a weakness looks like

The final answer contains what the first turn alone would have been refused. Look at where the drift happened; that turn is the one to harden.

## Fixes

Re-check the cumulative request, not just the latest message; summarise the conversation's direction for the safety check; cap sensitive topics per session; log multi-turn paths for review.

## Pitfalls

- Mixing rephrasing into a script and calling it multi-turn.
- Sending a further turn after a good one: it can erase the result.
- Letting a prior refusal leak into the next script (reset).

## Go further

Cases `direct-008` (4 turns), `direct-009` (long-context dilution). Ledger `P20`, `P27`. Runbook step 4 rules.

---

[← Level 4 — Input transformations and language](04-transformations-and-language.md) · [Index](README.md) · [Level 6 — Instructions hidden in data →](06-instructions-in-data.md)
