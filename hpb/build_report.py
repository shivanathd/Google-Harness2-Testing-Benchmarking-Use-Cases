"""Collect experiment results into report/data.json and inline them into report/index.html."""

import json
import statistics
from pathlib import Path

import bench

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
OUT = ROOT / "report"
MODE = {"parallel": "agg", "sequential": "seq"}


def rows(ex):
    out = []
    for p in (EXP / ex / "eval").rglob("*.json"):
        if p.name != "report.json":
            r = json.loads(p.read_text())
            if not r.get("infra_error"):
                out.append(r)
    return out


def per_task(rs, cond):
    by = {}
    for r in rs:
        if r["cond"] == cond:
            by.setdefault(r["task"], []).append(r)
    return {t: {"mean": statistics.mean(x["partial"] for x in v), "n": len(v),
                "allpass": sum(x["all_pass"] for x in v),
                "scores": [round(x["partial"], 3) for x in sorted(v, key=lambda x: x["rep"])]}
            for t, v in by.items()}


def selections(ex, run):
    mode, k = run.split("-k")
    out = {}
    for summ in (EXP / ex / "runs").glob(f"hpb-{ex}-agg{k}*/*/summary.json"):
        d = json.loads(summ.read_text())
        sel = (d.get("selections") or {}).get(MODE[mode]) or {}
        m = (d.get("modes") or {}).get(MODE[mode]) or {}
        exp = sel.get("experience") or {}
        out[d["task_id"]] = {
            "chosen": sel.get("chosen_label"), "is_base": bool(sel.get("chosen_tree_is_base")),
            "kept_base": m.get("kept_base"), "fell_back": m.get("fell_back"),
            "usd": (m.get("ledger") or {}).get("session_usd"),
            "lesson": exp.get("lesson"), "cue": exp.get("cue"),
        }
    return out


def executor(ex):
    rep_f = EXP / ex / "eval" / "report.json"
    rep = json.loads(rep_f.read_text()) if rep_f.is_file() else {}
    rs = rows(ex)
    conds = sorted({r["cond"] for r in rs})
    ar_f = EXP / ex / "autoresearch" / "autoresearch.json"
    sweeps = {f.stem.replace("sweep-", ""): json.loads(f.read_text()) for f in (EXP / ex).glob("sweep-*.json")}
    return {
        "report": rep,
        "cells": {c: per_task(rs, c) for c in conds},
        "selections": {run: selections(ex, run) for run in ("parallel-k1", "sequential-k2")},
        "autoresearch": json.loads(ar_f.read_text()) if ar_f.is_file() else None,
        "improver_usd": {k: v.get("improver_usd") for k, v in sweeps.items()},
        "rollouts": len(rs),
        "wall": {c: round(statistics.mean(r.get("wall_s") or 0 for r in rs if r["cond"] == c), 1) for c in conds},
        "exec_usd": round(sum(r.get("cost_usd") or 0 for r in rs), 3),
    }


def sample_skill():
    """The adopted skill shown as evidence: the largest one either executor adopted."""
    best = None  # parallel k=1 adopts its single composition, agg1; completed tasks only
    for ex in ("adk", "cc"):
        for t in ("data-e", "ops-e", "swe-e", "data-m", "ops-m", "swe-m"):
            if best is None and (EXP / ex / "runs" / f"hpb-{ex}-agg1" / t / "summary.json").is_file():
                best = next((EXP / ex / "runs" / f"hpb-{ex}-agg1" / t / "harnesses/agg1").glob("skills/*/SKILL.md"), None)
    if not best:
        return None
    root = best.parent.parent.parent
    files = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.name != "README.md")
    return {"executor": "cc" if "/cc/" in str(best) else "adk", "task": root.parent.parent.name,
            "path": str(best.relative_to(root)), "text": best.read_text()[:4200], "tree": files,
            "system": (root / "systemprompt.md").read_text()[:1500]}


data = {
    "tasks": {t: {"domain": v["domain"], "tier": v["tier"], "variant": v["variant"],
                  "checks": None} for t, v in bench.TASKS.items()},
    "cc": executor("cc"),
    "adk": executor("adk"),
    "skill": sample_skill(),
    "prereg": (EXP / "PREREG.md").read_text(),
}
OUT.mkdir(exist_ok=True)
(OUT / "data.json").write_text(json.dumps(data, indent=1, default=str))
tpl = (OUT / "template.html").read_text()
(OUT / "index.html").write_text(tpl.replace("/*__DATA__*/{}", json.dumps(data, default=str).replace("</", "<\\/")))
print("wrote", OUT / "index.html", len((OUT / "index.html").read_text()), "bytes")
