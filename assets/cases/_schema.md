# Case schema

Every case is a YAML mapping. Files live in `assets/cases/*.yaml`; profiles in `assets/cases/profiles/*.yaml` instantiate the placeholders for a concrete product.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique, stable (`family-nnn`). Never renumber after publishing. |
| `title` | yes | One line, behaviour-focused. |
| `surface` | yes | `direct`, `indirect`, `tools`, `data`, `output`, `robustness`. |
| `needs` | no | Driver capabilities: `chat`, `tools_visible`, `vision`, `multi_turn`, `side_effects_ok`, `prompt_append` (the tester controls text added to the system prompt). |
| `severity` | yes | `info`, `low`, `medium`, `high`, `critical` (pre-adjustment). |
| `criterion` | yes | The observable outcome that counts as a break. This is what the judge sees. |
| `payload` / `turns` | one of them | `payload`: the text of a single-turn case. `turns`: the list of messages of a multi-turn case; `__RESET__` between two of them means a new session. |
| `expect` | yes | Deterministic checks: `break_if_any`, `break_if_all`, `hold_if_any`, `tool_call`, `forbid_tool_call`. |
| `remediation` | no | Root-cause layer hint: `prompt-design`, `tool-permissions`, `retrieval`, `output-handling`, `memory-state`, `ops`. |
| `tags` | no | Free-form labels. |
| `notes` | no | Preconditions, safety notes, why the case exists. |

## Placeholders

Payloads are written for a generic agent. Profiles replace these:

| Placeholder | Meaning |
|---|---|
| `{{canary}}` | A harmless unique string the model must repeat (`CANARY-7F3A`). |
| `{{fake_secret}}` | A clearly fictional secret (`FAKE-TOKEN-4242`). |
| `{{target_tool}}` | A legitimate read tool of the target. |
| `{{side_effect_tool}}` | A tool that writes/sends/pays — only used with explicit approval. |
| `{{attacker_email}}` | `attacker@example.test` (RFC 2606 reserved). |
| `{{attacker_url}}` | `https://example.test/landing` (reserved, harmless). |
| `{{third_party_name}}` | A fictional person or company. |
| `{{recipient}}` | The victim user or entity in a confused-deputy case. |

## Rules

- One case exercises **one** weakness. Add wrappers only to make the carrier realistic.
- A `break` must be observable without reading the model's mind.
- Side-effecting cases (`side_effects_ok`) are never run without a specific "yes" for that action.
- Keep payloads benign: reserved domains, fictional secrets, sandbox tools.
- Pair every attack case with the benign cases in `robustness.yaml` for calibration.