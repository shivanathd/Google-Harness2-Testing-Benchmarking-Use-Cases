"""HPB-9: a small trap-laden benchmark for testing Harness² outside Vertex.

Three domains x three tasks. Every task writes into output/ and is graded by code
that lives only here (never copied into a workspace or shown to the improver).
"""

from __future__ import annotations

import csv
import shutil
import datetime as dt
import io
import json
import random
import re
import subprocess
import sys
import tempfile
import uuid
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import tiers

# ---------------------------------------------------------------- ledger

FX = {"USD": Decimal("1"), "EUR": Decimal("1.0850"), "INR": Decimal("0.01195")}
MONTHS = {8: "August", 9: "September", 10: "October"}


def gen_ledger(seed: int, month: int) -> tuple[dict[str, str], dict]:
    rng = random.Random(seed)
    rows, net, counted = [], Decimal(0), 0
    for i in range(36):
        in_month = rng.random() < 0.75
        m = month if in_month else month + rng.choice((-1, 1))
        date = dt.date(2026, m, rng.randint(1, 28))
        cur = rng.choice(("USD", "USD", "EUR", "INR"))
        amt = Decimal(rng.randint(500, 250000)) / 100 * (80 if cur == "INR" else 1)
        neg = rng.random() < 0.2
        status = rng.choices(("SETTLED", "VOID", "PENDING"), (0.75, 0.12, 0.13))[0]
        plain = f"{amt:.2f}"
        grouped = f"{amt:,.2f}"
        if neg:
            text = rng.choice((f"-{plain}", f"({grouped})"))
        else:
            text = rng.choice((plain, grouped))
        datestr = date.isoformat() if rng.random() < 0.6 else date.strftime("%b %d, %Y")
        row = [f"T{seed}{i:03d}", datestr, text, cur, status]
        rows.append(row)
        if rng.random() < 0.15:  # double import: an exact duplicate row
            rows.append(list(row))
        if in_month and status == "SETTLED":
            net += (-amt if neg else amt) * FX[cur]
            counted += 1
    rng.shuffle(rows)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["txn_id", "date", "amount", "currency", "status"])
    w.writerows(rows)
    fx = "currency,usd_per_unit\n" + "".join(f"{c},{r}\n" for c, r in FX.items())
    expected = {
        "net_usd": float(net.quantize(Decimal("0.01"), ROUND_HALF_UP)),
        "transactions": counted,
    }
    return {"transactions.csv": buf.getvalue(), "fx.csv": fx}, expected


def ledger_prompt(month: int) -> str:
    return (
        "transactions.csv is a payment-processor export and fx.csv gives the USD value of "
        "one unit of each currency. Compute the net settled revenue in USD for "
        f"{MONTHS[month]} 2026: include only transactions with status SETTLED dated in that "
        "month; refunds are negative amounts and reduce revenue. A txn_id identifies one "
        "transaction. Write output/answer.json as "
        '{"net_usd": <number rounded to 2 decimals>, "transactions": <number of '
        "transactions included>}."
    )


# ---------------------------------------------------------------- logs

USERS = ("alice", "bob", "chen", "diya", "eve", "farid", "gita", "hiro")
CODES = ("E401", "E403", "E500", "E502", "E504")
SVCS = ("auth", "billing", "search", "gateway")
TZS = (dt.timedelta(0), dt.timedelta(hours=5, minutes=30), dt.timedelta(hours=-7),
       dt.timedelta(hours=1))


def _stamp(t: dt.datetime, off: dt.timedelta) -> str:
    local = (t + off).replace(tzinfo=dt.timezone(off))
    s = local.isoformat(timespec="seconds")
    return s.replace("+00:00", "Z") if off == dt.timedelta(0) else s


def gen_logs(seed: int, start: dt.datetime) -> tuple[dict[str, str], dict]:
    rng = random.Random(seed)
    end = start + dt.timedelta(hours=3)
    events = []
    span = int(dt.timedelta(hours=9).total_seconds())
    for _ in range(130):
        t = start - dt.timedelta(hours=3) + dt.timedelta(seconds=rng.randrange(span))
        events.append((t, rng.choices(("INFO", "WARN", "ERROR"), (0.58, 0.15, 0.27))[0]))
    events.sort()
    lines, errs = [], []
    for t, level in events:
        ts, svc, user = _stamp(t, rng.choice(TZS)), rng.choice(SVCS), rng.choice(USERS)
        code = rng.choice(CODES)
        if level == "ERROR":
            lines.append(f"{ts} ERROR [{svc}] user={user} code={code} msg=request failed")
            if rng.random() < 0.4:
                lines += [
                    "    Traceback (most recent call last):",
                    f'      File "/srv/{svc}/handler.py", line {rng.randint(20, 300)}, in handle',
                    f"    RuntimeError: upstream ERROR user={rng.choice(USERS)} "
                    f"code={rng.choice(CODES)}",
                ]
            if start <= t < end:
                errs.append((user, code))
        elif level == "WARN":
            lines.append(f"{ts} WARN [{svc}] user={user} code={code} msg=slow response")
        elif rng.random() < 0.3:
            lines.append(f"{ts} INFO [{svc}] user={user} msg=retrying after ERROR code={code}")
        else:
            lines.append(f"{ts} INFO [{svc}] user={user} msg=ok")
    counts = Counter(c for _, c in errs).most_common()
    if len(counts) > 1 and counts[0][1] == counts[1][1]:  # break a tie in the data itself
        t = start + dt.timedelta(minutes=7)
        lines.append(f"{_stamp(t, TZS[0])} ERROR [auth] user=alice code={counts[0][0]} "
                     "msg=request failed")
        errs.append(("alice", counts[0][0]))
    expected = {
        "errors": len(errs),
        "users": len({u for u, _ in errs}),
        "top_code": Counter(c for _, c in errs).most_common(1)[0][0],
    }
    return {"app.log": "\n".join(lines) + "\n"}, expected


def logs_prompt(start: dt.datetime) -> str:
    end = start + dt.timedelta(hours=3)
    return (
        "app.log aggregates several services running in different timezones; every "
        "timestamp carries its UTC offset. For the window "
        f"{start:%Y-%m-%d %H:%M} (inclusive) to {end:%H:%M} (exclusive) UTC, find the number "
        "of ERROR-level log events, the number of distinct users with at least one "
        "ERROR-level event, and the most frequent error code among those events. Write "
        'output/answer.json as {"errors": <int>, "users": <int>, "top_code": "<code>"}.'
    )


# ---------------------------------------------------------------- grading

TOL = {"net_usd": 0.05, "error_rate": 0.0005, "p95_ms": 1}


def _leaves(d, prefix=""):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from _leaves(v, f"{prefix}{k}.")
        else:
            yield f"{prefix}{k}", k, v


def grade_json(work: Path, exp: dict) -> dict:
    """One check per expected leaf (numeric tolerance for money/rates); invalid JSON fails all."""
    checks = {path: False for path, _, _ in _leaves(exp)}
    try:
        ans = json.loads((work / "output/answer.json").read_text())
        assert isinstance(ans, dict)
    except Exception:  # no or invalid answer file: every check fails
        return checks
    for path, key, want in _leaves(exp):
        got = ans
        try:
            for part in path.split("."):
                got = got[part]
            if isinstance(want, str):
                checks[path] = str(got).strip() == want
            elif key in TOL:
                checks[path] = abs(float(got) - want) <= TOL[key]
            else:
                checks[path] = int(got) == want and float(got) == float(want)
        except Exception:
            pass
    return checks


DURATIONS_SRC = '''import re


def parse_duration(text: str) -> int:
    """Convert a duration such as "1h30m", "45s" or "2h 5m 10s" to seconds.

    Units are h, m and s, case-insensitive; whitespace around and between parts is
    allowed. Each unit may appear at most once, in h-m-s order. Raise ValueError for
    empty input, unknown units, or text that is not a duration.
    """
    total = 0
    for num, unit in re.findall(r"(\\d+)([hm])", text):
        total += int(num) * (3600 if unit == "h" else 60)
    return total
'''

DURATIONS_CASES = [
    ("seconds", 'parse_duration("45s") == 45'),
    ("all_units_spaced", 'parse_duration("2h 5m 10s") == 7510'),
    ("uppercase", 'parse_duration("1H30M") == 5400'),
    ("zero", 'parse_duration("0m") == 0'),
    ("outer_space", 'parse_duration(" 1h ") == 3600'),
    ("empty_raises", 'raises(lambda: parse_duration(""))'),
    ("unknown_unit_raises", 'raises(lambda: parse_duration("5x"))'),
    ("garbage_raises", 'raises(lambda: parse_duration("abc"))'),
    ("repeat_unit_raises", 'raises(lambda: parse_duration("1h1h"))'),
    ("order_raises", 'raises(lambda: parse_duration("30m1h"))'),
]

RUNNER_HEAD = '''import json, sys
sys.path.insert(0, sys.argv[1])
def raises(fn):
    try:
        fn()
    except ValueError:
        return True
    except Exception:
        return False
    return False
'''

RUNNER_TAIL = '''
out = {}
# eval: the expressions are this file's own constant test cases, never agent input.
for name, expr in CASES:
    try:
        out[name] = bool(eval(expr))
    except Exception:
        out[name] = False
print(sys.argv[2] + json.dumps(out))
'''


def grade_pkg(work: Path, spec: dict) -> dict:
    """Run hidden test expressions against a copy of the agent's code in a temp dir."""
    cases = spec["cases"]
    res = {}
    with tempfile.TemporaryDirectory() as td:
        code = Path(td) / "code"
        code.mkdir()
        for rel, src_rel in spec["copy"]:
            src = work / src_rel
            if src.is_dir():
                shutil.copytree(src, code / rel)
            elif src.is_file():
                shutil.copy(src, code / rel)
        runner = Path(td) / "runner.py"
        runner.write_text(RUNNER_HEAD + spec["prelude"] + f"\nCASES = {cases!r}\n" + RUNNER_TAIL)
        nonce = f"HPB-{uuid.uuid4().hex}:"
        try:
            p = subprocess.run([sys.executable, "-I", str(runner), str(code), nonce],
                               capture_output=True, text=True, timeout=60, cwd=td)
            line = next(x for x in p.stdout.splitlines() if x.startswith(nonce))
            res = json.loads(line[len(nonce):])
        except Exception:
            res = {}
    return {name: bool(res.get(name)) for name, _ in cases}


# ---------------------------------------------------------------- registry

SWE_PROMPT = (
    "Resolve the issue described in ISSUE.md. Keep existing public function names and "
    "signatures. tests/ holds the existing tests (run them with `python -m pytest tests` if "
    "pytest is available, or plain python). When you are done, write a short summary of "
    "your changes to output/CHANGES.md."
)


def _registry() -> dict[str, dict]:
    reg = {}

    def add(tid, domain, tier, files, prompt, expected=None, pkg=None):
        reg[tid] = dict(domain=domain, tier=tier, files=files, prompt=prompt,
                        expected=expected or {}, pkg=pkg)

    files, exp = gen_ledger(11, 9)
    add("data-e", "data", "easy", files, ledger_prompt(9), exp)
    files, exp, prompt = tiers.data_medium()
    add("data-m", "data", "medium", files, prompt, exp)
    files, exp, prompt = tiers.data_hard()
    add("data-h", "data", "hard", files, prompt, exp)

    start = dt.datetime(2026, 10, 3, 9, tzinfo=dt.timezone.utc)
    files, exp = gen_logs(5, start)
    add("ops-e", "ops", "easy", files, logs_prompt(start), exp)
    files, exp, prompt = tiers.ops_medium()
    add("ops-m", "ops", "medium", files, prompt, exp)
    files, exp, prompt = tiers.ops_hard()
    add("ops-h", "ops", "hard", files, prompt, exp)

    add("swe-e", "swe", "easy",
        {"src/durations.py": DURATIONS_SRC,
         "tests/test_durations.py": "from durations import parse_duration\n\n\n"
                                    "def test_hours_minutes():\n"
                                    '    assert parse_duration("1h30m") == 5400\n',
         "tests/conftest.py": "import pathlib\nimport sys\n\n"
                              "sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / \"src\"))\n"},
        "Bug report: parse_duration(\'45s\') returns 0 instead of 45. Fix src/durations.py so "
        "the function fully meets its docstring. tests/test_durations.py holds the existing "
        "tests. Keep the function name and signature. When you are done, also copy the final "
        "file to output/durations.py.",
        pkg={"cases": DURATIONS_CASES, "prelude": "from durations import parse_duration\n",
             "copy": [("durations.py", "src/durations.py")]})
    add("swe-m", "swe", "medium", tiers.SWE_M_FILES, SWE_PROMPT,
        pkg={"cases": tiers.SWE_M_CASES, "prelude": tiers.SWE_M_PRELUDE,
             "copy": [("invoicing", "invoicing")]})
    add("swe-h", "swe", "hard", tiers.SWE_H_FILES, SWE_PROMPT,
        pkg={"cases": tiers.SWE_H_CASES, "prelude": tiers.SWE_H_PRELUDE,
             "copy": [("stock", "stock")]})
    # Fresh-seed variants: same task family and prompt shape, new data. Used only to check
    # whether an adopted harness memorised its instance.
    files, exp = gen_ledger(12, 9)
    add("data-e-v", "data", "easy", files, ledger_prompt(9), exp)
    files, exp, prompt = tiers.data_medium(seed=42)
    add("data-m-v", "data", "medium", files, prompt, exp)
    files, exp, prompt = tiers.data_hard(seed=54)
    add("data-h-v", "data", "hard", files, prompt, exp)
    files, exp = gen_logs(6, start)
    add("ops-e-v", "ops", "easy", files, logs_prompt(start), exp)
    files, exp, prompt = tiers.ops_medium(seed=62)
    add("ops-m-v", "ops", "medium", files, prompt, exp)
    files, exp, prompt = tiers.ops_hard(seed=72)
    add("ops-h-v", "ops", "hard", files, prompt, exp)
    for tid in reg:
        reg[tid]["variant"] = tid.endswith("-v")
    return reg


TASKS = _registry()
DOMAINS = {d: [t for t, v in TASKS.items() if v["domain"] == d and not v["variant"]]
           for d in ("data", "ops", "swe")}
TASK_HASH = __import__("hashlib").sha256(
    repr(sorted((k, v["prompt"], sorted(v["files"])) for k, v in TASKS.items())).encode()
    + json.dumps({k: v["expected"] for k, v in TASKS.items()}, sort_keys=True).encode()
).hexdigest()[:12]


_INSTANCE_ID = re.compile(r"\b(?:T1\d{4}|S0\d\d|ch_\d{3}|cb_\d|R\d\d|r\d{6})\b")


def own_literals(task_id: str) -> set[str]:
    """Pre-registered leak rule (PREREG.md): the task's expected answers (strings, non-integer
    floats, ints >= 10) plus the instance ids found in its .csv/.log/.md/extension-less files."""
    lits = set()

    def walk(d):
        for v in d.values():
            if isinstance(v, dict):
                walk(v)
            elif isinstance(v, str) or (isinstance(v, float) and v != int(v)) or abs(v) >= 10:
                lits.add(str(v))
    walk(TASKS[task_id]["expected"])
    for rel, body in TASKS[task_id]["files"].items():
        if isinstance(body, str) and Path(rel).suffix in (".csv", ".log", ".md", ""):
            lits |= set(_INSTANCE_ID.findall(body))
    return lits


def leaked(text: str, task_id: str) -> list[str]:
    """The task's own literals that occur in text as whole tokens."""
    return sorted(x for x in own_literals(task_id)
                  if re.search(rf"(?<![\w.]){re.escape(x)}(?![\w])", text))


def write_task_files(task_id: str, dest: Path) -> None:
    for rel, body in TASKS[task_id]["files"].items():
        p = dest / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(body, bytes):
            p.write_bytes(body)
        else:
            p.write_text(body, encoding="utf-8")
    (dest / "output").mkdir(exist_ok=True)


def grade(work: Path, task_id: str) -> dict:
    t = TASKS[task_id]
    if t["pkg"]:
        checks = grade_pkg(work, t["pkg"])
    else:
        checks = grade_json(work, t["expected"])
    passed = sum(checks.values())
    return {"partial": passed / len(checks), "all_pass": passed == len(checks), "checks": checks,
            "n_passed": passed, "n_criteria": len(checks)}


def _selftest() -> None:
    """Graders score the untouched workspace low and the reference solution 1.0."""
    for tid, t in TASKS.items():
        with tempfile.TemporaryDirectory() as td:
            w = Path(td)
            write_task_files(tid, w)
            untouched = grade(w, tid)["partial"]
            assert untouched < (0.75 if t["pkg"] else 0.01), (tid, untouched)
            if t["pkg"]:
                ref = Path(__file__).parent / "reference" / tid
                shutil.copytree(ref, w, dirs_exist_ok=True)
            else:
                (w / "output/answer.json").write_text(json.dumps(t["expected"]))
            g = grade(w, tid)
            assert g["all_pass"], (tid, g)
        print(f"ok {tid:7s} {t['tier']:6s} checks={len(g['checks']):2d} untouched={untouched:.2f} "
              f"expected={t['expected'] or '(hidden tests)'}")


if __name__ == "__main__":
    _selftest()
