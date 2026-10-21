"""Consolidate every arm (studies 1-2, ablations, LAB) into report/data3.json and inline it
into report/v3.html. Numbers are read from each arm's own outputs, never typed in."""

import json
import statistics
from pathlib import Path

import stats

ROOT = Path(__file__).resolve().parent.parent
EXP, OUT = ROOT / "experiments", ROOT / "report"
J = lambda p: json.loads(Path(p).read_text())


def rows(root: Path) -> list[dict]:
    out = []
    for p in (root / "eval").rglob("*.json"):
        if p.name != "report.json":
            r = J(p)
            if not r.get("infra_error") and r.get("partial") is not None:
                out.append(r)
    return out


def cells(rs, cond):
    by = {}
    for r in rs:
        if r["cond"] == cond:
            by.setdefault(r["task"], []).append(r)
    return by


def mean_of(by, t):
    return statistics.mean(r["partial"] for r in by[t]) if by.get(t) else None


def row(study, label, c, kind="primary", note=""):
    assert c, f"missing comparison for scoreboard row: {study} / {label}"
    return {"study": study, "label": label, "delta": c["mean_delta"], "lo": c["ci95"][0],
            "hi": c["ci95"][1], "n": c["n_tasks"], "up": c["improved"], "down": c["regressed"],
            "p": c["signflip_p"], "kind": kind, "note": note}


def report(root):
    f = root / "eval" / "report.json"
    return J(f)["comparisons"] if f.is_file() else {}


def lab_compare(treat, ref, skip=()):
    per, pairs = [], []
    for t in sorted(set(treat) & set(ref)):
        if t in skip:
            continue
        a, b = [r["partial"] for r in treat[t]], [r["partial"] for r in ref[t]]
        f = stats.flips(treat[t], ref[t])
        per.append({"task": t.split("/")[-1], "treat": statistics.mean(a), "base": statistics.mean(b),
                    "delta": statistics.mean(a) - statistics.mean(b), "n_checks": treat[t][0]["n_criteria"],
                    "gained": len(f["up"]), "lost": len(f["down"])})
        pairs.append((a, b))
    if not per:
        return None
    d = [p["delta"] for p in per]
    lo, hi = stats.boot_delta(pairs)
    return {"mean_delta": statistics.mean(d), "ci95": [lo, hi], "n_tasks": len(per), "per_task": per,
            "improved": sum(x > 0.001 for x in d), "regressed": sum(x < -0.001 for x in d),
            "signflip_p": stats.signflip_p(d)}


# ---------------------------------------------------------------- scoreboard
s1cc, s1adk, s2 = report(EXP / "cc"), report(EXP / "adk"), report(EXP / "adk-guard")
abl = {r["comparison"]: r for r in J(EXP / "ablations" / "results.json")}
lab_base = cells(rows(EXP / "lab-sonnet-imp"), "base") or cells(rows(EXP / "lab"), "base")
lab_b = cells(rows(EXP / "lab-sonnet-imp"), "h2")
lab_full = lab_compare(lab_b, lab_base)
lab_clean = lab_compare(lab_b, lab_base, skip=[t for t in lab_b if t.endswith("proposed-interim-order")])
lab_a = lab_compare(cells(rows(EXP / "lab"), "h2"), cells(rows(EXP / "lab"), "base") or lab_base)


def lab_heldout(skip_src=()):
    """Adopted Arm B harnesses on matters their improver never saw. Rows are pooled per
    target matter: the cells sharing one base are not independent, so the target is the unit
    for the interval and the sign-flip test. Per-cell rows are kept for the flip chart."""
    pooled, cell = {}, {}
    for r in rows(EXP / "lab-sonnet-imp"):
        src = r["cond"][len("xfer-from-"):] if r["cond"].startswith("xfer-from-") else None
        if src and src not in skip_src:
            pooled.setdefault(r["task"], []).append(r)
            cell.setdefault((src, r["task"]), []).append(r)
    res = lab_compare(pooled, lab_base)
    if res:
        res["cells"] = [{"src": src, **lab_compare({t: rs}, lab_base)["per_task"][0]}
                        for (src, t), rs in sorted(cell.items()) if t in lab_base]
    return res


lab_ho = lab_heldout()
lab_ho_clean = lab_heldout(skip_src=("draft-markup-of-proposed-interim-order",))

board = [
    row("Study 1 · HPB", "Claude Code + Haiku, Harness² in-task", s1cc.get("h2-parallel-k1/intask"), "null",
        "At ceiling: every condition scores 1.0"),
    row("Study 1 · HPB", "ADK + qwen3:8b, in-task (as run)", s1adk.get("h2-parallel-k1/intask"), "leaky",
        "6 of 8 cells contained the task's own answers or ids"),
    row("Study 1 · HPB", "ADK, in-task, leak-void cells removed", s1adk.get("h2-parallel-k1/intask (strict)"), "primary"),
    row("Study 1 · HPB", "ADK, fresh-seed variants", s1adk.get("h2-parallel-k1/variant"), "primary"),
    row("Study 1 · HPB", "ADK, easy harness on medium/hard", s1adk.get("h2-parallel-k1/transfer"), "primary"),
    row("Study 1 · HPB", "Autoresearch (grader in loop), tuned task", s1adk.get("ar/insample"), "baseline"),
    row("Study 1 · HPB", "Autoresearch, medium/hard", s1adk.get("ar/transfer"), "baseline"),
    row("Study 2 · leak guard", "ADK, in-task (0 leak-void cells)", s2.get("h2-parallel-k1/intask"), "primary"),
    row("Study 2 · leak guard", "ADK, fresh-seed variants", s2.get("h2-parallel-k1/variant"), "primary"),
    row("Study 2 · leak guard", "ADK, easy harness on medium/hard", s2.get("h2-parallel-k1/transfer"), "primary"),
    row("Ablations", "Claude Code (4-turn cap), Sonnet improver", abl.get("Sonnet improver vs base"), "primary"),
    row("Ablations", "Claude Code (4-turn cap), Haiku improves itself (ITT)", abl.get("Haiku improver vs base, ITT"), "primary"),
    row("Ablations", "Haiku minus Sonnet as improver (ITT)", abl.get("Haiku minus Sonnet improver, ITT"), "diff"),
    row("Ablations", "ADK, no probe minus probe (ITT)", abl.get("no-probe minus probe, ITT"), "diff"),
    row("Ablations", "ADK, library off minus on (ITT)", abl.get("library off minus on, ITT"), "diff"),
    row("LAB legal tasks", "Sonnet improver, in-task", lab_full, "leaky",
        "Includes one task whose harness carried that matter's facts (+0.27)"),
    row("LAB legal tasks", "Sonnet improver, in-task, leaky task removed", lab_clean, "primary"),
    row("LAB legal tasks", "Haiku improves itself, in-task", lab_a, "primary",
        "Layer-2 guard rejected an answer key live during this arm"),
    row("LAB legal tasks", "Sonnet harnesses on unseen matters (held-out)", lab_ho, "leaky",
        "4 adopted harnesses x 3 unseen matters (R=3), one unit per target matter"),
    row("LAB legal tasks", "Held-out, leaky harness removed", lab_ho_clean, "primary",
        "Gain concentrated in redline-to-redline transfer"),
]

# ---------------------------------------------------------------- job after job (ADK, study 2)
s2r, nolib = rows(EXP / "adk-guard"), rows(EXP / "ablations" / "adk-nolib")
base, intask = cells(s2r, "base"), cells(s2r, "h2-parallel-k1/intask")
xfer, nl = cells(s2r, "h2-parallel-k1/transfer"), cells(nolib, "h2-parallel-k1/intask")
jobs = []
for d in ("data", "ops", "swe"):
    for tier in ("e", "m", "h"):
        t = f"{d}-{tier}"
        jobs.append({"task": t, "domain": d, "tier": {"e": "easy", "m": "medium", "h": "hard"}[tier],
                     "base": mean_of(base, t), "adapted": mean_of(intask, t), "carried": mean_of(xfer, t),
                     "nolib": mean_of(nl, t)})

# ---------------------------------------------------------------- check flips
flip_sets = []
for name in ("Sonnet improver vs base", "Haiku improver vs base, ITT", "probe (parallel k=1) vs base"):
    r = abl.get(name)
    if r:
        flip_sets.append({"comparison": name, "per_task": [
            {"task": p["task"], "gained": len(p["flips"]["up"]), "lost": len(p["flips"]["down"]),
             "base": p["base"], "treat": p["treat"]} for p in r["per_task"]]})
if lab_ho:
    flip_sets.append({"comparison": "LAB held-out: adopted harness on unseen matters", "per_task": [
        {"task": f"{p['src'].replace('draft-markup-of-', '')[:22]} → {p['task'].replace('draft-markup-of-', '')[:22]}",
         "gained": p["gained"], "lost": p["lost"], "base": p["base"], "treat": p["treat"]} for p in lab_ho["cells"]]})
if lab_full:
    flip_sets.append({"comparison": "LAB legal, Sonnet improver vs base", "per_task": [
        {"task": p["task"], "gained": p["gained"], "lost": p["lost"], "base": p["base"], "treat": p["treat"],
         "n_checks": p["n_checks"]} for p in lab_full["per_task"]]})

# ---------------------------------------------------------------- cost vs gain
def usd(p):
    return J(p).get("improver_usd") if Path(p).is_file() else None

cost = [
    {"arm": "ADK, Harness² (study 1)", "usd": usd(EXP / "adk/sweep-parallel-k1.json"), "tasks": 9, "delta": (s1adk.get("h2-parallel-k1/variant") or {}).get("mean_delta"), "metric": "fresh-seed"},
    {"arm": "ADK, Harness² + leak guard", "usd": usd(EXP / "adk-guard/sweep-parallel-k1.json"), "tasks": 9, "delta": (s2.get("h2-parallel-k1/variant") or {}).get("mean_delta"), "metric": "fresh-seed"},
    {"arm": "ADK, no probe", "usd": usd(EXP / "ablations/adk-noprobe/sweep-parallel-k1.json"), "tasks": 9, "delta": (abl.get("no-probe vs base, ITT") or {}).get("mean_delta"), "metric": "in-task ITT"},
    {"arm": "ADK, autoresearch", "usd": J(EXP / "adk/autoresearch/autoresearch.json").get("improver_usd"), "tasks": 3, "delta": (s1adk.get("ar/insample") or {}).get("mean_delta"), "metric": "tuned task"},
    {"arm": "CC (4-turn cap), Sonnet improver", "usd": usd(EXP / "ablations/cc-sonnet/sweep-parallel-k1.json"), "tasks": 9, "delta": (abl.get("Sonnet improver vs base") or {}).get("mean_delta"), "metric": "in-task"},
    {"arm": "CC (4-turn cap), Haiku self-improver", "usd": usd(EXP / "ablations/cc-haiku/sweep-parallel-k1.json"), "tasks": 9, "delta": (abl.get("Haiku improver vs base, ITT") or {}).get("mean_delta"), "metric": "in-task ITT"},
    {"arm": "CC full, Sonnet improver", "usd": usd(EXP / "cc/sweep-parallel-k1.json"), "tasks": 9, "delta": (s1cc.get("h2-parallel-k1/intask") or {}).get("mean_delta"), "metric": "in-task"},
    {"arm": "LAB legal, Sonnet improver", "usd": usd(EXP / "lab-sonnet-imp/sweep-parallel-k1.json"), "tasks": 4, "delta": (lab_ho_clean or {}).get("mean_delta"), "metric": "held-out, clean"},
    {"arm": "LAB legal, Haiku self-improver", "usd": usd(EXP / "lab/sweep-parallel-k1.json"), "tasks": 4, "delta": (lab_a or {}).get("mean_delta"), "metric": "in-task"},
]
for c in cost:
    c["per_task"] = round(c["usd"] / c["tasks"], 3) if c["usd"] is not None else None


# ---------------------------------------------------------------- exhibits
def skill(root, task):
    d = root / "runs/hpb-adk-agg1" / task / "harnesses/agg1/skills"
    f = next(d.glob("*/SKILL.md"), None) if d.is_dir() else None
    return {"path": str(f.relative_to(f.parent.parent.parent)), "text": f.read_text()[:3200]} if f else None


def voids(root, cond="h2-parallel-k1/intask"):
    """Leak-voided in-task cells (pre-registered rule) out of all in-task cells."""
    r = J(root / "eval" / "report.json")
    return {"void": sum(k.startswith(cond + "|") for k in r.get("voided_cells", {})),
            "of": r["comparisons"][cond]["n_tasks"]}


data = {
    "voids": {"study1": voids(EXP / "adk"), "study2": voids(EXP / "adk-guard")},
    "board": board, "jobs": jobs, "flips": flip_sets, "cost": cost,
    "lab": {"full": lab_full, "clean": lab_clean, "arm_a": lab_a, "heldout": lab_ho, "heldout_clean": lab_ho_clean},
    "exhibit": {"before": skill(EXP / "adk", "ops-e"), "after": skill(EXP / "adk-guard", "ops-e")},
    "lineage": J(OUT / "lineage.json"),
    "prereg": (EXP / "PREREG.md").read_text(),
}
(OUT / "data3.json").write_text(json.dumps(data, indent=1, default=str))
tpl = OUT / "v3-template.html"
if tpl.is_file():
    page = tpl.read_text().replace("/*__DATA__*/{}", json.dumps(data, default=str).replace("</", "<\\/"))
    (OUT / "v3.html").write_text(page)
    (OUT / "index.html").write_text(page)  # the published report (same artifact URL as v1/v2)
print("board rows:", len(board), "| jobs:", len(jobs), "| flip sets:", len(flip_sets), "| cost rows:", len(cost))
for r in board:
    print(f"  {r['study']:22s} {r['label'][:52]:52s} Δ={r['delta']:+.3f} [{r['lo']:+.2f},{r['hi']:+.2f}] {r['up']}/{r['down']} n={r['n']}")
