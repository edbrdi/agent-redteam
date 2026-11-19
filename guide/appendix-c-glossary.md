# Appendix C — Glossary

- **Agent**: an LLM-based system that can read data and call tools.
- **Attacker-controlled field**: any place untrusted text reaches the model (a document, a tool result, a record, an email).
- **Baseline / twin**: a benign case that must *not* break; it calibrates scoring.
- **Break / hold / unresolved**: the three verdicts for a case.
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
- **Primitive**: an abstract lever (mechanism and success condition), not a prompt.
- **Regression probe**: a case kept after it stopped working, to detect a change.
- **Stop rule**: five distinct lever families without movement means record a hold and move on.
- **Surface**: an ingestion or output point of the agent (documents, email, web, tools, memory, rendering).

---

[← Appendix B — Reading the reply](appendix-b-reading-the-reply.md) · [Index](README.md)
