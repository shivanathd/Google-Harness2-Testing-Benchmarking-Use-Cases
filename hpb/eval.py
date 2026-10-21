"""Evaluation per PREREG.md: fresh re-rolls of base / adopted / frozen harnesses, then stats.

  ../repo/.venv/bin/python eval.py adk base --reps 4
  ../repo/.venv/bin/python eval.py adk h2 --run parallel-k1 --reps 4
  ../repo/.venv/bin/python eval.py adk ar --reps 4
  ../repo/.venv/bin/python eval.py adk report
"""

import argparse
import itertools
import json
import re
import statistics
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import bench
import stats
from adapters import HPBAdapter

ap = argparse.ArgumentParser()
ap.add_argument("executor", choices=("cc", "adk"))
ap.add_argument("phase", choices=("base", "h2", "ar", "report"))
ap.add_argument("--run", default="parallel-k1", help="Harness² run name, e.g. sequential-k2")
ap.add_argument("--reps", type=int, default=4)
ap.add_argument("--width", type=int, default=9)
ap.add_argument("--only", nargs="+", default=["intask", "variant", "transfer"],
                help="h2 phase: which conditions to roll (also: itt)")
ap.add_argument("--root", help="experiments root (default experiments/<executor>)")
args = ap.parse_args()

root = Path(args.root or Path(__file__).resolve().parent.parent / "experiments" / args.executor).resolve()
ad = HPBAdapter(args.executor, root)
EVAL = root / "eval"
MAIN = [t for t, v in bench.TASKS.items() if not v["variant"]]
VARIANT = {t[:-2]: t for t in bench.TASKS if t.endswith("-v")}
MODE = {"parallel": "agg", "sequential": "seq"}


def roll(cond: str, harness: Path | None, task: str, reps: int) -> list[dict]:
    """reps fresh rollouts; recorded under eval/<cond>/<task>.json (resumable)."""
    jobs = [(cond, harness, task, r) for r in range(1, reps + 1)]
    return jobs


def run_jobs(jobs: list) -> None:
    def one(job):
        cond, harness, task, r = job
        rd = ad.execute(task, harness, f"eval/{cond}/{task}/r{r}")
        g = ad.score(rd, task)
        meta = json.loads((rd / "meta.json").read_text())
        row = {"cond": cond, "task": task, "rep": r, "partial": g["partial"], "all_pass": g["all_pass"],
               "checks": g["checks"], "harness": str(harness or "base"),
               **{k: meta.get(k) for k in ("cost_usd", "tokens_in", "tokens_out", "wall_s", "error",
                                           "infra_error", "turns", "tool_calls")}}
        out = EVAL / cond / f"{task}.r{r}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(row, indent=1))
        print(f"{args.executor} {cond:22s} {task:8s} r{r} partial={g['partial']:.2f} "
              f"err={str(meta.get('error') or '')[:50]}", flush=True)
    with ThreadPoolExecutor(args.width) as pool:
        list(pool.map(one, jobs))


def adopted(run: str) -> dict[str, tuple[Path, bool]]:
    """task -> (adopted harness dir, adopted-is-base) from a Harness² run."""
    mode, k = run.split("-k")
    out = {}
    # harness2 writes every mode's summary under the "agg" namespace (where the shared base
    # rollouts live) but each mode's harnesses under its own namespace.
    for summ in (root / "runs").glob(f"hpb-{args.executor}-agg{k}*/*/summary.json"):
        d = json.loads(summ.read_text())
        sel = (d.get("selections") or {}).get(MODE[mode]) or {}
        if sel.get("chosen_label"):
            ns = summ.parent.parent.name.replace("-agg", f"-{MODE[mode]}", 1)
            out[d["task_id"]] = (root / "runs" / ns / d["task_id"] / "harnesses" / sel["chosen_label"],
                                 bool(sel.get("chosen_tree_is_base")))
    return out


if args.phase == "base":
    jobs = list(itertools.chain.from_iterable(roll("base", None, t, args.reps) for t in MAIN))
    jobs += list(itertools.chain.from_iterable(roll("base", None, v, 2) for v in VARIANT.values()))
    run_jobs(jobs)

elif args.phase == "h2":
    ad_h = adopted(args.run)
    tag = f"h2-{args.run}"
    jobs = []
    for t, (h, _) in ad_h.items():
        if "intask" in args.only:
            jobs += roll(f"{tag}/intask", h, t, args.reps)
        if t in VARIANT and "variant" in args.only:
            jobs += roll(f"{tag}/variant", h, VARIANT[t], 2)
    if "itt" in args.only:  # not adopted (the final delivered nothing): roll that final anyway
        k = args.run.split("-k")[1]
        for summ in (root / "runs").glob(f"hpb-{args.executor}-agg{k}*/*/summary.json"):
            d = json.loads(summ.read_text())
            fin = ((d.get("modes") or {}).get(MODE[args.run.split("-k")[0]]) or {}).get("finals") or []
            if d["task_id"] not in ad_h and fin:
                ns = summ.parent.parent.name.replace("-agg", f"-{MODE[args.run.split('-k')[0]]}", 1)
                jobs += roll(f"{tag}/itt", root / "runs" / ns / d["task_id"] / "harnesses" / fin[0],
                             d["task_id"], args.reps)
    for dom, tasks in bench.DOMAINS.items():
        easy = tasks[0]
        if easy in ad_h and "transfer" in args.only:
            for t in tasks[1:]:
                jobs += roll(f"{tag}/transfer", ad_h[easy][0], t, args.reps)
    run_jobs(jobs)

elif args.phase == "ar":
    jobs = []
    for dom, tasks in bench.DOMAINS.items():
        final = root / "autoresearch" / dom / "final"
        if not final.is_dir():
            continue
        jobs += roll("ar/insample", final, tasks[0], args.reps)
        for t in tasks[1:]:
            jobs += roll("ar/transfer", final, t, args.reps)
        for t in tasks:
            if t in VARIANT:
                jobs += roll("ar/variant", final, VARIANT[t], 2)
    run_jobs(jobs)

else:  # report
    rows = [json.loads(p.read_text()) for p in EVAL.rglob("*.json") if p.name != "report.json"]
    valid = [r for r in rows if not r.get("infra_error")]
    by = {}
    for r in valid:
        by.setdefault((r["cond"], r["task"]), []).append(r)

    def cell(cond, task):
        rs = by.get((cond, task), [])
        return [r["partial"] for r in rs], [r["all_pass"] for r in rs]

    def compare(cond, tasks, ref=lambda t: ("base", t)):
        return stats.compare({t: by.get((cond, t), []) for t in tasks},
                             {t: by.get(ref(t), []) for t in tasks}, tasks)

    def pass_k(cond, tasks, k):
        vals = []
        for t in tasks:
            _, ap_ = cell(cond, t)
            n, c = len(ap_), sum(ap_)
            if n >= k:
                vals.append(sum(1 for comb in itertools.combinations(ap_, k) if all(comb)) /
                            len(list(itertools.combinations(ap_, k))))
        return statistics.mean(vals) if vals else None

    # Pre-registered leak rule, applied per cell: a harness that contains the evaluated
    # task's own expected answers or instance ids voids that cell.
    leaked = stats.harness_leaks

    void = {}
    for (c, t), rs in by.items():
        hits = sorted({h for r in rs for h in leaked(r["harness"], t)})
        if hits:
            void[(c, t)] = hits
    report_void = {f"{c}|{t}": h for (c, t), h in void.items()}
    conds = sorted({c for c, _ in by})
    hard_mid = [t for t in MAIN if bench.TASKS[t]["tier"] != "easy"]
    report = {"executor": args.executor, "task_hash": bench.TASK_HASH,
              "n_rows": len(rows), "infra_voided": len(rows) - len(valid), "comparisons": {}}
    for c in conds:
        if c == "base":
            continue
        tasks = [t for t in bench.TASKS if (c, t) in by]
        if c.endswith("/variant"):
            cmp = compare(c, tasks)
        elif c.endswith("/transfer"):
            cmp = compare(c, [t for t in hard_mid if t in tasks])
        else:
            cmp = compare(c, tasks)
        report["comparisons"][c] = cmp
        clean = [t for t in (cmp or {}).get("per_task", []) and [p["task"] for p in cmp["per_task"]] if (c, t) not in void]
        if cmp and len(clean) < cmp["n_tasks"]:
            report["comparisons"][c + " (strict)"] = compare(c, clean) if clean else None
    report["voided_cells"] = report_void
    report["base_mean"] = statistics.mean(statistics.mean(cell("base", t)[0]) for t in MAIN if cell("base", t)[0])
    report["pass_k"] = {c: {k: pass_k(c, MAIN, k) for k in (1, 2, 3)} for c in conds
                        if not c.endswith("variant")}
    report["cost"] = {c: {"exec_usd": round(sum(r.get("cost_usd") or 0 for r in valid if r["cond"] == c), 4),
                          "tokens_in": sum(r.get("tokens_in") or 0 for r in valid if r["cond"] == c),
                          "tokens_out": sum(r.get("tokens_out") or 0 for r in valid if r["cond"] == c),
                          "rollouts": sum(1 for r in valid if r["cond"] == c),
                          "mean_wall_s": round(statistics.mean([r.get("wall_s") or 0 for r in valid if r["cond"] == c]), 1)}
                      for c in conds}
    # improver spend per run
    report["improver"] = {}
    for f in root.glob("sweep-*.json"):
        d = json.loads(f.read_text())
        report["improver"][f.stem] = {"usd": d.get("improver_usd"), "calls": d.get("improver_calls")}
    arj = root / "autoresearch" / "autoresearch.json"
    if arj.is_file():
        d = json.loads(arj.read_text())
        report["improver"]["autoresearch"] = {"usd": d.get("improver_usd")}
        report["autoresearch_log"] = {k: v for k, v in d.items() if isinstance(v, dict)}

    # leak audit
    lits = set()
    for t, v in bench.TASKS.items():
        for leaf in json.dumps(v["expected"]).replace("{", " ").replace("}", " ").split(","):
            val = leaf.split(":")[-1].strip().strip('"')
            if re.fullmatch(r"\d+\.\d+", val) or (val.isdigit() and int(val) >= 100):
                lits.add(val)
    harness_dirs = set(stats.local(r["harness"]) for r in valid if r["harness"] != "base")
    hits = []
    for h in harness_dirs:
        for f in h.rglob("*"):
            if f.is_file():
                txt = f.read_text(errors="replace")
                hits += [f"{f}: literal {x}" for x in lits if x in txt]
                hits += [f"{f}: id {m}" for m in set(re.findall(r"\b(?:T11\d{3}|S0\d\d|ch_\d{3}|r\d{6})\b", txt))]
    blocked_exec = [str(p) for p in (root / "exec").rglob("stream.jsonl") if "Operation not permitted" in p.read_text(errors="replace")]
    blocked_exec += [str(p) for p in (root / "exec").rglob("trajectory.jsonl") if "Operation not permitted" in p.read_text(errors="replace")]
    streams = list((root / "audit").rglob("streams/*.jsonl"))
    grader_refs = [str(p) for p in streams + list((root / "exec").rglob("stream.jsonl"))
                   if re.search(r"hpb/(bench|tiers|reference)", p.read_text(errors="replace"))]
    report["leak_audit"] = {"harness_literal_hits": sorted(set(hits))[:50],
                            "blocked_escape_attempts": blocked_exec[:50],
                            "grader_path_mentions": grader_refs[:50],
                            "improver_sessions_audited": len(streams),
                            "harnesses_audited": len(harness_dirs)}
    (EVAL / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({c: (v and {k: v[k] for k in ("n_tasks", "mean_delta", "ci95", "signflip_p", "improved", "regressed")})
                      for c, v in report["comparisons"].items()}, indent=1))
    for c, v in report["comparisons"].items():  # check-level flips (stats.flips)
        for p in (v or {}).get("per_task", []):
            if p["flips"]["up"] or p["flips"]["down"]:
                print(f"flips {c} {p['task']}: fail->pass {p['flips']['up']} pass->fail {p['flips']['down']}")
    print("leak:", {k: (len(v) if isinstance(v, list) else v) for k, v in report["leak_audit"].items()})
