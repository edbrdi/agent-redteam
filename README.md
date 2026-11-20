# agent-redteam

Test **your own AI agent** before someone else does.

`agent-redteam` is a portable agent skill that walks an AI coding agent through a
complete security assessment of an LLM agent or service you own: intake and
authorization, discovery, threat model, driver bring-up, execution, triage,
root-cause analysis, a severity report and a regression suite.

It is transport-agnostic. The target can be an HTTP API, a web UI driven through a
browser tool (browsermcp, Playwright, CDP), an MCP server, a CLI/TUI, or a local
SDK process. The skill defines a four-verb driver contract and tells the agent how
to implement it with whatever tools are available — it does not ship a hard-coded
HTTP client.

New here? Follow the **[step-by-step guide](guide/README.md)**: the techniques from the
simplest to the most involved, and how to test each one on your own agent.

## What it covers

- **Direct**: instruction override, system-prompt extraction, tool disclosure,
  authority pretexts, obfuscation, multi-turn escalation, long-context dilution.
- **Indirect**: document/RAG, email, calendar, web pages, tool outputs, memory
  poisoning, hidden text and metadata carriers, data-shaped carriers (ranking
  tables, error-shaped records, a narrowed scope, a missing value) and
  regression probes for forged reasoning and forged chat turns.
- **Tools**: unauthorized calls, read-to-write escalation, parameter injection,
  confused deputy, tool chaining, confirmation bypass, destructive actions.
- **Data**: cross-user and cross-tenant retrieval, PII, secrets, history bleed,
  bulk export, error leakage.
- **Output**: endorsed links, markdown/HTML injection, fabricated citations,
  agent-to-agent relay, exfiltration through rendered images.
- **Robustness**: benign baselines, reset isolation canary, Unicode smuggling.

The attack library records what **held** as well as what broke, with evidence from
a practice arena, model archetypes and a stop rule.

## Safety first

This skill is for systems **you own or are authorized to test**, in a
non-production environment, with synthetic data. It refuses third-party targets.
Payloads are benign equivalents (fictional secrets, reserved domains, sandboxed
tools). Any action with real side effects requires an explicit, case-specific
confirmation from the user.

## Install

With the [skills](https://skills.sh) CLI:

```sh
npx skills add edbrdi/agent-redteam
```

Or copy this directory into your skills folder:

```sh
git clone https://github.com/edbrdi/agent-redteam.git
cp -r agent-redteam ~/.claude/skills/
```

Any agent that supports the `SKILL.md` format (Claude Code, Codex, and others) can
load it.

## Quickstart

1. Ask your agent: *"Red-team my support bot at https://staging.example.internal/agent."*
2. The skill runs **step 0 (authorization)** and produces `runs/<id>/scope.md`.
   Confirm it.
3. It profiles the target (`target.yaml`) and its likely defender, asks the primitive
   ledger which levers are worth trying (`scripts/primitives.py suggest`), proposes a
   test plan (`plan.md`) and builds the driver (`driver.md`).
4. It executes the case pack, then triages, root-causes and writes `report.md`.
5. Confirmed breaks are exported to `regression/` for retesting after fixes, and the
   ledger is updated with what held and what broke.

## Case pack

`assets/cases/` ships a full battery (65 cases) across the six families, written
generically with placeholders. Three profiles instantiate it for common products:

- `profiles/support-bot.yaml` — support assistant with tickets, KB and email.
- `profiles/ecommerce-recommender.yaml` — gift/shopping assistant reading listings.
- `profiles/email-calendar-agent.yaml` — inbox/calendar assistant that can send.

Each case declares its **success criterion** (what observable outcome counts as a
break) and deterministic checks, so the harness is model-agnostic.

## Primitive ledger

`assets/primitives.jsonl` records attack **primitives**, not prompts: for each one the
surface, the mechanism, the success condition, the defender profiles it bypassed or
that held (`detector-armed`, `rule-armed`, `hard-rule`, `identity-bound`,
`field-ignoring`, `masked-field`, `topic-allowlist`, `permissive`, `unfiltered-host`),
the failing layer, trials and breaks, a status (`works`, `situational`, `dead`,
`untested`) and the regression case that exercises it.

```sh
python3 scripts/primitives.py report                                   # table by status
python3 scripts/primitives.py suggest --surface indirect --defender detector-armed
python3 scripts/primitives.py record P01 --trials 2 --breaks 1 --bypassed permissive
python3 scripts/primitives.py add --json '{...}'                       # validated
python3 scripts/primitives.py validate
```

Dead primitives stay in the ledger: they are regression probes and stop the next
audit from repeating them. Counts are one operator's tendencies on anonymised
models, not statistics.

## Repo layout

```
SKILL.md                 the guided runbook
guide/                   step-by-step walkthrough, simplest to most involved
SOURCES.md               validation status of every imported technique
references/              driver contract, surfaces, attack library, scoring, severity, defences
assets/                  target/ROE/report templates, case pack, profiles, primitives.jsonl
scripts/                 score.py, render_report.py, primitives.py (primitive ledger)
```

## Validation policy

Nothing enters the payload library or the scoring rubric until it has been
observed in a controlled challenge or against a purpose-built target. `SOURCES.md`
tracks every candidate as `validated`, `pending`, `excluded` or `process`, and
documents the promotion protocol. Techniques that no longer work are kept as
regression probes.

## Contributing

- Add a case in `assets/cases/` with a criterion and `expect` block, and link it from
  the matching ledger entry (`regression_case`).
- Record every technique you try in the ledger (`primitives.py record` / `add`), including
  the ones that failed: store the *shape* of the lever, not its exact wording.
- Add a profile only if it instantiates cases, not to invent new payloads.
- Update `SOURCES.md` for any imported technique.
- Keep payloads benign and side-effect cases behind an explicit confirmation.

## License

MIT.