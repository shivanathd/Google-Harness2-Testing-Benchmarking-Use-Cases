"""Ablation drivers for Harness² parallel k=1; harness2 core is imported, never edited.

  ../repo/.venv/bin/python ablate.py adk --no-probe --share-base ../experiments/adk-guard \
      --root ../experiments/ablations/adk-noprobe
  ../repo/.venv/bin/python ablate.py adk --no-library --tiers medium hard \
      --share-base ../experiments/adk-guard --root ../experiments/ablations/adk-nolib

--no-probe    INV and DOM proposals are composed (agg1) without their probe rollouts.
--no-library  every task runs as a one-task stream with its own empty library.
--share-base  reuse that root's base rollouts (H2 base1 and eval/base), so the ablation sees
              the same evidence as the run it is compared with.
The output layout is run.py's (runs/hpb-<x>-agg1, sweep-parallel-k1.json): eval.py works on
it with --root.
"""

import argparse
import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import harness2.core.proposer as P
from harness2.core import prompts, recursion
from harness2.core import tree as HT
from harness2.core.ledger import Ledger
from harness2.core.schedule import mode_token, run_domain
from harness2.core.spec import resolve_prompts

import bench
from adapters import HPBAdapter, LocalClaudeProposer

PROBED = "Each candidate was rolled out ONCE and you have that rollout."
UNPROBED = ("NO candidate was rolled out: you have each candidate's harness and diff only, so "
            "weigh every edit against the base rollout evidence alone.")


def run_parallel_noprobe(task_id, k, base, *, adapter, prop, work_dir, run_id_of, base_tree,
                         library_dir=None, **_):
    """recursion.run_parallel minus the 2k candidate rollouts (R=2k, P=3k by design)."""
    surface = adapter.substrate.surface()
    ledger = Ledger(mode="agg", task_id=task_id, k=k)
    for r in base:
        ledger.rollout(r.label)
    result = recursion.ModeResult(mode="agg", task_id=task_id, k=k, ledger=ledger)
    result.rollouts.update({r.label: r for r in base})
    bp = resolve_prompts(adapter, task_id)
    base_dir = HT.write_tree(surface, base_tree, work_dir / "harnesses" / "base")

    def stage(label, dim, job, **kw):
        return recursion._run_stage(label=label, dim=dim, job=job, fallback=base_tree,
                                    adapter=adapter, prop=prop, ctx_dir=work_dir / "context",
                                    task_id=task_id, rollouts=base, harness_dir=base_dir,
                                    library_dir=library_dir, **kw)

    specs = [(f"{d.lower()}{i}", d, i) for i in range(1, k + 1) for d in ("INV", "DOM")]
    with ThreadPoolExecutor(len(specs)) as pool:
        stages = list(pool.map(lambda s: stage(s[0], s[1], prompts.propose(
            bp, s[1], surface, k=k, index=s[2])), specs))
    recursion._record_sessions(ledger, stages)
    for s in stages:
        result.stages.append(s)
        result.trees[s.label] = s.tree
        HT.write_tree(surface, s.tree, work_dir / "harnesses" / s.label)

    pool_ev = [(s.label, work_dir / "harnesses" / s.label, None) for s in stages]
    decisions = {s.label: s.notes or s.error for s in stages}

    def agg(i):
        job = prompts.aggregate(bp, surface, k=k, index=i)
        assert PROBED in job, "harness2 aggregate prompt changed; update the no-probe rewrite"
        return stage(f"agg{i}", "AGG", job.replace(PROBED, UNPROBED), pool=pool_ev,
                     decisions=decisions)

    with ThreadPoolExecutor(k) as pool:
        aggs = list(pool.map(agg, range(1, k + 1)))
    recursion._record_sessions(ledger, aggs)
    for s in aggs:
        result.stages.append(s)
        result.trees[s.label] = s.tree
        result.finals.append(s.label)
    result.rollouts.update(recursion._roll_many(
        adapter, ledger, task_id, [(s.label, s.tree) for s in aggs], run_id_of, work_dir,
        width=recursion.PHASE_WIDTH))
    result.similarity = HT.diversity({s.label: s.tree for s in aggs})
    return result


def share_base(src: Path, dst: Path, executor: str) -> None:
    for rd in (src / "exec").glob(f"hpb-{executor}-agg1/*/base1"):
        out = dst / rd.relative_to(src)
        if not out.exists():
            shutil.copytree(rd, out)
    if (src / "eval/base").is_dir():
        shutil.copytree(src / "eval/base", dst / "eval/base", dirs_exist_ok=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("executor", choices=("cc", "adk"))
    ap.add_argument("--root", required=True)
    ap.add_argument("--no-probe", action="store_true")
    ap.add_argument("--no-library", action="store_true")
    ap.add_argument("--tiers", nargs="+", default=["easy", "medium", "hard"])
    ap.add_argument("--domains", nargs="+", default=list(bench.DOMAINS))
    ap.add_argument("--share-base")
    ap.add_argument("--improver-sessions", type=int, default=6)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    if args.share_base:
        share_base(Path(args.share_base).resolve(), root, args.executor)
    if args.no_probe:
        recursion.run_parallel = run_parallel_noprobe  # recursion.run_mode looks it up at call time
    P._SEM = threading.BoundedSemaphore(args.improver_sessions)
    ad = HPBAdapter(args.executor, root)
    prop = LocalClaudeProposer(ad.spec.channels["proposer"], audit_dir=root / "audit/parallel-k1")
    (root / "ablation.json").write_text(json.dumps(vars(args) | {"improver": ad.spec.channels["proposer"].model}))

    keep = lambda ts: [t for t in ts if bench.TASKS[t]["tier"] in args.tiers]
    streams = [(d, keep(bench.DOMAINS[d]), root / "library/parallel-k1") for d in args.domains]
    if args.no_library:
        streams = [(d, [t], root / "library/parallel-k1" / t) for d, ts, _ in streams for t in ts]

    def go(s):
        d, ts, lib = s
        return run_domain(d, ts, 1, adapter=ad, prop=prop, runs_root=ad.spec.runs_root,
                          library_root=lib, modes=(mode_token("parallel"),))

    with ThreadPoolExecutor(len(streams)) as pool:
        res = list(pool.map(go, streams))
    out = {(ts[0] if args.no_library else d): r for (d, ts, _), r in zip(streams, res)}
    out["improver_usd"] = round(sum(r.cost_usd for r in prop._calls), 4)
    out["improver_calls"] = len(prop._calls)
    (root / "sweep-parallel-k1.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({d: (v["done"], v["failed"]) for d, v in out.items() if isinstance(v, dict)}),
          "improver_usd", out["improver_usd"])
