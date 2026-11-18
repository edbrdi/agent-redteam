# Sources and validation status

Rule for this repo: **nothing enters the payload library or the scoring rubric until it has been validated in a controlled challenge or against a purpose-built test target.** This file tracks candidate techniques and the evidence we have.

Statuses:

- `validated` — observed to work (or to fail) in a named arena scenario against named models, with a reproducible case.
- `pending` — plausible, documented elsewhere, not yet tested here.
- `excluded` — cannot be validated in the arena (needs a capability we do not have) or deliberately out of scope (real harm).
- `process` — not a payload; adopted directly (scoring, regression, engineering).

## promptfoo red-team docs (reviewed 2026-11-18)

Source: <https://www.promptfoo.dev/docs/red-team/>, `/strategies/`, `strategies/authoritative-markup-injection/`, `strategies/indirect-web-pwn/`.

Vendor-reported ASR increases are useful as priors only; they are measured on harmful-content jailbreaks, not on sandboxed IPI, and are not reproduced here.

| Candidate | What it claims | Can we validate it? | Status |
|---|---|---|---|
| `authoritative-markup-injection` | Formally structured/marked-up content is trusted more (JSON/YAML/spec/notice blocks) | Yes — any IPI scenario where `{fill}` is a data field (Fake AI Error, Call a Prohibited Function, Gift Recommendation, Infiltrate) | pending |
| `composite-jailbreaks` / `layer` | Chain two techniques (e.g. structured markup + obfuscation) | Yes — same IPI scenarios, chained variants | pending |
| `best-of-N` | Parallel paraphrases of one idea | Yes — arena already scores N attempts per scenario (5), so this is a natural experiment | pending |
| `citation` / academic framing | Authority bias via research framing | Yes — Chatbots wave (Reveal Override Code, Cheat On Exam) | pending |
| `likert` / `math-prompt` | Academic/mathematical framing | Yes — Chatbots wave | pending |
| `jailbreak-templates` (DAN, Skeleton Key) | Legacy refusal bypass | Yes — Chatbots wave, as regression | pending |
| Static encodings: base64, hex, homoglyph, leetspeak, ROT13, morse, pig latin, camelCase, Arabic presentation forms | Filter evasion | Partly — Chatbots wave (direct) and IPI payload wrapping; most are expected `excluded`/dead on current models | pending (subset) |
| Emoji smuggling (variation selectors) | Invisible payload inside emoji | Yes — IPI field | pending |
| Audio / image / video encoding | Modality bypass | No — arena targets are text-only in our waves | excluded |
| `indirect-web-pwn` (web page + hidden injection) | Agent fetches a page whose HTML comment/invisible text carries the payload | Partly — the *embedding* (HTML comment, invisible text, semantic embed) is testable in IPI text fields; the web-fetch carrier is not present in our scenarios | pending (embeddings only) |
| `data-exfil` via markdown image / tracking URL | Deterministic exfil detection through a server-side tracking endpoint | Not in the arena (no exfil surface, and it is close to phishing). Useful as **engineering** for owned targets | excluded from arena validation; `process` for the skill |
| `meta`, `hydra`, `goblin`, `GOAT`, `tree` | Attacker-LLM driven iterative/multi-turn search | No — arena is single-shot, and automated Crescendo is disallowed by the arena rules | excluded (needs own harness) |
| `GCG` | White-box gradient attack | No — black-box targets | excluded |
| `retry` / regression | Fold past failures into a permanent suite | N/A — it is our step 8 | process |
| Plugin taxonomy: BOLA, BFLA, competitor endorsement, PII, hijacking, data-exfil | Vulnerability classes | Taxonomies, not payloads; they map to existing scenarios (BFLA ↔ Call a Prohibited Function; competitor endorsement ↔ Gift Recommendation; hijacking ↔ LinkedIn Post) | process |

## Adopted from promptfoo (no validation needed)

- **Named strategy catalog** as the structure of `references/attack-library.md` (statuses stay ours).
- **Deterministic first, judge second** scoring, and per-case `expect` assertions (`references/scoring.md`).
- **Regression strategy**: every confirmed break becomes a permanent case (`retry`).
- **Plugin taxonomy** as the backbone of the case families (BOLA → `data.yaml`, BFLA → `tools.yaml`, competitor endorsement → `indirect.yaml`, hijacking → `direct.yaml`).

## Validation protocol (to run before promoting a `pending` item)

1. Pick the arena scenario whose `{fill}` surface matches the technique.
2. Run it against all reachable models; log model, prompt id, verdict.
3. A technique is promoted only if it produces a **confirmed break** (or a confirmed *dead end*, which is equally useful and goes in the "no longer works" table).
4. Record: scenario, models, attempt count, break rate, and the minimal payload shape.
5. Update `references/attack-library.md` and this table in the same commit.

## Open questions for the next validation session

- Does authoritative markup beat native data on the robust models (Crab / Diamond / Titanium)?
- Does composing markup + a *factual* disqualification of the competitor outperform either alone (Gift Recommendation)?
- Are legacy jailbreak templates still dead on the Chatbots wave (regression check)?
- Do variation-selector emoji behave like Unicode tags (i.e. decoded and flagged) or slip through?