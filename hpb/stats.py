"""Statistics shared by eval.py and ablations.py (PREREG.md: hierarchical bootstrap,
exact sign-flip test, the leak rule, and check-level flips)."""

import functools
import itertools
import random
import statistics
from pathlib import Path

import bench


def boot_delta(pairs, n=10000, seed=0):
    """Hierarchical bootstrap of mean per-task delta: resample tasks, then rollouts."""
    rng = random.Random(seed)
    ds = []
    for _ in range(n):
        tot = 0.0
        for _ in pairs:
            a, b = rng.choice(pairs)
            tot += statistics.mean(rng.choices(a, k=len(a))) - statistics.mean(rng.choices(b, k=len(b)))
        ds.append(tot / len(pairs))
    ds.sort()
    return ds[int(0.025 * n)], ds[int(0.975 * n)]


def signflip_p(deltas):
    obs = abs(sum(deltas))
    hits = sum(abs(sum(s * d for s, d in zip(signs, deltas))) >= obs - 1e-12
               for signs in itertools.product((1, -1), repeat=len(deltas)))
    return hits / 2 ** len(deltas)


def flips(treat: list[dict], ref: list[dict], thresh: float = 0.5) -> dict:
    """Grader checks whose pass rate rose (fail->pass) or fell (pass->fail) by >= thresh
    between the ref rollouts and the treatment rollouts of one task."""
    rate = lambda rows, c: statistics.mean(bool((r.get("checks") or {}).get(c)) for r in rows)
    names = sorted({c for r in treat + ref for c in r.get("checks") or {}})
    out = {"up": [], "down": []}
    for c in names:
        a, b = rate(treat, c), rate(ref, c)
        if abs(a - b) >= thresh:
            out["up" if a > b else "down"].append(f"{c} {b:.2f}->{a:.2f}")
    return out


def compare(treat: dict[str, list[dict]], ref: dict[str, list[dict]], tasks) -> dict | None:
    """Per-task paired partial-score deltas, treat minus ref, over tasks present in both."""
    per, pairs = [], []
    for t in tasks:
        rt, rr = treat.get(t) or [], ref.get(t) or []
        if not rt or not rr:
            continue
        a, b = [r["partial"] for r in rt], [r["partial"] for r in rr]
        per.append({"task": t, "tier": bench.TASKS[t]["tier"], "treat": statistics.mean(a),
                    "base": statistics.mean(b), "delta": statistics.mean(a) - statistics.mean(b),
                    "treat_allpass": f"{sum(r['all_pass'] for r in rt)}/{len(rt)}",
                    "base_allpass": f"{sum(r['all_pass'] for r in rr)}/{len(rr)}",
                    "treat_sd": statistics.pstdev(a), "base_sd": statistics.pstdev(b),
                    "flips": flips(rt, rr)})
        pairs.append((a, b))
    if not per:
        return None
    deltas = [p["delta"] for p in per]
    lo, hi = boot_delta(pairs)
    return {"n_tasks": len(per), "mean_delta": statistics.mean(deltas), "ci95": [lo, hi],
            "signflip_p": signflip_p(deltas), "improved": sum(d > 0.001 for d in deltas),
            "regressed": sum(d < -0.001 for d in deltas), "per_task": per}


def local(path: str) -> Path:
    """Eval rows store absolute paths from the machine that ran them; rebase them onto this checkout."""
    p = Path(path)
    if p.exists() or "/experiments/" not in path:
        return p
    return Path(__file__).resolve().parent.parent / "experiments" / path.split("/experiments/", 1)[1]


@functools.lru_cache(maxsize=None)
def harness_leaks(harness: str, task: str) -> tuple[str, ...]:
    """Pre-registered leak rule: the evaluated task's own literals found in the harness."""
    if harness == "base":
        return ()
    txt = "\n".join(f.read_text(errors="replace") for f in local(harness).rglob("*") if f.is_file())
    return tuple(bench.leaked(txt, task))
