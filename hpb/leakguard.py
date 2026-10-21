"""Answer-leak detector for adopted harnesses (defence in depth on top of bench.leaked).

A harness may teach a method. It must not carry facts about the one instance it was tuned on.
Flags, per file:
  answer   - the task's own expected values (numbers compared after normalisation)
  datum    - a distinctive number or id that occurs in the instance data
  entity   - case-specific proper nouns from the source documents (3+ distinct)
  verbatim - an 8-word passage copied from the source data or documents
  fact     - "workspace fact" style phrasing
Anything that also occurs in the task's own instructions (prompt, POLICY/RUNBOOK/ISSUE/docs
.md files) is allowed: restating a stated rule is method, not a leak.

  python leakguard.py                      # self-check
  python leakguard.py audit <root> [...]   # audit every adopted harness under experiment roots
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import tempfile
import zipfile
from decimal import Decimal, InvalidOperation
from pathlib import Path

FACT_RX = re.compile(r"(?i)workspace facts?\b|task instance|reference check for this workspace"
                     r"|verified (?:here|in this workspace|on the files)|in this (?:workspace|matter|data room)")
ID_RX = re.compile(r"\b(?=[A-Za-z_-]*\d)[A-Za-z]+[_-]?\d{2,}\b")
NUM_RX = re.compile(r"(?<![\w.])[-(]?\d[\d,]*(?:\.\d+)?\)?(?![\w])")
WORD_RX = re.compile(r"[A-Za-z][A-Za-z'’-]+")
PROPER_RX = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})*")
INSTRUCTION_SUFFIXES = (".md",)
DATA_SUFFIXES = (".csv", ".log", ".jsonl", ".json", ".txt", ".py", ".gz", ".1", ".2", ".docx", "")
COMMON = set("""The This That These Those When Where What Which While With Without Write Read Run Use
Return Keep Never Always Only Each Every Before After Then Also First Second Third Note Rules Rule
Step Steps Task Tasks Output Input File Files Script Scripts Skill Skills Harness Python JSON CSV
Monday Tuesday Wednesday Thursday Friday Saturday Sunday January February March April May June July
August September October November December UTC USD EUR INR JPY""".split())


def norm_num(tok: str) -> str | None:
    t = tok.strip("()").replace(",", "").lstrip("-")
    if sum(c.isdigit() for c in t) < 3:  # 1-2 digit numbers occur everywhere
        return None
    try:
        d = Decimal(t)
    except InvalidOperation:
        return None
    return format(d.normalize(), "f")


def numbers(text: str) -> set[str]:
    return {n for n in (norm_num(m.group(0)) for m in NUM_RX.finditer(text)) if n}


def specific(n: str) -> bool:
    """A number specific enough to identify an instance: a non-zero decimal, or an integer
    of 1000 or more. Small integers (status codes, limits, counts like 100) are vocabulary."""
    return ("." in n and n.strip("0.") != "") or (n.isdigit() and int(n) >= 1000)


def read_text(p: Path) -> str:
    if p.suffix == ".gz":
        return gzip.decompress(p.read_bytes()).decode(errors="replace")
    if p.suffix == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode(errors="replace")
        return re.sub(r"<[^>]+>", " ", xml)
    return p.read_text(errors="replace")


def ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    w = [x.lower() for x in WORD_RX.findall(text)]
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


class Instance:
    """What is instance-specific about one task: data minus its own instructions."""

    def __init__(self, sources: Path, instructions: str, answers: list = ()):
        data, docs = [], [instructions]
        for f in sorted(p for p in Path(sources).rglob("*") if p.is_file()):
            if f.name.endswith(INSTRUCTION_SUFFIXES) and f.stat().st_size < 200_000:
                docs.append(read_text(f))
            elif f.suffix in DATA_SUFFIXES or f.name.endswith((".gz", ".docx")):
                try:
                    data.append(read_text(f))
                except Exception:
                    pass
        allowed = "\n".join(docs)
        blob = "\n".join(data)
        self.allowed_nums, self.allowed_words = numbers(allowed), set(WORD_RX.findall(allowed))
        self.allowed_ids = set(ID_RX.findall(allowed))
        self.answers = {norm_num(str(a)) or str(a) for a in answers if str(a).strip()}
        self.data_nums = {n for n in numbers(blob) - self.allowed_nums if specific(n)}
        counts: dict[str, int] = {}
        for i in ID_RX.findall(blob):
            counts[i] = counts.get(i, 0) + 1
        # rare ids identify records (T11007, ch_013); labels repeated across rows (E500) are vocabulary
        self.data_ids = {i for i, c in counts.items() if c <= 2} - self.allowed_ids
        self.entities = {e for e in PROPER_RX.findall(blob) if e.split()[0] not in COMMON
                         and not set(e.split()) <= self.allowed_words}
        self.grams = ngrams(blob) - ngrams(allowed)

    def scan(self, text: str) -> dict[str, list[str]]:
        hits: dict[str, list[str]] = {}
        nums, ids = numbers(text), set(ID_RX.findall(text))
        words = set(PROPER_RX.findall(text))
        if a := sorted(x for x in self.answers if x in nums or x in ids or
                       (not x[0].isdigit() and re.search(rf"(?<![\w]){re.escape(x)}(?![\w])", text))):
            hits["answer"] = a
        if d := sorted((nums & self.data_nums) | (ids & self.data_ids)):
            hits["datum"] = d[:20]
        if len(e := sorted(words & self.entities)) >= 3:
            hits["entity"] = e[:20]
        if v := ngrams(text) & self.grams:
            hits["verbatim"] = [" ".join(g) for g in list(v)[:3]]
        if f := sorted({m.group(0) for m in FACT_RX.finditer(text)}):
            hits["fact"] = f
        return hits


def scan_tree(tree: dict[str, str], inst: Instance) -> dict[str, dict]:
    return {rel: h for rel, src in sorted(tree.items()) if not rel.endswith("README.md")
            and (h := inst.scan(src))}


def message(found: dict[str, dict]) -> str:
    """Rejection text for the improver: what leaked and what to do instead."""
    parts = [f"{rel}: " + "; ".join(f"{k} {', '.join(map(str, v[:6]))}" for k, v in h.items())
             for rel, h in found.items()]
    return ("The harness records facts about this one instance (" + " | ".join(parts) + "). "
            "A harness must teach the method and let the agent re-derive every value from the "
            "files at run time: remove results, counts, ids, names, dates and quoted passages "
            "that come from this task's data. Rules stated in the task's own instructions may stay.")


# ------------------------------------------------------------------ audit + self-check

def _hpb_instance(root: Path, task: str) -> Instance:
    import bench
    t = bench.TASKS[task]

    def leaves(d):
        for v in d.values():
            yield from (leaves(v) if isinstance(v, dict) else [v])
    src = root / "sources" / task
    if not src.is_dir():  # a fresh clone has no generated sources; bench writes the same files
        src = Path(tempfile.mkdtemp()) / task
        bench.write_task_files(task, src)
    return Instance(src, t["prompt"], list(leaves(t["expected"])))


def audit(roots: list[Path]) -> dict:
    """Scan every adopted harness (summary-selected) and every frozen autoresearch harness."""
    out = {}
    for root in roots:
        for summ in root.glob("runs/*-agg*/*/summary.json"):
            d = json.loads(summ.read_text())
            for mode, sel in (d.get("selections") or {}).items():
                label = sel.get("chosen_label")
                if not label or sel.get("chosen_tree_is_base"):
                    continue
                ns = summ.parent.parent.name.replace("-agg", f"-{mode}", 1)
                h = root / "runs" / ns / d["task_id"] / "harnesses" / label
                if not h.is_dir():
                    continue
                tree = {str(p.relative_to(h)): p.read_text(errors="replace") for p in h.rglob("*") if p.is_file()}
                try:
                    inst = _hpb_instance(root, d["task_id"])
                except Exception:
                    continue  # non-HPB roots (e.g. LAB) are audited by their own adapter
                out[str(h)] = scan_tree(tree, inst)
    return out


def _selfcheck() -> None:
    sys.path.insert(0, str(Path(__file__).parent))
    root = Path(__file__).resolve().parent.parent / "experiments" / "adk"
    inst = _hpb_instance(root, "ops-e")
    leak = "- Workspace fact (this app.log): script gives errors=15, users=6, top_code=E500."
    assert {"answer", "fact"} <= set(inst.scan(leak)), inst.scan(leak)
    clean = "Normalise every timestamp to UTC, skip continuation lines, count ERROR-level events only."
    assert not inst.scan(clean), inst.scan(clean)
    d = _hpb_instance(root, "data-e")
    assert "datum" in d.scan("duplicated ids T11007 and T11010; T11002 is -1,638.49"), d.scan("T11007 -1,638.49")
    assert not _hpb_instance(root, "ops-h").scan("Count status >= 500 as errors; 404 and 429 are client errors; "
                                                "a 0.00 total means nothing matched; E500 is a code"), "vocabulary flagged"
    assert "answer" in d.scan("net_usd should come out near 18,691.640"), "normalised answer"
    h = _hpb_instance(root, "data-h")
    assert not h.scan("Each chargeback costs a 15.00 USD fee (POLICY.md rule 5)."), "policy constant allowed"
    old = root / "runs/hpb-adk-agg1/ops-h/harnesses/agg1"
    if old.is_dir():  # study 1's leaky ops-h harness must be caught
        tree = {str(p.relative_to(old)): p.read_text() for p in old.rglob("*") if p.is_file()}
        assert scan_tree(tree, _hpb_instance(root, "ops-h")), "study-1 ops-h leak missed"
    print("leakguard self-check: ok")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    if len(sys.argv) > 2 and sys.argv[1] == "audit":
        res = audit([Path(r).resolve() for r in sys.argv[2:]])
        bad = {k: v for k, v in res.items() if v}
        for k, v in bad.items():
            print(k.split("experiments/")[-1], json.dumps(v)[:300])
        print(f"audited {len(res)} adopted harnesses; flagged {len(bad)}")
    else:
        _selfcheck()
