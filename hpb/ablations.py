"""Cross-root comparisons for the ablations (PREREG.md Amendment 5) -> experiments/ablations/.

  ../repo/.venv/bin/python ablations.py
Writes results.json and the tables block of RESULTS.md (between the <!-- tables --> markers).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import bench
import stats

EXP = Path(__file__).resolve().parent.parent / "experiments"
OUT = EXP / "ablations"
G, NP, NL = EXP / "adk-guard", OUT / "adk-noprobe", OUT / "adk-nolib"
CS, CH = OUT / "cc-sonnet", OUT / "cc-haiku"
IN, TR = "h2-parallel-k1/intask", "h2-parallel-k1/transfer"
ITT = IN + "+itt"  # in-task, plus the non-adopted final (eval.py --only itt) where nothing was adopted
MAIN = [t for t, v in bench.TASKS.items() if not v["variant"]]
MH = [t for t in MAIN if bench.TASKS[t]["tier"] != "easy"]

# (ablation, comparison, (treat root, cond), (ref root, cond), tasks)
COMPARISONS = [
    ("1 self-improvement (CC)", "Sonnet improver vs base", (CS, IN), (CS, "base"), MAIN),
    ("1 self-improvement (CC)", "Haiku improver vs base", (CH, IN), (CH, "base"), MAIN),
    ("1 self-improvement (CC)", "Haiku minus Sonnet improver", (CH, IN), (CS, IN), MAIN),
    ("1 self-improvement (CC)", "Sonnet improver transfer vs base", (CS, TR), (CS, "base"), MH),
    ("1 self-improvement (CC)", "Haiku improver transfer vs base", (CH, TR), (CH, "base"), MH),
    ("1 self-improvement (CC)", "Haiku improver vs base, ITT", (CH, ITT), (CH, "base"), MAIN),
    ("1 self-improvement (CC)", "Haiku minus Sonnet improver, ITT", (CH, ITT), (CS, ITT), MAIN),
    ("2 no-probe (ADK)", "probe (parallel k=1) vs base", (G, IN), (G, "base"), MAIN),
    ("2 no-probe (ADK)", "no-probe vs base", (NP, IN), (NP, "base"), MAIN),
    ("2 no-probe (ADK)", "no-probe minus probe", (NP, IN), (G, IN), MAIN),
    ("2 no-probe (ADK)", "no-probe vs base, ITT", (NP, ITT), (NP, "base"), MAIN),
    ("2 no-probe (ADK)", "no-probe minus probe, ITT", (NP, ITT), (G, ITT), MAIN),
    ("3 library (ADK)", "library on vs base", (G, IN), (G, "base"), MH),
    ("3 library (ADK)", "library off vs base", (NL, IN), (NL, "base"), MH),
    ("3 library (ADK)", "library off minus on", (NL, IN), (G, IN), MH),
    ("3 library (ADK)", "library off vs base, ITT", (NL, ITT), (NL, "base"), MH),
    ("3 library (ADK)", "library off minus on, ITT", (NL, ITT), (G, ITT), MH),
]


def cells(root: Path, cond: str) -> dict[str, list[dict]]:
    if cond == ITT:
        return cells(root, IN.rsplit("/", 1)[0] + "/itt") | cells(root, IN)
    out = {}
    for p in (root / "eval" / cond).glob("*.json"):
        r = json.loads(p.read_text())
        if r["cond"] == cond and not r.get("infra_error"):
            out.setdefault(r["task"], []).append(r)
    return out


def voided(rows: dict[str, list[dict]]) -> dict[str, list[str]]:
    v = {t: sorted({x for r in rs for x in stats.harness_leaks(r["harness"], t)}) for t, rs in rows.items()}
    return {t: x for t, x in v.items() if x}


def fmt(c):
    return (f"{c['mean_delta']:+.3f} | [{c['ci95'][0]:+.3f}, {c['ci95'][1]:+.3f}] | "
            f"{c['signflip_p']:.3f} | {c['improved']}/{c['regressed']} | {c['n_tasks']}")


res, lines, flip_lines = [], [], []
lines += ["| ablation | comparison | Δ partial | 95% CI | sign-flip p | up/down | tasks | "
          "leak-voided cells | strict Δ (clean tasks) |", "|---|---|---|---|---|---|---|---|---|"]
for abl, name, (tr, tc), (rr, rc), tasks in COMPARISONS:
    if not (tr / "eval").is_dir() or not (rr / "eval").is_dir():
        continue
    a, b = cells(tr, tc), cells(rr, rc)
    c = stats.compare(a, b, tasks)
    if not c:
        continue
    void = {f"{tr.name}:{tc}|{t}": x for t, x in voided(a).items() if t in tasks}
    void |= {f"{rr.name}:{rc}|{t}": x for t, x in voided(b).items() if t in tasks}
    bad = {k.split("|")[1] for k in void}
    clean = [p["task"] for p in c["per_task"] if p["task"] not in bad]
    strict = stats.compare(a, b, clean) if bad and clean else None
    res.append({"ablation": abl, "comparison": name, "treat": f"{tr.name}:{tc}",
                "ref": f"{rr.name}:{rc}", **c, "voided": void, "strict": strict})
    vtxt = ", ".join(f"{k.split('|')[1]} ({len(v)})" for k, v in sorted(void.items())) or "none"
    stxt = (f"{strict['mean_delta']:+.3f} (n={strict['n_tasks']})" if strict
            else "-" if not bad else "no clean task")
    lines.append(f"| {abl} | {name} | {fmt(c)} | {vtxt} | {stxt} |")
    for p in c["per_task"]:
        f = p["flips"]
        flip_lines.append(f"| {name} | {p['task']} | {p['base']:.2f} -> {p['treat']:.2f} | "
                          f"{'; '.join(f['up']) or '-'} | {'; '.join(f['down']) or '-'} |")

tables = "\n".join(
    ["## Results table", "", *lines, "",
     "Δ = mean over tasks of (treatment mean partial − reference mean partial); CI = hierarchical "
     "bootstrap (tasks, then rollouts; 10k draws); up/down = tasks with Δ > 0.001 / < −0.001. "
     "A cell is leak-voided when its harness contains the evaluated task's own literals "
     "(bench.leaked, the pre-registered rule); strict Δ drops those tasks.", "",
     "## Check-level flips", "",
     "A check flips fail→pass (pass→fail) when its pass rate over the rollouts rises (falls) by "
     "at least 0.5 from reference to treatment. Rates shown as reference->treatment.", "",
     "| comparison | task | mean partial | fail→pass | pass→fail |", "|---|---|---|---|---|",
     *flip_lines])
audit = ["## Second-layer leak audit (hpb/leakguard.py, read-only)", "",
         "Every arm ran with the study-2 guard only: validate_tree with bench.leaked and the "
         "workspace-fact filter, with HPB_LEAKGUARD unset. The audit is run afterwards.", "",
         "| root | adopted harnesses | flagged | flags |", "|---|---|---|---|"]
for r in (G, NP, NL, CS, CH):
    if not (r / "runs").is_dir():
        continue
    p = subprocess.run([sys.executable, str(Path(__file__).with_name("leakguard.py")), "audit", str(r)],
                       capture_output=True, text=True, cwd=Path(__file__).parent)
    m = re.search(r"audited (\d+) adopted harnesses; flagged (\d+)", p.stdout)
    flags = [ln.split(" ", 1) for ln in p.stdout.splitlines() if "/harnesses/" in ln]
    ftxt = "; ".join(f"{h.split('/')[-3]}: {f}" for h, f in flags) or "-"
    audit.append(f"| {r.name} | {m and m.group(1)} | {m and m.group(2)} | {ftxt} |")
tables += "\n\n" + "\n".join(audit)

# .git was readable inside the sandbox from 12:28 to 13:20 IST (git init; fixed in efd91a1).
# Any rollout that read repo content through git (show/cat-file/grep/archive/ls-*) or named
# hpb/ in a git command would void its cell.
GIT_ANY = re.compile(r"\bgit (?:status|log|show|cat-file|grep|diff|ls-files|ls-tree|archive|rev-parse)\b")
GIT_READ = re.compile(r"\bgit (?:-C \S+ )?(?:show|cat-file|grep|archive|ls-tree|ls-files)\b|\bgit [^\"\n]{0,80}hpb/")
gx = ["## Exposure check: .git readable 12:28-13:20 IST", "",
      "| root | rollouts + improver sessions scanned | ran any git command | read repo content via git | voided |",
      "|---|---|---|---|---|"]
for r in (G, NP, NL, CS, CH):
    fs = [f for pat in ("stream.jsonl", "trajectory.jsonl") for f in (r / "exec").rglob(pat)]
    fs += list((r / "audit").rglob("streams/*.jsonl"))  # improver sessions
    anyg = [f for f in fs if GIT_ANY.search(f.read_text(errors="replace"))]
    reads = [f for f in anyg if GIT_READ.search(f.read_text(errors="replace"))]
    gx.append(f"| {r.name} | {len(fs)} | {len(anyg)} | {len(reads)} | "
              f"{', '.join(str(f.relative_to(r)) for f in reads) or 'none'} |")
tables += "\n\n" + "\n".join(gx)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "results.json").write_text(json.dumps(res, indent=1))
md = OUT / "RESULTS.md"
body = md.read_text() if md.is_file() else "# Harness² ablations\n\n<!-- tables -->\n<!-- /tables -->\n"
md.write_text(re.sub(r"<!-- tables -->.*<!-- /tables -->",
                     lambda _: f"<!-- tables -->\n{tables}\n<!-- /tables -->", body, flags=re.S))
print("\n".join(lines))
