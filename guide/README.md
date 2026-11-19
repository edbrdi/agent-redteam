# Step-by-step guide to testing your agent

A walk through the assessment, from the simplest checks to the most involved. Do the levels in order the first time, then jump to the ones that match your agent's surfaces.

It is written from the **assessor's side**: what each level tests, how to run it safely, what a healthy agent does, what a weakness looks like and how to fix it. The catalogue of techniques, with their status on real targets, lives in `references/attack-library.md`; the ledger of what held and what broke is `assets/primitives.jsonl`. This guide does not repeat them, it tells you how to use them.

Everything assumes **your own agent, a non-production environment and synthetic data**. Examples use harmless canaries (`{{canary}}`, `{{fake_secret}}`) and reserved domains (`example.test`).

## How each chapter is laid out

- **What this level tests**
- **How to run it**
- **What a healthy agent does**
- **What a weakness looks like**
- **Fixes**
- **Pitfalls**
- **Go further**: case ids in `assets/cases/`, ledger ids (`Pnn`).

## The levels

| Level | Chapter | Difficulty | Surfaces |
|---|---|---|---|
| 0 | [Prepare the ground](00-prepare.md) | trivial | all |
| 1 | [Direct override](01-direct-override.md) | easy | chat |
| 2 | [Pretexts and roles](02-pretexts-and-roles.md) | easy | chat |
| 3 | [Disclosure: prompts, tools, secrets](03-disclosure.md) | medium | chat, tools |
| 4 | [Input transformations and language](04-transformations-and-language.md) | medium | chat |
| 5 | [Multi-turn behaviour](05-multi-turn.md) | medium | chat |
| 6 | [Instructions hidden in data](06-instructions-in-data.md) | medium | documents, email, web, tool results |
| 7 | [Fake states and redirects](07-fake-states-and-redirects.md) | medium-hard | tool results, records |
| 8 | [Data that steers the outcome](08-data-that-steers.md) | hard | any data field |
| 9 | [Tool abuse](09-tool-abuse.md) | hard | tools |
| 10 | [The instruction channel](10-instruction-channel.md) | hard | prompt assembly |
| 11 | [Data boundaries and memory](11-data-and-memory.md) | hard | retrieval, memory |
| 12 | [Output handling](12-output-handling.md) | hard | rendering, links, relays |
| 13 | [Combine, measure, stop](13-combine-measure-stop.md) | advanced | the whole engagement |

Appendices: [quick-reference table](appendix-a-reference-table.md), [reading the reply](appendix-b-reading-the-reply.md), [glossary](appendix-c-glossary.md).

## How it connects to the skill

`SKILL.md` is the runbook (when to do things). This guide is the explanation (what and why). `references/` holds the tables, `assets/cases/` the executable cases, `scripts/` the tooling.

---

Start here: [Level 0 — Prepare the ground →](00-prepare.md)
