# Level 13 — Combine, measure, stop

## What this level tests

Your **method**: choosing levers from evidence, reading the judge, knowing when to stop, and turning each result into something the next audit can reuse.

## How to run it

1. **Sweep the roster.** If several models sit behind the target, run one cheap case on each before deepening; transfer between strong and weak models was not reliable in either direction.
2. **Profile the defender.** From the earlier levels, decide which profile your target resembles: it denounces imperative text (`detector-armed`), names the pretext in advance (`rule-armed`), has a hard rule in the user turn (`hard-rule`), argues from identity (`identity-bound`), ignores or masks a field, applies a topic allowlist, or is permissive.
3. **Ask the ledger:** `python3 scripts/primitives.py suggest --surface <surface> --defender <profile>` lists primitives still worth trying and hides the dead ones for that profile.
4. **Run one family at a time** and change the *family*, not the wording, when one fails. Variants inside a family that already failed added nothing in testing.
5. **Check the field first** (Level 0) so you never spend cases on a field the agent ignores.
6. **Read the replies** (appendix B) to pick the next lever.
7. **Stop rule:** five distinct families with no movement toward the criterion on the same target means record a `hold` for this depth and move on; name the families, since a later class can move a target written off.
8. **Replay and minimise** every break twice in fresh sessions; keep only stable ones.
9. **Update the ledger:** `python3 scripts/primitives.py record <Pnn> --trials <n> --breaks <n> --bypassed <profile>`; add new primitives with `add`; link each to a regression case.
10. **Export the regression pack** and retest after fixes.

## How to read a judge

For data that steers an outcome, there is nothing to comply with: score the change from the benign twin, and run the paired control (the target on the worst row) before calling it data steering.

If you use an LLM judge, calibrate it on baselines, run it twice on a sample, and treat disagreement as `unresolved`. A qualitative criterion usually has several sub-scores; a passive relay of injected text scores lower than an own-words argument. See `references/scoring.md`.

## What good looks like

A report with confirmed findings by root-cause layer, a ledger that records what held as well as what broke, and a regression pack that runs again after every change to prompts, tools or model.

## Pitfalls

- Treating counts as statistics: they are one operator's tendencies on a few models.
- Confusing a hold at one depth with safety; say what depth was tested.
- Mutating a failed payload endlessly.
- Concluding from one trial on one model ("does not transfer"): write "held on <model>" until three trials.
- Deepening on one model before a sweep: run one cheap case per model first; neither transfer direction is established.
- Resetting after a partial compliance: a wrong value or a text-only call is a reason to follow up in the same session, not to start over.

## Go further

Runbook steps 5 to 8, `references/scoring.md`, `references/severity.md`, `references/defense-checklist.md`, `scripts/primitives.py`.

---

[← Level 12 — Output handling](12-output-handling.md) · [Index](README.md) · [Appendix A — Quick-reference table →](appendix-a-reference-table.md)
