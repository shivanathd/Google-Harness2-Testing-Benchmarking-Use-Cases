"""Karpathy-style autoresearch baseline on the same harness surface.

Per domain: the first task is the dev task. Each iteration the improver edits the harness
(program.md-style mission), we roll it once, grade it with the REAL grader, and keep the edit
only if the scalar score strictly beats the incumbent (git-style keep/revert). The final
harness is then frozen and evaluated on the held-out tasks. This is the verifier-in-the-loop
counterpart to Harness²'s verifier-free Propose-Probe-Compose.
"""

import argparse
import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import harness2.core.proposer as P
from harness2.core import tree as HT

import bench
from adapters import SURFACE, HPBAdapter, LocalClaudeProposer

PROGRAM = """# program.md -- autoresearch on an agent harness

You are improving the HARNESS of a smaller agent: the files in `context/harness/`
(systemprompt.md, guardrails.md, LongTermMEMORY.md, tool_descriptions/tool_guidance.md,
skills/<name>/SKILL.md with `name:` and `description:` frontmatter, scripts/<name>.py).
The agent's model is fixed; only these files change.

`context/task.md` is the kind of work the agent does and `context/source/` holds its input
files. `context/trajectory.md` and
`context/output/` show its latest attempt with the current harness. `context/results.tsv`
lists every experiment so far and its score (0..1, higher is better; the scoring code is not
available to you).

Make ONE focused change to the files in `context/harness/` that you expect to raise the
score. Improve how the agent works on this KIND of task -- the harness will be reused on
other tasks of the same kind, so never write task-specific facts or answers. Edit the files in
place, then reply with one line: <notes>what you changed and why</notes>.
"""

ap = argparse.ArgumentParser()
ap.add_argument("executor", choices=("cc", "adk"))
ap.add_argument("--iters", type=int, default=4)
args = ap.parse_args()

P._SEM = threading.BoundedSemaphore(6)
root = Path(__file__).resolve().parent.parent / "experiments" / args.executor
ad = HPBAdapter(args.executor, root)
prop = LocalClaudeProposer(ad.spec.channels["proposer"], audit_dir=root / "audit" / "autoresearch")
out_root = root / "autoresearch"


def research(domain: str) -> dict:
    dev = bench.DOMAINS[domain][0]
    d = out_root / domain
    best_tree = HT.read_tree(SURFACE, ad.base_harness())
    rd = ad.execute(dev, ad.base_harness(), f"ar/{domain}/it0")
    best = ad.score(rd, dev)["partial"]
    log = [{"iter": 0, "score": best, "kept": True, "notes": "baseline"}]
    for it in range(1, args.iters + 1):
        ctx = d / f"ctx{it}"
        shutil.rmtree(ctx, ignore_errors=True)
        HT.write_tree(SURFACE, best_tree, ctx / "harness")
        (ctx / "task.md").write_text(ad.task_prompt(dev))
        shutil.copytree(ad.task_files(dev), ctx / "source")  # same evidence Harness2's improver gets
        (ctx / "trajectory.md").write_text(ad.trajectory(rd, obs_trunc=3000)[-60000:])
        for k, v in ad.deliverable_files(rd).items():
            (ctx / "output" / k).parent.mkdir(parents=True, exist_ok=True)
            (ctx / "output" / k).write_text(v)
        (ctx / "results.tsv").write_text("iter\tscore\tkept\tnotes\n" + "".join(
            f"{r['iter']}\t{r['score']:.3f}\t{r['kept']}\t{r['notes'][:200]}\n" for r in log))
        try:
            reply = prop.call(PROGRAM, ctx, f"ar.{domain}.{it}", harvest="context/harness")
            cand = HT.read_tree(SURFACE, reply.workspace) if reply.workspace else {}
            notes = reply.text.strip()[-300:]
        except Exception as exc:
            cand, notes = {}, f"improver failed: {exc}"
        if not cand:
            log.append({"iter": it, "score": best, "kept": False, "notes": notes})
            continue
        hdir = HT.write_tree(SURFACE, cand, d / f"h{it}")
        crd = ad.execute(dev, hdir, f"ar/{domain}/it{it}")
        s = ad.score(crd, dev)["partial"]
        kept = s > best
        if kept:
            best, best_tree, rd = s, cand, crd
        log.append({"iter": it, "score": s, "kept": kept, "notes": notes})
        print(f"[ar {args.executor} {domain}] it{it} score={s:.2f} best={best:.2f} kept={kept}",
              flush=True)
    HT.write_tree(SURFACE, best_tree, d / "final")
    return {"dev_task": dev, "best_dev_score": best, "log": log, "final": str(d / "final")}


with ThreadPoolExecutor(3) as pool:
    res = dict(zip(bench.DOMAINS, pool.map(research, bench.DOMAINS)))
res["improver_usd"] = round(sum(r.cost_usd for r in prop._calls), 4)
(out_root / "autoresearch.json").write_text(json.dumps(res, indent=2))
print("done", {k: v["best_dev_score"] for k, v in res.items() if isinstance(v, dict)})
