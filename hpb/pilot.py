"""Calibration: roll the base harness R times per task and grade, to find tasks at floor/ceiling."""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from adapters import HPBAdapter

executor, reps, width = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
root = Path(__file__).resolve().parent.parent / "experiments" / executor
ad = HPBAdapter(executor, root)
jobs = [(t, r) for t in ad.tasks() for r in range(1, reps + 1)]


def one(job):
    t, r = job
    rd = ad.execute(t, None, f"pilot/{t}/r{r}")
    g = ad.score(rd, t)
    meta = json.loads((rd / "meta.json").read_text())
    print(f"{executor} {t:9s} r{r} partial={g['partial']:.2f} all={g['all_pass']} "
          f"wall={meta.get('wall_s')} cost={meta.get('cost_usd')} err={meta.get('error', '')[:80]}",
          flush=True)
    return {"task": t, "rep": r, **g, "meta": meta}


with ThreadPoolExecutor(width) as pool:
    rows = list(pool.map(one, jobs))
(root / "pilot.json").write_text(json.dumps(rows, indent=2))
