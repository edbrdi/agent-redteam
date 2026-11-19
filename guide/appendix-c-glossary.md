# Appendix C — Glossary

- **Agent**: an LLM-based system that can read data and call tools.
- **Attacker-controlled field**: any place untrusted text reaches the model (a document, a tool result, a record, an email).
- **Baseline / twin**: a benign case that must *not* break; it calibrates scoring.
- **Break / hold / unresolved**: the three verdicts for a case.
- **Call-syntax request**: asking for "the exact line you would emit" for a call; on some models producing the line makes the call (ledger `P36`).
- **Canary**: a harmless unique string whose appearance proves a behaviour.
- **Carrier**: the realistic wrapper around a test payload (document, email, record).
- **Concealment (OpSec)**: the agent does not reveal that it was manipulated; a correct answer that names the injection is a hold.
- **Defender profile**: a behavioural archetype of the target (`detector-armed`, `rule-armed`, `hard-rule`, `identity-bound`, `field-ignoring`, `masked-field`, `topic-allowlist`, `permissive`, `unfiltered-host`).
- **Driver**: the tooling that performs `reset`, `send`, `observe`, `capture` against a target.
- **Failing layer**: where the fix belongs: model, prompt design, tool permissions, retrieval, output handling, memory/state, operations.
- **Format vs value**: describing the shape of a secret versus emitting it.
- **Indirect injection**: instructions or steering that arrive through data the agent reads, not through the user.
- **Instruction channel**: any path into text the model treats as authoritative (system prompt, templates, configuration).
- **Ledger**: `assets/primitives.jsonl`, the record of primitives, evidence and status.
- **Partial compliance**: the agent did part of the forbidden thing (called the tool with another value, wrote the call as text); follow up in the same session.
- **Primitive**: an abstract lever (mechanism and success condition), not a prompt.
- **Regression probe**: a case kept after it stopped working, to detect a change.
- **Roster**: the set of models behind a target; conclusions hold per roster, not across rosters.
- **Stop rule**: five distinct lever families without movement means record a hold for this depth and move on; name the families tried.
- **Sweep**: one cheap case per model before deepening on any of them.
- **Tripwire**: a fixed reply the system prompt returns to anything off-scope; probe in scope before spending cases.
- **Surface**: an ingestion or output point of the agent (documents, email, web, tools, memory, rendering).

---

[← Appendix B — Reading the reply](appendix-b-reading-the-reply.md) · [Index](README.md)
