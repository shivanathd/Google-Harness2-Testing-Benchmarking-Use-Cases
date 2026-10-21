"""Run Harness² (unmodified core) on HPB-9 for one executor, mode and budget k.

  ../repo/.venv/bin/python run.py cc --mode parallel --k 1
Domains run concurrently; tasks inside a domain run in order so the library carries forward.
"""

import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import harness2.core.proposer as P
from harness2.core.schedule import mode_token, run_domain

import bench
from adapters import HPBAdapter, LocalClaudeProposer

ap = argparse.ArgumentParser()
ap.add_argument("executor", choices=("cc", "adk"))
ap.add_argument("--mode", choices=("parallel", "sequential"), default="parallel")
ap.add_argument("--k", type=int, default=1)
ap.add_argument("--domains", nargs="+", default=list(bench.DOMAINS))
ap.add_argument("--improver-sessions", type=int, default=6)
ap.add_argument("--root", help="experiments root (default experiments/<executor>)")
args = ap.parse_args()

P._SEM = threading.BoundedSemaphore(args.improver_sessions)  # release default is 2
root = Path(args.root or Path(__file__).resolve().parent.parent / "experiments" / args.executor).resolve()
ad = HPBAdapter(args.executor, root)
name = f"{args.mode}-k{args.k}"
prop = LocalClaudeProposer(ad.spec.channels["proposer"], audit_dir=root / "audit" / name)


def domain(d: str) -> dict:
    return run_domain(d, bench.DOMAINS[d], args.k, adapter=ad, prop=prop,
                      runs_root=ad.spec.runs_root, library_root=root / "library" / name,
                      modes=(mode_token(args.mode),))


with ThreadPoolExecutor(len(args.domains)) as pool:
    out = dict(zip(args.domains, pool.map(domain, args.domains)))
out["improver_usd"] = round(sum(r.cost_usd for r in prop._calls), 4)
out["improver_calls"] = len(prop._calls)
(root / f"sweep-{name}.json").write_text(json.dumps(out, indent=2))
print(json.dumps({d: (v["done"], v["failed"]) for d, v in out.items() if isinstance(v, dict)}),
      "improver_usd", out["improver_usd"])
