"""LAB (harveyai/harvey-labs) tasks on the HPB rig: sandboxed Claude Code executor, Harness²
core unmodified, and a rubric judge run through the sandboxed claude CLI.

  ../repo/.venv/bin/python lab.py selfcheck
  ../repo/.venv/bin/python lab.py base --reps 3        # fresh base rollouts, judged
  ../repo/.venv/bin/python lab.py h2 --k 1             # Harness² parallel k=1, library on
  ../repo/.venv/bin/python lab.py adopted --reps 3     # re-roll each adopted harness, judged
  ../repo/.venv/bin/python lab.py report

The rubric lives only in task.json `criteria`. It is read in exactly one place, `criteria()`,
whose only caller is `score()` (the judge). The executor and improver get the task through
`task.json` minus `criteria`, every sandbox also denies reads of the whole LAB checkout, and
the LAB leak glob keeps task.json out of the improver's context tree.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import adapters as A
import leakguard
from adapters import C8_HELP, FACT_RX, HPBAdapter, harness_fingerprint
from harness2.benchmarks.lab import CODEX_BASE_BODY, LAB_BASE, lab_prompts
from harness2.core import tree as HT
from harness2.core.spec import BenchSpec, ChannelSpec

LAB = A.ROOT / "repo/dependencies/harvey-labs"
LAB_COMMIT = "b58a28ae9fde5ee4b810e53b4fd0a1915325a35d"
AREA = "arbitration-international-dispute-resolution"
TASKS = [f"{AREA}/{t}" for t in sorted([
    "draft-markup-of-arbitration-agreement",
    "draft-markup-of-procedural-order",  # the 55-check public-demo task
    "draft-markup-of-proposed-interim-order",
    "identify-arbitration-agreement-issues",
])]
EXEC_MODEL = os.environ.get("LAB_EXECUTOR", "claude-haiku-5-5")
IMPROVER = os.environ.get("LAB_IMPROVER", EXEC_MODEL)  # self-improvement by default
JUDGE = os.environ.get("LAB_JUDGE", "claude-sonnet-5-5")
DELIV_CAP = 60_000  # harness2 config.LAB_DELIV_CAP
A.EXECUTOR_MODEL["cc"] = EXEC_MODEL  # _run_cc reads it at call time
# The CLI's message when the shared OAuth session expires; adapters.AUTH_FAIL predates it, and
# without it such a rollout counts as an agent failure instead of plumbing.
if "Failed to authenticate" not in A.AUTH_FAIL:
    A.AUTH_FAIL = A.AUTH_FAIL + ("Failed to authenticate",)

# Every model-driven process (executor, improver, judge) also loses read access to the LAB
# checkout, which holds the rubric. The deny is appended last, so it wins over the profile's
# allows. adapters.py calls `sandboxed` through its module global, so this covers its callers.
_sandboxed = A.sandboxed


def sandboxed(cmd, *, read_ok=(), write_ok=()):
    c = _sandboxed(cmd, read_ok=read_ok, write_ok=write_ok)
    c[2] += f'\n(deny file-read* (subpath "{LAB}"))'
    return c


A.sandboxed = sandboxed

READ_DOC = '''#!/usr/bin/env python3
"""Print the text of a document: python3 scripts/read_doc.py <path>"""
import subprocess, sys
from pathlib import Path
p = Path(sys.argv[1])
if p.suffix.lower() == ".docx":
    r = subprocess.run(["pandoc", str(p), "-t", "markdown", "--wrap=none",
                        "--track-changes=all"], capture_output=True, text=True)
    sys.stdout.write(r.stdout); sys.stderr.write(r.stderr); sys.exit(r.returncode)
sys.stdout.write(p.read_text(errors="replace"))
'''

JUDGE_SYSTEM = "You grade legal work product against one criterion. Reply with JSON only."
JUDGE_PROMPT = (LAB / "evaluation/prompts/rubric_criterion.txt")


def task_json(task_id: str) -> dict:
    """task.json WITHOUT `criteria`: what the executor and improver may see."""
    d = json.loads((LAB / "tasks" / task_id / "task.json").read_text())
    d.pop("criteria", None)
    return d


def criteria(task_id: str) -> list[dict]:
    """The rubric. Judge only."""
    return json.loads((LAB / "tasks" / task_id / "task.json").read_text())["criteria"]


def docx_text(p: Path, track: str = "accept") -> str:
    """LAB judge's reader (evaluation.scoring._read_file_as_text) for the formats used here."""
    if p.suffix.lower() == ".docx":
        r = subprocess.run(["pandoc", str(p), "-t", "markdown", "--wrap=none",
                            f"--track-changes={track}"], capture_output=True, text=True,
                           errors="replace", timeout=60)
        return r.stdout if r.returncode == 0 else f"(error reading {p.name}: {r.stderr[:200]})"
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"(binary file: {p.name})"


DICT = {w.strip().lower() for w in open("/usr/share/dict/words")}
LEAKGUARD_VERSION = "layer2 = hpb/leakguard.py + LabInstance (dictionary entities, no years, datum >= 2)"


class LabInstance(leakguard.Instance):
    def scan(self, text: str) -> dict[str, list[str]]:
        hits = super().scan(text)
        if len(hits.get("datum", [])) < 2:  # one stray section number or constant is noise
            hits.pop("datum", None)
        return hits


class LabAdapter(HPBAdapter):
    """HPBAdapter's executor, sandbox and trajectory code on LAB task data."""

    def __init__(self, root: Path, rollout_timeout: int = 1800):  # noqa: super() writes HPB data
        self.executor = "cc"
        self.root = Path(root)
        self.exec_root = self.root / "exec"
        self.rollout_timeout = rollout_timeout
        self.max_turns = 40  # what every LAB rollout here used; adapters._run_cc reads it
        self.substrate = A.Substrate("cc")
        channel = ChannelSpec("claude_cli", IMPROVER, effort="high", timeout=1800)
        self.spec = BenchSpec(name="lab", runs_root=self.root / "runs",
                              install_mode="workspace_config", prompts=LAB_BASE,
                              channels={"proposer": channel, "selector": channel},
                              domain_word="practice area", leak_globs=("task.json",),
                              proposer_deliverables="contents", obs_trunc=50_000)
        if not (self.base_harness() / "systemprompt.md").is_file():
            base = {name: "" for name in A.SURFACE.always_on}
            base["systemprompt.md"] = CODEX_BASE_BODY  # harness2's own LAB base body
            HT.write_tree(A.SURFACE, base, self.base_harness(), stubs=False)
        for tid in TASKS:  # staged data room: documents/, empty output/, scripts/read_doc.py
            d = self.task_files(tid)
            if not (d / "scripts/read_doc.py").is_file():
                shutil.copytree(LAB / "tasks" / tid / "documents", d / "documents",
                                dirs_exist_ok=True)
                (d / "output").mkdir(exist_ok=True)
                (d / "scripts").mkdir(exist_ok=True)
                (d / "scripts/read_doc.py").write_text(READ_DOC)

    def tasks(self, split: str = "all") -> list[str]:
        return list(TASKS)

    def domain_of(self, task_id: str) -> str:
        return task_id.split("/", 1)[0]

    def prompts_for(self, task_id: str):
        return lab_prompts(practice_area=self.domain_of(task_id),
                           work_type=str(task_json(task_id).get("work_type", "")))

    def task_prompt(self, task_id: str, *, max_chars: int = 12_000) -> str:
        """harness2 LabAdapter.task_prompt: the improver's answer-free view of the task."""
        A._CUR.task = task_id  # context.build calls this in the thread that then validates
        t = task_json(task_id)
        parts = [f"# TASK {task_id}", f"**Title:** {t.get('title', '')}",
                 f"**Work type:** {t.get('work_type', '')}"]
        if t.get("tags"):
            parts.append("**Tags:** " + ", ".join(map(str, t["tags"])))
        parts.append("\n## Instructions\n" + str(t.get("instructions", "")).strip())
        if t.get("deliverables"):
            parts.append("\n## Deliverables\n" + "\n".join(
                f"- `{n}`" + (f" — {d}" if d and d != n else "")
                for n, d in t["deliverables"].items()))
        return "\n\n".join(parts)[:max_chars]

    def exec_prompt(self, task_id: str) -> str:
        """LAB runner's assignment message (run_codex_lab.build_prompt), workspace = cwd."""
        return ("=== WORKSPACE ===\n. (the current directory)\n\n"
                "=== DOCUMENTS (read-only) ===\ndocuments/\n\n"
                "=== OUTPUT DIRECTORY (deliverables go here) ===\noutput/\n\n"
                f"=== ASSIGNMENT ===\n{str(task_json(task_id)['instructions']).strip()}")

    def task_files(self, task_id: str) -> Path:
        return self.root / "sources" / task_id

    def validate_tree(self, tree: dict[str, str]) -> None:
        """harness2 LabAdapter's cx invariants (output/, read_doc.py in the always-on text),
        plus this rig's c8 rule and workspace-fact rule."""
        errs = []
        body = "\n".join(tree.get(r, "") for r in A.SURFACE.always_on)
        if "output/" not in body:
            errs.append("the always-on prompt must say deliverables go to `output/<filename>`")
        if "read_doc.py" not in body:
            errs.append("the always-on prompt must say .docx files are read with "
                        "`python3 scripts/read_doc.py <path>`")
        for rel, src in sorted(tree.items()):
            if rel.startswith("plugin/"):
                errs.append(f"{rel}: {C8_HELP}")
            if rel == "scripts/read_doc.py":
                errs.append("scripts/read_doc.py is the runtime's reader; a harness may not ship it")
            facts = sorted({m.group(0) for m in FACT_RX.finditer(src)})
            if facts:
                errs.append(f"{rel} has a workspace-fact block ({', '.join(facts)}): keep only "
                            "method, never facts about this matter's files.")
        task = getattr(A._CUR, "task", None)
        if task and (found := leakguard.scan_tree(tree, self.instance(task))):
            errs.append(leakguard.message(found))
        if errs:
            raise ValueError(" | ".join(errs))

    def instance(self, task_id: str) -> leakguard.Instance:
        """Layer-2 leak guard (hpb/leakguard.py): the matter's data room minus what the task's
        instructions, the base body and the runtime reader already state."""
        inst = LabInstance(self.task_files(task_id) / "documents", "\n".join(
            [str(task_json(task_id)["instructions"]), CODEX_BASE_BODY, READ_DOC]))
        # LAB tuning: legal vocabulary (Respondent, Section, Arbitrator) is in the dictionary;
        # matter names (Andino, Bogotá, PetroChem) are not. Years are not instance data.
        inst.entities = {e for e in inst.entities if any(w.lower() not in DICT for w in e.split())}
        inst.data_nums = {n for n in inst.data_nums if not re.fullmatch(r"(19|20)\d\d", n)}
        return inst

    def execute(self, task_id: str, harness_dir: Path | None, run_id: str, *,
                timeout: int | None = None) -> Path:
        """HPBAdapter.execute keyed on the LAB commit instead of the HPB task hash."""
        run_dir = self.exec_root / run_id
        harness = Path(harness_dir or self.base_harness())
        fp = harness_fingerprint(harness)
        meta_f = run_dir / "meta.json"
        if meta_f.is_file():
            old = json.loads(meta_f.read_text())
            if old.get("harness_fp") == fp and old.get("task_hash") == LAB_COMMIT \
                    and not old.get("infra_error") and not self._is_infra(old, run_dir):
                return run_dir
        for attempt in range(1, 4):
            shutil.rmtree(run_dir, ignore_errors=True)
            work = run_dir / "work"
            shutil.copytree(self.task_files(task_id), work)
            t0 = time.time()
            self._run_cc(harness, work, run_dir, self.exec_prompt(task_id),
                         timeout or self.rollout_timeout)
            meta = json.loads(meta_f.read_text()) if meta_f.is_file() else {"error": "no meta"}
            meta.update(task=task_id, harness=str(harness), harness_fp=fp, task_hash=LAB_COMMIT,
                        model=EXEC_MODEL, wall_s=round(time.time() - t0, 1), attempt=attempt,
                        infra_error=self._is_infra(meta, run_dir))
            meta_f.write_text(json.dumps(meta, indent=2))
            if not meta["infra_error"]:
                break
            time.sleep(20 * attempt)
        return run_dir

    def deliverable_files(self, run_dir: Path) -> dict[str, str]:
        """output/* through the judge's own reader, capped as harness2 caps it."""
        out = Path(run_dir) / "work/output"
        files = {}
        for p in sorted(out.rglob("*")) if out.is_dir() else []:
            if p.is_file():
                t = docx_text(p)
                files[f"output/{p.relative_to(out)}"] = (
                    t[:DELIV_CAP] + f"\n\n... [truncated, {len(t) - DELIV_CAP} more chars]"
                    if len(t) > DELIV_CAP else t)
        return files

    # ---- judge
    def score(self, run_dir: Path, task_id: str) -> dict | None:
        """LAB's rubric scoring (evaluation.scoring.score_rubric): one judge call per
        criterion, with only that criterion's deliverables, read with tracked changes
        accepted. Judge failure => None, never 0; scores are cached in scores.json."""
        run_dir = Path(run_dir)
        cache = run_dir / "scores.json"
        if cache.is_file():
            return json.loads(cache.read_text())
        out = run_dir / "work/output"
        title = task_json(task_id).get("title", "")
        tmpl = JUDGE_PROMPT.read_text()

        def deliverable(name: str) -> str:
            p = out / name
            if not p.is_file():  # LAB fuzzy-matches names; an exact-or-basename match here
                hits = [q for q in out.rglob("*") if q.is_file() and q.name.lower() == name.lower()]
                p = hits[0] if hits else p
            return (f"## Agent Output: {name}\n" + docx_text(p) if p.is_file()
                    else f"## Agent Output: {name}\n(File not found: {name})")

        part_f = run_dir / "judge_partial.json"  # verdicts survive a failed sibling call
        part = json.loads(part_f.read_text()) if part_f.is_file() else {}
        lock = threading.Lock()

        def one(c: dict):
            if c["id"] in part:
                return tuple(part[c["id"]])
            body = "\n\n".join(deliverable(n) for n in c.get("deliverables") or []) \
                or "(No agent output found)"
            prompt = (tmpl.replace("{task_description}", title).replace("{agent_output}", body)
                      .replace("{criterion_title}", c["title"])
                      .replace("{match_criteria}", c["match_criteria"]).replace("{{", "{")
                      .replace("}}", "}"))
            spent = 0.0
            for attempt in range(8):
                with A._CLAUDE_SLOTS:  # the rig-wide cap (4) on concurrent claude -p processes
                    verdict, why, usd = _judge_call(prompt)
                spent += usd
                if verdict:
                    with lock:
                        part[c["id"]] = (c["id"], verdict, why, spent)
                        part_f.write_text(json.dumps(part))
                    return c["id"], verdict, why, spent
                time.sleep(30 * (attempt + 1))  # the CLI's OAuth refresh races under load
            return c["id"], None, why, spent

        with ThreadPoolExecutor(8) as pool:
            res = list(pool.map(one, criteria(task_id)))
        usd = round(sum(r[3] for r in res), 4)
        if any(r[1] is None for r in res):
            print(f"judge failed on {run_dir}: "
                  f"{[(r[0], r[2][:120]) for r in res if r[1] is None][:3]}", file=sys.stderr)
            return None
        checks = {r[0]: r[1] == "pass" for r in res}
        n = sum(checks.values())
        s = {"n_passed": n, "n_criteria": len(checks), "all_pass": n == len(checks),
             "partial": n / len(checks), "checks": checks, "judge_model": JUDGE,
             "judge_usd": usd, "reasoning": {r[0]: r[2] for r in res}}
        cache.write_text(json.dumps(s, indent=1))
        return s


def _judge_call(prompt: str) -> tuple[str | None, str, float]:
    """One sandboxed, tool-less claude -p call; returns (verdict, reasoning, cost)."""
    with tempfile.TemporaryDirectory() as td:
        cmd = A.isolated_claude(JUDGE) + ["--tools", "", "--system-prompt", JUDGE_SYSTEM,
                                         "--output-format", "json"]
        try:
            p = subprocess.run(sandboxed(cmd, write_ok=[td]), input=prompt, cwd=td,
                               env=A.base_env(), text=True, capture_output=True, timeout=600)
        except subprocess.TimeoutExpired:
            return None, "timeout", 0.0
    try:
        ev = json.loads(p.stdout)
    except ValueError:
        return None, f"rc={p.returncode} {p.stderr[-200:]}", 0.0
    usd = float(ev.get("total_cost_usd") or 0.0)
    text = str(ev.get("result") or "")
    m = re.search(r"\{.*\}", text, re.S)
    try:
        got = json.loads(m.group(0)) if m else {}
    except ValueError:
        got = {}
    v = str(got.get("verdict", "")).lower()
    return (v if v in ("pass", "fail") else None), str(got.get("reasoning", text[:300])), usd


# ---- drivers
def roll_and_judge(ad: LabAdapter, cond: str, jobs: list[tuple[str, Path | None, int]],
                   width: int) -> None:
    def one(job):
        task, harness, r = job
        rd = ad.execute(task, harness, f"eval/{cond}/{task}/r{r}")
        meta = json.loads((rd / "meta.json").read_text())
        g = None if meta.get("infra_error") else ad.score(rd, task)  # plumbing: never scored
        row = {"cond": cond, "task": task, "rep": r, "harness": str(harness or "base"),
               **({k: g[k] for k in ("partial", "n_passed", "n_criteria", "all_pass", "checks",
                                     "judge_usd")} if g else {"judge_error": True}),
               **{k: meta.get(k) for k in ("cost_usd", "turns", "wall_s", "error", "infra_error",
                                           "tokens_in", "tokens_out")}}
        f = ad.root / "eval" / cond / f"{task.replace('/', '__')}.r{r}.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(row, indent=1))
        print(f"{cond} {task.split('/')[-1]} r{r} "
              f"{g['n_passed'] if g else '?'}/{g['n_criteria'] if g else '?'} "
              f"exec ${meta.get('cost_usd')} judge ${g['judge_usd'] if g else '?'} "
              f"turns={meta.get('turns')} err={str(meta.get('error') or '')[:40]}", flush=True)
    with ThreadPoolExecutor(width) as pool:
        list(pool.map(one, jobs))


def adopted(root: Path, k: int) -> dict[str, tuple[Path, bool]]:
    """task -> (adopted harness dir, adopted-is-base) from a parallel Harness² run."""
    out = {}
    for summ in (root / "runs").glob(f"lab-cc-agg{k}*/**/summary.json"):
        d = json.loads(summ.read_text())
        sel = (d.get("selections") or {}).get("agg") or {}
        if sel.get("chosen_label"):
            out[d["task_id"]] = (summ.parent / "harnesses" / sel["chosen_label"],
                                 bool(sel.get("chosen_tree_is_base")))
    return out


def _selfcheck(ad: LabAdapter) -> None:
    """The rubric cannot reach a model-driven process."""
    t = TASKS[1]
    crit = criteria(t)
    assert len(crit) == 55, len(crit)
    seen = ad.task_prompt(t) + ad.exec_prompt(t) + json.dumps(task_json(t))
    assert "criteria" not in task_json(t) and not any(c["match_criteria"][:60] in seen for c in crit)
    staged = [p.name for p in ad.task_files(t).rglob("*") if p.is_file()]
    assert "task.json" not in staged, staged
    # a sandboxed process cannot read task.json, but can read its staged documents
    p = subprocess.run(sandboxed(["cat", str(LAB / "tasks" / t / "task.json")]),
                       capture_output=True, text=True)
    assert p.returncode != 0 and "Operation not permitted" in p.stderr, p.stderr
    doc = next(ad.task_files(t).glob("documents/*.docx"))
    p = subprocess.run(sandboxed(["python3", str(ad.task_files(t) / "scripts/read_doc.py"),
                                  str(doc)], read_ok=[ad.task_files(t)]),
                       cwd=ad.task_files(t), capture_output=True, text=True)
    assert p.returncode == 0 and len(p.stdout) > 500, p.stderr
    ad.task_prompt(t)  # sets the validating thread's task, as context.build does
    ad.validate_tree({"systemprompt.md": CODEX_BASE_BODY})
    leaky = A.EXPERIMENTS / "lab-sonnet-imp/runs/lab-cc-agg1" / (
        TASKS[2].replace("/", "__") + "/harnesses/agg1/skills/interim-measures-order-review/SKILL.md")
    if leaky.is_file():  # study-2 Arm B's adopted answer key must be rejected for its own task
        ad.task_prompt(TASKS[2])
        try:
            ad.validate_tree({"systemprompt.md": CODEX_BASE_BODY, "skills/x/SKILL.md": leaky.read_text()})
            raise AssertionError("layer-2 guard accepted the interim-order answer key")
        except ValueError as exc:
            assert "instance" in str(exc), exc
    for bad in ({"systemprompt.md": "Write files."},
                {"systemprompt.md": CODEX_BASE_BODY, "plugin/x.ts": "export const P = 1"}):
        try:
            ad.validate_tree(bad)
            raise AssertionError(f"accepted {bad}")
        except ValueError:
            pass
    print("lab self-check ok")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("selfcheck", "base", "h2", "adopted", "transfer", "audit", "report"))
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--width", type=int, default=6)
    ap.add_argument("--tasks", nargs="+", default=TASKS)
    ap.add_argument("--root", default=str(A.EXPERIMENTS / "lab"))
    ap.add_argument("--src", help="transfer: the task whose adopted harness is re-rolled on --tasks")
    args = ap.parse_args()
    ad = LabAdapter(Path(args.root).resolve())
    if args.phase == "selfcheck":
        _selfcheck(ad)
    elif args.phase == "base":
        roll_and_judge(ad, "base", [(t, None, r) for t in args.tasks
                                    for r in range(1, args.reps + 1)], args.width)
    elif args.phase == "h2":
        import harness2.core.proposer as P
        from harness2.core.schedule import mode_token, run_domain
        from adapters import LocalClaudeProposer
        P._SEM = threading.BoundedSemaphore(4)
        name = f"parallel-k{args.k}"
        prop = LocalClaudeProposer(ad.spec.channels["proposer"], audit_dir=ad.root / "audit" / name)
        out = run_domain(AREA, args.tasks, args.k, adapter=ad, prop=prop,
                         runs_root=ad.spec.runs_root, library_root=ad.root / "library" / name,
                         modes=(mode_token("parallel"),))
        out["improver_model"] = IMPROVER
        out["improver_usd"] = round(sum(c.cost_usd for c in prop._calls), 4)
        out["improver_calls"] = len(prop._calls)
        (ad.root / f"sweep-{name}.json").write_text(json.dumps(out, indent=2, default=str))
        print(out["done"], out["failed"], "improver_usd", out["improver_usd"])
    elif args.phase == "adopted":
        sel = adopted(ad.root, args.k)
        roll_and_judge(ad, "h2", [(t, sel[t][0], r) for t in args.tasks if t in sel
                                  for r in range(1, args.reps + 1)], args.width)
    elif args.phase == "transfer":  # memorisation check: a task's adopted harness on other tasks
        h = adopted(ad.root, args.k)[args.src][0]
        roll_and_judge(ad, f"xfer-from-{args.src.split('/')[-1]}",
                       [(t, h, r) for t in args.tasks if t != args.src
                        for r in range(1, args.reps + 1)], args.width)
    elif args.phase == "audit":
        audit(ad.root)
    else:
        report(ad.root, args.tasks)


def norm(s: str) -> str:
    """Whitespace, quotes and markdown escapes folded, so a quoted sentence matches its source."""
    s = s.translate(str.maketrans("‘’“”", "\'\'\"\"")).replace("\\", "")
    return " ".join(s.split())


def audit(root: Path) -> None:
    """Rubric leak audit over everything a model-driven process saw or wrote: improver tool
    streams, improver context trees, harnesses, library, executor streams. A hit is a
    verbatim 60-char slice of any criterion, the rubric's field names, or the LAB task path."""
    needles = {"match_criteria", '"criteria"', "harvey-labs/tasks"}
    for t in TASKS:
        # criteria quote the documents; a slice the data room also contains is not a leak
        docs = norm(" ".join(docx_text(p, "all") for p in (LAB / "tasks" / t / "documents").iterdir()))
        for c in criteria(t):
            mc = c["match_criteria"]
            needles |= {s for i in range(0, max(len(mc) - 60, 1), 60)
                        if norm(s := mc[i:i + 60]) not in docs}
    scanned, hits, blocked = 0, [], 0
    for f in [*(root / "audit").rglob("*"), *(root / "runs").rglob("*"),
              *(root / "library").rglob("*"), *(root / "exec").rglob("stream.jsonl")]:
        if not f.is_file() or f.suffix in (".docx", ".pptx", ".xlsx", ".pdf"):
            continue
        text = f.read_text(errors="replace")
        scanned += 1
        blocked += text.count("Operation not permitted")
        hits += [(str(f.relative_to(root)), n[:40]) for n in needles if n in text]
    print(f"scanned {scanned} files; rubric hits: {len(hits)}; 'Operation not permitted': {blocked}")
    for h in hits[:20]:
        print("  HIT", h)
    instance_audit(root)


def instance_literals(task_id: str) -> set[str]:
    """Matter literals of one task: proper nouns not in the system dictionary, and numbers
    with 3+ digits, from its data room. Generic rule names (ICC, SIAC) are noise both ways."""
    words = {w.strip().lower() for w in open("/usr/share/dict/words")}
    text = " ".join(docx_text(p, "all") for p in (LAB / "tasks" / task_id / "documents").iterdir())
    names = {w for w in re.findall(r"\b[A-Z][A-Za-zÀ-ÿ]{2,}\b", text) if w.lower() not in words}
    nums = {n for n in re.findall(r"(?<![\w.])\d[\d,.]*\d(?![\w])", text)
            if sum(ch.isdigit() for ch in n) >= 3 and not re.fullmatch(r"(19|20)\d\d", n)}
    return names | nums


def instance_audit(root: Path) -> dict[str, dict]:
    """Per adopted harness: its own task's matter literals (the leak) vs other tasks' (control).
    Literals shared by two or more tasks are dropped as generic."""
    lits = {t: instance_literals(t) for t in TASKS}
    common = {x for t in TASKS for x in lits[t] if sum(x in lits[u] for u in TASKS) > 1}
    out = {}
    for t, (h, is_base) in adopted(root, 1).items():
        text = "\n".join(f.read_text(errors="replace") for f in h.rglob("*") if f.is_file())
        found = lambda s: sorted(x for x in s - common if re.search(rf"(?<![\w.]){re.escape(x)}(?![\w])", text))
        own = found(lits[t])
        other = sorted({x for u in TASKS if u != t for x in found(lits[u])})
        tree = {str(f.relative_to(h)): f.read_text(errors="replace") for f in h.rglob("*") if f.is_file()}
        lg = leakguard.scan_tree(tree, LabAdapter(root).instance(t))
        out[t] = {"tree_is_base": is_base, "own": own, "other": other, "chars": len(text),
                  "leakguard": lg}
        print(f"  {t.split('/')[-1]}: base={is_base} chars={len(text)} own-matter literals={len(own)} "
              f"{own[:12]} | other tasks' literals={len(other)} {other[:6]}")
    (root / "instance_audit.json").write_text(json.dumps(out, indent=1))
    return out


def report(root: Path, tasks: list[str]) -> None:
    """Per-task partial scores, check-level flips versus base, and cost, as markdown."""
    rows = [json.loads(f.read_text()) for f in sorted((root / "eval").glob("*/*.json"))]
    rows = [r for r in rows if "partial" in r]  # infra failures and judge failures are not scored
    by = lambda cond, t: [r for r in rows if r["cond"] == cond and r["task"] == t]
    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")
    conds = sorted({r["cond"] for r in rows} - {"base"})
    exec_usd: dict[str, float] = {}  # Harness² improvement-phase rollouts, by task
    for m in (root / "exec").glob("lab-*/**/meta.json"):
        d = json.loads(m.read_text())
        exec_usd[d["task"]] = exec_usd.get(d["task"], 0.0) + float(d.get("cost_usd") or 0.0)
    sweep = json.loads((root / "sweep-parallel-k1.json").read_text()) \
        if (root / "sweep-parallel-k1.json").is_file() else {}
    print("| task | checks | base (R) | " + " | ".join(f"{c} (R) | Δ pts | gained / lost checks"
                                                 for c in conds) + " |")
    print("|" + "---|" * (3 + 3 * len(conds)))
    deltas = {c: [] for c in conds}
    for t in tasks:
        b = by("base", t)
        if not b:
            continue
        cells = [t.split("/")[-1], str(b[0]["n_criteria"]),
                 f"{100 * mean([r['partial'] for r in b]):.1f} ({len(b)})"]
        for c in conds:
            h = by(c, t)
            if not h:
                cells += ["—", "—", "—"]
                continue
            d = 100 * (mean([r["partial"] for r in h]) - mean([r["partial"] for r in b]))
            deltas[c].append(d)
            rate = lambda rs, k: mean([1.0 if r["checks"][k] else 0.0 for r in rs])
            ks = b[0]["checks"].keys()
            gained = sum(rate(b, k) < .5 < rate(h, k) for k in ks)
            lost = sum(rate(h, k) < .5 < rate(b, k) for k in ks)
            cells += [f"{100 * mean([r['partial'] for r in h]):.1f} ({len(h)})", f"{d:+.1f}",
                      f"{gained} / {lost}"]
        print("| " + " | ".join(cells) + " |")
    for c in conds:
        print(f"\nmean Δ ({c}): {mean(deltas[c]):+.1f} pts over {len(deltas[c])} tasks")
    xf = [c for c in conds if c.startswith("xfer-from-")]
    if xf:  # held-out: each adopted harness on the tasks its improver never saw
        short = lambda t: t.split("/")[-1]
        print("\nheld-out Δ pts vs base (R) | rows: harness adopted on | cols: scored on")
        print("| adopted on | " + " | ".join(short(t) for t in tasks) + " | mean |")
        print("|" + "---|" * (len(tasks) + 2))
        alld = []
        for c in xf:
            ds, cells = [], []
            for t in tasks:
                h, b = by(c, t), by("base", t)
                if not h or not b:
                    cells.append("—")
                    continue
                d = 100 * (mean([r["partial"] for r in h]) - mean([r["partial"] for r in b]))
                ds.append(d)
                cells.append(f"{d:+.1f} ({len(h)})")
            alld += ds
            print(f"| {c[len('xfer-from-'):]} | " + " | ".join(cells) + f" | {mean(ds):+.1f} |")
        print(f"\nmean held-out Δ: {mean(alld):+.1f} pts over {len(alld)} cells")
    print("\n| task | base exec $/rollout | judge $/run | H2 improvement rollouts $ |")
    print("|---|---|---|---|")
    for t in tasks:
        b = by("base", t)
        if b:
            print(f"| {t.split('/')[-1]} | {mean([r['cost_usd'] or 0 for r in b]):.2f} | "
                  f"{mean([r['judge_usd'] for r in rows if r['task'] == t]):.2f} | "
                  f"{exec_usd.get(t, 0):.2f} |")
    total = sum((r.get("cost_usd") or 0) + r["judge_usd"] for r in rows) \
        + sum(exec_usd.values()) + float(sweep.get("improver_usd") or 0)
    print(f"\nimprover ({sweep.get('improver_model')}): ${sweep.get('improver_usd')} over "
          f"{sweep.get('improver_calls')} sessions; all scored eval + improvement: ${total:.2f}")


if __name__ == "__main__":
    main()
