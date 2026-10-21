"""Build the writer's pack in ~/Downloads from the committed experiment outputs."""
import csv, json, shutil, subprocess, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP, REP = ROOT / "experiments", ROOT / "report"
OUT = Path.home() / "Downloads" / "Harness2-Field-Test"
shutil.rmtree(OUT, ignore_errors=True)
for d in ("results/per-arm", "report", "benchmark-code"):
    (OUT / d).mkdir(parents=True, exist_ok=True)

D = json.loads((REP / "data3.json").read_text())
L, V, LAB = D["lineage"], D["voids"], D["lab"]
commit = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%h (%cd)", "--date=format:%d %b %Y %H:%M"],
                        capture_output=True, text=True).stdout.strip()
REPORT_URL = "report/Harness2-on-the-Bench.html in this pack"
f2 = lambda x: "–" if x is None else f"{x:+.2f}"
BOARD = {(r["study"], r["label"]): r for r in D["board"]}


def b(study, label):
    r = BOARD[(study, label)]
    return f"{f2(r['delta'])} (95% CI {r['lo']:+.2f} to {r['hi']:+.2f}; {r['up']} up / {r['down']} down of {r['n']})"


def board_row(r):
    p = "–" if r["p"] is None else f"{r['p']:.3f}"
    return f"| {r['study']} | {r['label']} | {f2(r['delta'])} | {r['lo']:+.2f} to {r['hi']:+.2f} | {r['up']} / {r['down']} | {r['n']} | {p} |"


def cost_row(c):
    per = "–" if c["per_task"] is None else f"${c['per_task']:.2f}"
    return f"| {c['arm']} | {per} | {f2(c['delta'])} | {c['metric']} |"


# ------------------------------------------------------------ chart-ready results
with open(OUT / "results/scoreboard.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["study", "comparison", "kind", "delta", "ci_low", "ci_high", "tasks", "improved", "regressed", "signflip_p", "note"])
    for r in D["board"]:
        w.writerow([r["study"], r["label"], r["kind"], round(r["delta"], 4), round(r["lo"], 4), round(r["hi"], 4),
                    r["n"], r["up"], r["down"], None if r["p"] is None else round(r["p"], 4), r["note"]])
with open(OUT / "results/job-after-job.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["task", "domain", "tier", "base", "adapted", "carried", "nolib"])
    w.writeheader(); w.writerows(D["jobs"])
with open(OUT / "results/cost-vs-gain.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["arm", "usd", "tasks", "per_task", "delta", "metric"])
    w.writeheader(); w.writerows(D["cost"])
with open(OUT / "results/check-flips.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["comparison", "task", "checks_gained", "checks_lost", "base", "treatment"])
    for fs in D["flips"]:
        for p in fs["per_task"]:
            w.writerow([fs["comparison"], p["task"], p["gained"], p["lost"], round(p["base"], 3), round(p["treat"], 3)])
(OUT / "results/all-data.json").write_text(json.dumps(D, indent=1))
for src, name in [(EXP / "PREREG.md", "PREREG.md"), (EXP / "leak-guard-results.md", "study2-leak-guard-RESULTS.md"),
                  (EXP / "ablations/RESULTS.md", "ablations-RESULTS.md"), (EXP / "ablations/results.json", "ablations-results.json"),
                  (EXP / "lab/RESULTS.md", "lab-legal-RESULTS.md")]:
    shutil.copy(src, OUT / "results" / name)
for rep in sorted(EXP.glob("**/eval/report.json")):
    arm = str(rep.parent.parent.relative_to(EXP)).replace("/", "-")
    shutil.copy(rep, OUT / "results/per-arm" / f"{arm}-report.json")

# ------------------------------------------------------------ report, diagrams, benchmark code
shutil.copy(REP / "index.html", OUT / "report/Harness2-on-the-Bench.html")
shutil.copy(next(ROOT.glob(".archify/workflow-harness2-loop-*/final/harness2-loop.html")), OUT / "report/diagram-harness2-task-loop.html")
shutil.copy(next(ROOT.glob(".archify/architecture-*/final/hpb-rig.html")), OUT / "report/diagram-test-rig.html")
for f in sorted((ROOT / "hpb").glob("*.py")):
    shutil.copy(f, OUT / "benchmark-code" / f.name)
shutil.copytree(ROOT / "hpb/reference", OUT / "benchmark-code/reference")

# ------------------------------------------------------------ lineage + learnings
TYPE = {"ask": "You asked", "decision": "Decision", "finding": "Finding", "bug": "Bug caught", "amendment": "Pre-reg amendment"}
cell = lambda s: str(s or "").replace("|", "\\|").replace("\n", " ")
ev = sorted(L["events"], key=lambda e: e["t"])
lin = ["# Decision lineage", "",
       f"Every request, decision, finding, bug and pre-registration amendment, in time order (IST, 19 Oct 2026). {len(ev)} events.", "",
       "| Time | Type | What happened | Why / found by | Evidence |", "|---|---|---|---|---|"]
lin += [f"| {e['t']} | {TYPE.get(e['type'], e['type'])} | **{cell(e['title'])}**. {cell(e.get('what'))} | "
        f"{cell(e.get('why') or e.get('found_by'))} | {cell(e.get('evidence'))} |" for e in ev]
(OUT / "02-decision-lineage.md").write_text("\n".join(lin) + "\n")
learn = ["# Learnings", ""]
for k, n in {"harness2": "About Harness²", "benchmarking": "About benchmarking agents", "claude_code": "About Claude Code"}.items():
    learn += [f"## {n}", ""] + [f"- {x}" for x in L["learnings"].get(k, [])] + [""]
(OUT / "03-learnings.md").write_text("\n".join(learn))

# ------------------------------------------------------------ verdicts
demo = next(p for p in LAB["arm_a"]["per_task"] if p["task"].startswith("draft-markup-of-procedural-order"))
S2, AB, S1, LT = "Study 2 · leak guard", "Ablations", "Study 1 · HPB", "LAB legal tasks"
verd = f"""# Verdicts and findings

Generated from the committed results (`results/scoreboard.csv`). Δ = mean change in the fraction of grader checks
passed versus that study's base harness; 95% hierarchical-bootstrap interval; up/down = tasks that moved.

## The five verdicts

1. **It works where there is headroom and a stronger improver.**
   - Weak local model (Google ADK + qwen3:8b), leak guard on, fresh instances its improver never saw: {b(S2, "ADK, fresh-seed variants")}.
   - Claude Code capped at 4 turns, Sonnet improving Haiku: {b(AB, "Claude Code (4-turn cap), Sonnet improver")}.
   - Full-strength Claude Code was already at ceiling: {b(S1, "Claude Code + Haiku, Harness² in-task")}. Harness² kept the base harness on every task.
2. **Self-improvement is weaker, and can hurt (no interval excludes zero).**
   - Haiku improving its own harness (Claude Code, intent-to-treat): {b(AB, "Claude Code (4-turn cap), Haiku improves itself (ITT)")}.
   - Haiku minus Sonnet as improver: {b(AB, "Haiku minus Sonnet as improver (ITT)")}.
   - Legal tasks, Haiku improving itself: {b(LT, "Haiku improves itself, in-task")}. The {demo['n_checks']}-check demo task fell from {demo['base'] * demo['n_checks']:.1f} to {demo['treat'] * demo['n_checks']:.1f} checks.
3. **Each job is its own jump, not a staircase.**
   - Easy-task harness reused on medium/hard: {b(S2, "ADK, easy harness on medium/hard")}.
   - Lesson library off minus on: {b(AB, "ADK, library off minus on (ITT)")}, all of it on one task (data-hard).
   - No probe minus probe: {b(AB, "ADK, no probe minus probe (ITT)")}. The paper's claim that probing first matters did not reproduce here.
4. **It leaks unless you stop it.**
   - Unguarded, {V['study1']['void']} of {V['study1']['of']} adopted harnesses carried the task's own answers or ids; with the guard, {V['study2']['void']} of {V['study2']['of']}.
   - Unguarded in-task gain as run: {b(S1, "ADK + qwen3:8b, in-task (as run)")}; leak-voided cells removed: {b(S1, "ADK, in-task, leak-void cells removed")}.
   - On legal tasks both Sonnet and Haiku wrote answer keys for the matter in front of them without ever seeing the rubric.
5. **On Google's own legal tasks (LAB) the gain is small, not significant, and partly format.**
   - Sonnet harnesses on matters their improver never saw (one unit per target matter): {b(LT, "Sonnet harnesses on unseen matters (held-out)")}; leaky harness removed: {b(LT, "Held-out, leaky harness removed")}.
   - In-task: {b(LT, "Sonnet improver, in-task")}; clean: {b(LT, "Sonnet improver, in-task, leaky task removed")}.
   - The gain sits mostly in redline-to-redline transfer, much of it teaching the deliverable format the judge's reader expects.
   - The harness2 README quotes up to +11.8 points for one step (quoted, not measured here).

## Karpathy autoresearch (grader in the loop)
- Tuned task: {b(S1, "Autoresearch (grader in loop), tuned task")}.
- Frozen, on medium/hard: {b(S1, "Autoresearch, medium/hard")}.
- With a trustworthy check, autoresearch is simpler and cheaper; without one, Harness² still makes progress. Neither transferred up a tier.

## Full scoreboard

| Study | Comparison | Δ | 95% CI | Up / down | Tasks | Sign-flip p |
|---|---|---|---|---|---|---|
""" + "\n".join(board_row(r) for r in D["board"]) + """

## Cost against gain (improver spend only; executor and judge costs excluded)

| Arm | $ per task | Δ | Metric |
|---|---|---|---|
""" + "\n".join(cost_row(c) for c in D["cost"]) + "\n"
(OUT / "01-verdicts-and-findings.md").write_text(verd)

(OUT / "04-benchmarks-and-tests.md").write_text("""# Benchmarks and tests

## What was tested
Google Research's Harness² (github.com/google-research/harness2, commit 1cfe254, core unmodified). It rewrites an
agent's surroundings (system prompt, guardrails, memory, tool guidance, skills, scripts, subagents, plugins) while the
model stays fixed: Propose edits, Probe them on the same task, Compose a refined harness, then write a lesson into a
per-domain library that later tasks read.

## Benchmarks
1. **HPB (built for this test): 9 tasks + 6 fresh-seed variants, hidden programmatic graders.**
   - data, revenue reconciliation. Easy: one CSV with duplicates, `(x)` negatives, FX. Medium: daily FX and partial refunds. Hard: rules only in POLICY.md (UTC month boundary, minor units incl. JPY, test customers, chargeback fees).
   - ops, log analytics. Easy: timezone offsets and traceback traps. Medium: rotated gzip logs, retries. Hard: per-service p95 with a seconds/ms schema switch and RUNBOOK exclusions.
   - swe, issue fixing with hidden tests. Easy: one function. Medium: 3-module invoicing package. Hard: CLI repo with 2 bugs, 1 feature and regression tests on its output format.
2. **LAB (Google's own, harveyai/harvey-labs):** 4 arbitration tasks, 37–59 rubric checks each, scored by a Claude rubric judge that mirrors LAB's scorer.

## Agents and improvers
- Claude Code CLI (`claude -p`, Haiku 5.5); capped at 4 turns in the ablations to create headroom.
- Google ADK agent on local qwen3:8b via Ollama (4 workspace tools + load_skill).
- Improvers: Claude Sonnet 5.5, or Haiku 5.5 improving itself.

## Studies (all committed in the repo)
| Study | What | Where |
|---|---|---|
| 1 | Harness² parallel k=1 on both agents; sequential k=2 on Claude Code; Karpathy autoresearch baseline | experiments/cc, experiments/adk |
| 2 | Leak guard + Stop-hook (c8) rerun on ADK | experiments/adk-guard |
| Ablations | Self-improvement (Haiku vs Sonnet improver), no-probe, library off | experiments/ablations |
| LAB | Google's legal tasks: in-task, Haiku self-improver, held-out matrix at R=3 | experiments/lab, experiments/lab-sonnet-imp |

## Measurement
- Pre-registered endpoints (`results/PREREG.md`) with 7 dated amendments, each written before the results it affects, or labelled post-hoc.
- Fresh re-rolls of every adopted harness (R=3–4); hierarchical-bootstrap 95% CI; exact sign-flip test. Units that share a base (LAB held-out) are grouped per target before testing.
- Headline metric: data the improver never saw (fresh-seed variants, held-out matters). In-task numbers are labelled test-time adaptation.

## Tests that guard the benchmark itself
- `python benchmark-code/bench.py`: grader self-test. Every task scores about 0 untouched and 1.0 on its reference solution (15 tasks).
- `python benchmark-code/leakguard.py`: leak-detector self-check (catches the known study-1 leaks, allows stated policy constants).
- `python benchmark-code/adapters.py`: adapter self-check of the adoption-time guard.
- Before any treatment run: an adversarial review (critical, supportive and neutral reviewers) and a security review. They caught 1 silent blocker and 7 grader or spec bugs.
- Leak audits over every agent and improver log: harness literal scan, grader-path scan, sandbox-blocked access scan.
- A post-publication code review of the report builder fixed a statistics error (held-out p 0.085 → 0.25).

## Isolation
macOS `sandbox-exec` around every model process: environment allow-list (no tokens), reads of graders, other runs,
credentials and `.git` denied, writes only in the workspace, web tools off.
""")

(OUT / "00-README.md").write_text(f"""# Harness² on the Bench: writer's pack

A field test of Google Research's Harness² ("recursive agent harnessing"), run 19 Oct 2026 with Claude Code.
Generated from repo commit {commit}. Interactive report: {REPORT_URL}.

## Start here
| File | What it is |
|---|---|
| 01-verdicts-and-findings.md | The five verdicts with numbers, the full scoreboard, cost against gain |
| 02-decision-lineage.md | {len(ev)} events in time order: what was decided, why, and what each bug changed |
| 03-learnings.md | Learnings about Harness², benchmarking agents, and Claude Code |
| 04-benchmarks-and-tests.md | Benchmarks, agents, studies, measurement, tests, isolation |
| report/Harness2-on-the-Bench.html | The full interactive report (open in a browser) |
| report/diagram-*.html | Interactive diagrams of the Harness² loop and the test rig |
| results/*.csv | Scoreboard, job-after-job, check flips, cost against gain (chart-ready) |
| results/*-RESULTS.md, PREREG.md | Each study's own write-up, and the pre-registration |
| results/per-arm/*.json | Raw evaluation reports per arm |
| benchmark-code/ | Benchmark, graders, adapters, leak guard, evaluation and stats code |

## The story in sequence
1. **The claim.** A video and the README say Harness² lets an agent improve itself job after job, without changing the model.
2. **Preflight.** Google's own benchmarks need Vertex Gemini, and the only Google Cloud project here was production, so we built our own benchmark and ran Harness² unmodified behind our own adapter.
3. **Calibration.** Claude Code + Haiku passed every task (27/27), so we added difficulty tiers and a weak local agent (ADK + qwen3:8b) that had real headroom.
4. **Review before running.** Three adversarial reviewers and a security review caught a silent blocker (every Harness² edit would have been dropped), impossible test data, forgeable graders, and API tokens exposed to agents.
5. **Study 1.** Large in-task gains on the weak model, none on Claude Code (correctly). A login glitch faked a +0.11 gain until an A/A check exposed it.
6. **The leak.** The improver wrote the answers into the harness ({V['study1']['void']} of {V['study1']['of']} tasks). We built a leak guard; study 2 kept the gain with {V['study2']['void']} of {V['study2']['of']} leaks.
7. **Ablations.** A model improving itself does about half as well as a stronger improver; skipping the probe step changed nothing; the library barely mattered.
8. **Google's legal tasks.** Held-out gain {f2(LAB['heldout']['mean_delta'])} (95% CI {LAB['heldout']['ci95'][0]:+.2f} to {LAB['heldout']['ci95'][1]:+.2f}), mostly format; Haiku improving itself got worse.
9. **Reviewing our own report** fixed a statistics error: the held-out p-value went from 0.085 to 0.25 once cells sharing a base were grouped.

## One-paragraph summary
Harness² is real but narrow. It turns a weak agent's repeated failures into correct runs, and the edits it writes (a domain skill with a tested script, rules like "write the deliverable early") hold on fresh data. It does nothing for an agent already at ceiling, and it knows to leave that agent alone. Its gains don't carry from one task family to a harder one, the lesson library and the probe step mattered little in our runs, a model improving itself does about half as well as a stronger improver, and unguarded it writes the answers straight into the harness. On Google's own legal tasks the measurable gain is a few points, mostly from teaching the deliverable format.
""")

zp = OUT.parent / "Harness2-Field-Test.zip"
zp.unlink(missing_ok=True)
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            z.write(f, f.relative_to(OUT.parent))
print(f"wrote {OUT} ({sum(1 for f in OUT.rglob('*') if f.is_file())} files) and {zp.name} ({zp.stat().st_size // 1024} KB)")
