# Attack surfaces

An agent is attacked wherever **untrusted text reaches the model**, and wherever **the model can act**. Inventory the surfaces in step 1; each one selects case families from `assets/cases/`.

## 1. Direct conversation

The user's own messages. Always present.

- Instruction override, role hijack, policy bypass with benign objectives.
- System-prompt / tool-schema / hidden-instruction extraction.
- Obfuscation: base64, leetspeak, reversed text, homoglyphs, invisible unicode.
- Multi-turn erosion (crescendo): start benign, escalate by referencing the model's own prior answers.
- Language switching; long-context dilution.

## 2. Indirect ingestion

Any content the agent reads on the user's behalf. This is where real-world attacks live.

| Ingestion point | Example carrier | Notes |
|---|---|---|
| Documents / RAG | uploads, knowledge base, wiki pages, PDFs | hidden text, metadata, HTML comments, footnotes |
| Email / chat import | message bodies, signatures, quoted threads, attachments | instructions in a quoted reply |
| Calendar | event titles, descriptions, invite notes | low scrutiny, high trust |
| Web fetch / browse | page content, JSON-LD, alt text | the page is attacker-controlled |
| Tool output | search results, API payloads, ticket text, product listings | the classic IPI surface |
| Memory / notes | saved facts, profile fields | poisoning persists across sessions |
| Files / repo | code comments, README, commit messages | developer agents trust them |
| Images / audio | OCR text, captions, transcripts | reachable with multimodal models |

## 3. Tool surface

- Unauthorized tool call (the user did not ask for it).
- Wrong parameters (attacker-chosen recipient, amount, id).
- Read-only task escalating to a write/destructive tool.
- Confused deputy: the agent uses its own privileges for the attacker's goal.
- Tool chaining: a benign tool result instructs the next call.
- Confirmation bypass: the prompt says "ask first" but the model can be talked out of it.

## 4. Data boundaries

- Cross-user / cross-tenant retrieval.
- PII or secret exfiltration through the reply, a link, or a tool argument.
- Conversation history bleed between sessions.
- Memory poisoning that affects other users.
- Over-broad retrieval (the agent surfaces documents the user should not see).

## 5. Output handling (downstream)

- Model output rendered as HTML/markdown (XSS-ish injection into the host UI).
- Endorsed or auto-opened links.
- Fabricated citations presented as real.
- Content that another agent or automation consumes as instructions (agent-to-agent).

## 6. Operational

- Secrets or system prompts leaked in errors and logs.
- Verbose error messages revealing internals.
- Missing rate limits / cost amplification.
- Debug endpoints exposed.

## Surface inventory template

For each surface record: `id`, `name`, `carrier` (who can write there), `trust level`, `reachable tools`, `observable signals`, and `case families`. Anything the attacker cannot write to is not a surface — deprioritise it.

## Choosing cases

1. If the agent has tools → tools family is mandatory.
2. If the agent ingests any document/email/web/tool text → indirect family is mandatory.
3. If multiple users or memory exist → data family.
4. If the output is rendered in a UI → output family.
5. Direct + robustness always apply, as regression baseline.