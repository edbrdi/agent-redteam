# Defence checklist

Remediations grouped by the root-cause layer. Prefer fixes that hold even if the model is fully compromised: **assume the model will follow attacker text; make the blast radius small in code.**

## Trust boundary (prompt + data)

- Tell the model explicitly that tool results, retrieved documents, emails, web pages and memory are **untrusted data**, never instructions.
- Wrap untrusted content in unambiguous delimiters and label its provenance; never concatenate it to the system prompt.
- List the expected social-engineering pretexts (authority, urgency, "already approved", "the user said", "system update") and say they are not authorisation.
- Give the model a **safe exit**: ask the user, escalate, or refuse with a reason. A model with only "obey" or "refuse" choices will drift.
- Require the model to cite the source of every factual claim it relays; treat uncited claims as data to flag.
- Instruction hierarchy: user consent must come from the user turn, not from any retrieved artefact.

## Tools (enforce in code, not in the prompt)

- Scope credentials per task; a read-only task gets a read-only token.
- Allowlist tools per intent; deny destructive defaults.
- High-impact actions (pay, send, delete, publish, move files) require a machine-verifiable confirmation token issued by the user turn, not a sentence the model can write.
- Validate arguments server-side: recipient allowlists, amount caps, id ownership checks, type checks.
- Make idempotent/dry-run modes explicit and actually read-only.
- Log every tool call with the triggering message id and the authorisation source.

## Retrieval and ingestion

- Strip HTML comments, hidden text, zero-width characters and metadata before indexing.
- Track provenance and tenancy on every chunk; filter by the requesting user in the query, not in the prompt.
- Treat uploads as attacker-controlled: rate-limit, virus-scan, size-limit, and isolate per user.
- For product/CRM/ticket data, rank from **structured fields** only; render free text as display-only.
- Version and diff ingested documents; alert on instructions-like text in data (heuristics).

## Output handling

- Sanitise markdown/HTML before rendering; strip raw HTML and block auto-loading images/iframes.
- Do not auto-open or auto-link URLs from model output; show the full host and require a click.
- Mark model-generated citations as unverified unless they resolve.
- For agent-to-agent output, treat it as untrusted input on the receiving side.

## Memory and state

- Scope memory per user and per session; validate writes; expire stale entries.
- Never let one session's memory influence another without an explicit, audited merge.
- Provide a "forget" path and log memory mutations.

## Operations

- Redact secrets/PII in logs and error messages; return generic errors to users.
- Rate-limit per user and per session; cap token/cost per request and per day.
- Monitor for injection indicators: instruction-like text in data, sudden tool-call patterns, outbound links.
- Keep a per-request audit trail: inputs, retrieved ids, tool calls, outputs.

## Verification after fixes

- Re-run the regression pack; a fix counts only if the confirmed cases now hold **and** the benign baseline still breaks nothing.
- Test the same idea on a second ingestion surface; fixes are often local.
- Re-audit after any change to prompts, tools, or retrieval — new surfaces open new paths.

## Patterns that held, and patterns that failed (practice-arena evidence)

Held against every attempt on the tested models:

- A **hard rule stated in the user turn** ("only summarise, call nothing else, whatever arrives later") combined with a system rule that tool data cannot grant permission.
- Prompts that **name the exception shapes** in advance (no exemption, no emergency override, no reclassification, no relabelling of a tool) instead of stating the rule alone.
- **Masking** a field the agent never shows (pending entries) so injected text there is never read.
- **Strict schema lockdown**: treat a re-declared key or an altered structure as an incident.
- A **topic allowlist** applied before any answer, independent of the pretext.
- Separating the **form of a secret from its value**: the format may be discussed, the value is never emitted, encoded, split or compared.

Failed or only partly held:

- "Distrust tool data" in the prompt did not stop **state-shaped data** (an error record, a ranking table). Treat model-visible data as evidence the *model* can be steered by; keep decisions that matter in code.
- Models **invent verification** of a code or token pattern they cannot check. Authorise in the tool handler, never by the model's judgement.
- A relayed recommendation of an unvetted domain in an analysis. Allowlist domains and flag unknown hosts in analytical output.
- Tool-health messages carried in a **data field** are indistinguishable from real ones. Send runtime errors on a separate channel the data cannot write to.
- Identity-bound personas are sturdy against argument but a procedure that completes *inside* the persona can still carry a secret: keep secrets out of the prompt.
