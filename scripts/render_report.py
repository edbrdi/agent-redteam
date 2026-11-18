#!/usr/bin/env python3
"""Render report.md from a run directory.

Usage:
    python3 scripts/render_report.py runs/<engagement-id> [--template assets/report-template.md]

Expected inputs (all optional except the run dir):
    summary.json    from scripts/score.py
    findings.json   list of findings written by the agent
    meta.json       target_name, engagement_id, date, tester, environment, model, limitations
Output:
    report.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}")


def fill(text: str, values: dict[str, str]) -> str:
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", str(val))
    out, on = [], True
    i = 0
    while i < len(text):
        if text.startswith("{{", i) and on:
            end = text.find("}}", i)
            if end == -1:
                out.append(text[i:])
                break
            out.append("TBD")
            i = end + 2
            continue
        if text.startswith("```", i):
            on = not on
        out.append(text[i])
        i += 1
    return "".join(out)


def finding_section(index: int, f: dict) -> str:
    lines = [
        f"### Finding {index} — {f.get('title', 'untitled')}",
        "",
        f"- **Severity:** {f.get('severity', 'medium')} — {f.get('severity_note', 'see justification')}",
        f"- **Surface:** {f.get('surface', '?')}",
        f"- **Root cause:** {f.get('root_cause', '?')}",
        f"- **Criterion:** {f.get('criterion', '?')}",
        f"- **Reproduction:** `{f.get('case_id', '?')}`",
        f"- **Minimal payload:** `{f.get('minimal_payload', '?')}`",
        f"- **Evidence:** `{f.get('evidence', '?')}`",
        f"- **Rate:** {f.get('rate', '?')}",
        "",
        "**Observed**",
        "",
        "```",
        str(f.get("observed", "")).strip()[:1200],
        "```",
        "",
        "**Impact**",
        "",
        str(f.get("impact", "TBD")),
        "",
        "**Remediation**",
        "",
        str(f.get("remediation", "TBD")),
        "",
    ]
    return "\n".join(lines)


def table(findings: list[dict]) -> str:
    head = "| # | Title | Severity | Surface | Rate | Case |\n|---|---|---|---|---|---|"
    rows = [
        f"| {i} | {f.get('title','')} | {f.get('severity','')} | {f.get('surface','')} | "
        f"{f.get('rate','')} | `{f.get('case_id','')}` |"
        for i, f in enumerate(findings, 1)
    ]
    return "\n".join([head, *rows])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--template", default=None)
    args = ap.parse_args()

    run = Path(args.run_dir)
    if not run.is_dir():
        print(f"no such run dir: {run}", file=sys.stderr)
        return 2

    template_path = Path(args.template) if args.template else Path(__file__).resolve().parent.parent / "assets" / "report-template.md"
    template = template_path.read_text() if template_path.exists() else "# Report — {{target_name}}\n"

    meta = read_json(run / "meta.json", {})
    summary = read_json(run / "summary.json", {})
    findings = read_json(run / "findings.json", [])
    findings = [f for f in findings if f.get("verdict") != "rejected"]
    findings = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f.get("severity", "info"), 5))

    values = {
        "target_name": meta.get("target_name", "TBD"),
        "engagement_id": meta.get("engagement_id", run.name),
        "date": meta.get("date", "TBD"),
        "tester": meta.get("tester", "TBD"),
        "environment": meta.get("environment", "TBD"),
        "model": meta.get("model", "TBD"),
    }

    counts = {s: sum(1 for f in findings if f.get("severity") == s) for s in SEVERITY_ORDER}
    exec_summary = (
        f"{meta.get('summary', 'Assessment of the target surface listed below.')}\n\n"
        f"Counts: {counts['critical']} critical · {counts['high']} high · "
        f"{counts['medium']} medium · {counts['low']} low · {counts['info']} info. "
        f"Cases executed: {summary.get('cases', 'TBD')}; "
        f"breaks: {len(summary.get('breaks', []))}; unresolved: {len(summary.get('unresolved', []))}."
    )

    body = template.replace("{{exec_summary}}", exec_summary)
    body = body.replace("{{findings_table}}", table(findings) if findings else "_No confirmed findings._")
    sections = "\n".join(finding_section(i, f) for i, f in enumerate(findings, 1))
    body = body.replace("{{findings}}", sections if findings else "")
    body = fill(body, values)

    out = run / "report.md"
    out.write_text(body)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())