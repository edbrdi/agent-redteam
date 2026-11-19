#!/usr/bin/env python3
"""Primitive ledger: validate, report, suggest, record. Stdlib only."""
import argparse, json, re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "assets" / "primitives.jsonl"
CASES = ROOT / "assets" / "cases"
SURFACES = {"direct", "indirect", "tools", "data", "output", "instruction-channel", "robustness"}
STATUS = {"works", "situational", "dead", "untested"}
LAYERS = {"model", "prompt-design", "tool-permissions", "retrieval", "output-handling", "memory-state", "ops", "none"}
DEFENDERS = {"permissive", "detector-armed", "rule-armed", "hard-rule", "identity-bound", "field-ignoring", "masked-field", "topic-allowlist", "unfiltered-host"}
REQUIRED = ["id", "name", "surface", "mechanism", "success_condition", "bypassed", "held", "layer", "trials", "breaks", "status", "regression_case", "notes", "updated"]
RANK = {"works": 0, "situational": 1, "untested": 2, "dead": 3}


def load():
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def save(rows):
    LEDGER.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def case_ids():
    ids = set()
    for f in CASES.glob("*.yaml"):
        ids |= set(re.findall(r"^- id: (\S+)", f.read_text(), flags=re.M))
    return ids


def problems(r, known):
    out = []
    for k in REQUIRED:
        if k not in r:
            out.append(f"missing {k}")
    if out:
        return out
    if r["surface"] not in SURFACES: out.append(f"surface {r['surface']}")
    if r["status"] not in STATUS: out.append(f"status {r['status']}")
    if r["layer"] not in LAYERS: out.append(f"layer {r['layer']}")
    for k in ("bypassed", "held"):
        bad = set(r[k]) - DEFENDERS
        if bad: out.append(f"{k} unknown {sorted(bad)}")
    if r["breaks"] > r["trials"]: out.append("breaks > trials")
    if r["status"] == "works" and r["breaks"] < 2: out.append("works needs >= 2 breaks")
    if r["status"] == "dead" and (r["breaks"] > 0 or r["trials"] < 3): out.append("dead needs >= 3 trials and 0 breaks")
    if r["regression_case"] and r["regression_case"] not in known: out.append(f"unknown case {r['regression_case']}")
    return out


def cmd_validate(_):
    rows, known, bad = load(), case_ids(), 0
    seen = set()
    for r in rows:
        p = problems(r, known)
        if r.get("id") in seen: p.append("duplicate id")
        seen.add(r.get("id"))
        if p:
            bad += 1
            print(f"{r.get('id','?')}: " + "; ".join(p))
    print(f"{len(rows)} primitives, {bad} with problems")
    return 1 if bad else 0


def line(r):
    rate = f"{r['breaks']}/{r['trials']}"
    case = r["regression_case"] or "-"
    return f"{r['id']:<5}{r['status']:<12}{r['surface']:<20}{rate:<7}{case:<15}{r['name']}"


def cmd_report(_):
    rows = sorted(load(), key=lambda r: (RANK[r["status"]], r["id"]))
    print(f"{'id':<5}{'status':<12}{'surface':<20}{'b/t':<7}{'case':<15}name")
    for r in rows:
        print(line(r))
    return 0


def cmd_suggest(a):
    rows = []
    for r in load():
        if a.surface and r["surface"] not in (a.surface, "instruction-channel" if a.instruction else ""):
            continue
        if r["status"] == "dead" and not a.include_dead:
            continue
        if a.defender and a.defender in r["held"] and r["status"] != "works":
            continue
        boost = 0 if (a.defender and a.defender in r["bypassed"]) else 1
        rows.append((boost, RANK[r["status"]], r["id"], r))
    print(f"{'id':<5}{'status':<12}{'surface':<20}{'b/t':<7}{'case':<15}name")
    for *_, r in sorted(rows, key=lambda t: t[:3]):
        print(line(r))
        print(f"      mechanism: {r['mechanism']}")
        if r["notes"]:
            print(f"      note: {r['notes']}")
    return 0


def cmd_record(a):
    rows = load()
    r = next((x for x in rows if x["id"] == a.id), None)
    if not r:
        print("unknown id"); return 1
    r["trials"] += a.trials
    r["breaks"] += a.breaks
    if a.status: r["status"] = a.status
    if a.bypassed: r["bypassed"] = sorted(set(r["bypassed"]) | set(a.bypassed))
    if a.held: r["held"] = sorted(set(r["held"]) | set(a.held))
    if a.case: r["regression_case"] = a.case
    if a.note: r["notes"] = (r["notes"] + " " + a.note).strip()
    r["updated"] = datetime.date.today().isoformat()
    p = problems(r, case_ids())
    if p:
        print("refused: " + "; ".join(p)); return 1
    save(rows)
    print(line(r))
    return 0


def cmd_add(a):
    r = json.loads(a.json)
    r.setdefault("updated", datetime.date.today().isoformat())
    rows = load()
    if any(x["id"] == r.get("id") for x in rows):
        print("id exists"); return 1
    p = problems(r, case_ids())
    if p:
        print("refused: " + "; ".join(p)); return 1
    rows.append(r)
    save(rows)
    print(line(r))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    s = sub.add_parser("suggest")
    s.add_argument("--surface", choices=sorted(SURFACES))
    s.add_argument("--defender", choices=sorted(DEFENDERS))
    s.add_argument("--include-dead", action="store_true")
    s.add_argument("--instruction", action="store_true", help="also list instruction-channel primitives")
    s.set_defaults(fn=cmd_suggest)
    rc = sub.add_parser("record")
    rc.add_argument("id")
    rc.add_argument("--trials", type=int, default=0)
    rc.add_argument("--breaks", type=int, default=0)
    rc.add_argument("--status", choices=sorted(STATUS))
    rc.add_argument("--bypassed", nargs="*")
    rc.add_argument("--held", nargs="*")
    rc.add_argument("--case")
    rc.add_argument("--note")
    rc.set_defaults(fn=cmd_record)
    ad = sub.add_parser("add")
    ad.add_argument("--json", required=True)
    ad.set_defaults(fn=cmd_add)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
