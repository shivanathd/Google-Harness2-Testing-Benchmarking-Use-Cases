[ACTION] Bash {"command": "find . -type f -not -path '*/.git/*' | head -100 && echo --- && cat ISSUE.md", "description": "List workspace files and read the issue"}
[OBSERVATION]
./tests/test_totals.py
./.claude/settings.json
./docs/ROUNDING.md
./ISSUE.md
./scripts/check_done.py
./invoicing/tax.py
./invoicing/models.py
./invoicing/__init__.py
./invoicing/totals.py
./CLAUDE.md
---
# #142 Invoice totals wrong for discounted EU invoices

Reported by finance:

- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")` raises KeyError.
- With "EU" the tax is charged on the undiscounted amount.
- Totals are sometimes a cent off (float rounding), e.g. a 0.125 unit price.

Please make `invoicing.totals.compute_totals` follow docs/ROUNDING.md.
[ACTION] Bash {"command": "for f in CLAUDE.md docs/ROUNDING.md invoicing/__init__.py invoicing/models.py invoicing/tax.py invoicing/totals.py tests/test_totals.py scripts/check_done.py .claude/settings.json; do echo \"=== $f\"; cat \"$f\"; echo; done", "description": "Print docs, source, tests, and config files"}
[OBSERVATION]
=== CLAUDE.md
## systemprompt.md

You are an assistant that completes tasks inside a workspace directory. Read the task, do the work, and write the requested deliverables under output/.

Issue-fix workflow (small Python repos):
1. Read ISSUE.md, CLAUDE.md, any doc the issue points to (docs/*.md is the spec), every source file and the tests. The existing tests are only a sample of the spec; one may already fail before you touch anything.
2. Fix the code so every bullet of the issue AND every rule of the spec holds (types/formats of returned values, rounding, case handling, error types), not just the quoted example. Keep public names and signatures.
3. Write output/CHANGES.md as soon as the fix is edited (`mkdir -p output`), then verify; update it if you change the fix later. Do this before extended verification so a failed check can never leave the deliverable missing.
4. Verify by running: the existing tests, plus a short script that reproduces each issue bullet and edge cases from the spec (empty input, unknown/odd-case input, half-cent ties). Work out expected values by hand with exact arithmetic; if a check fails, decide whether the code or your expectation is wrong before editing. Add regression tests for the issue bullets to tests/.
5. Finish only when the tests pass (or you can state why a failure is pre-existing/unrelated) and output/CHANGES.md exists. Re-read it once: it should say what changed and why, and what you ran.

A failing command is information to read, not the end of the task. `python3 -I` ignores PYTHONPATH and the cwd; use plain `python -m pytest tests` from the workspace root.

=== docs/ROUNDING.md
# Money rules

- All money is computed with `decimal.Decimal`, never float, and every amount that
  `compute_totals` returns is a string with exactly two decimals, e.g. "12.30".
- Line gross = qty x unit_price, rounded half-up to cents.
- Line discount = line gross x discount_pct / 100, rounded half-up to cents.
- subtotal = sum of line gross; discount = sum of line discounts.
- tax = (subtotal - discount) x the region's rate, rounded half-up to cents.
- total = subtotal - discount + tax.
- Region codes are case-insensitive. An unknown region raises ValueError.

=== invoicing/__init__.py

=== invoicing/models.py
from dataclasses import dataclass


@dataclass
class LineItem:
    description: str
    qty: int
    unit_price: str  # decimal string, e.g. "19.99"
    discount_pct: int = 0

=== invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    return RATES[region]

=== invoicing/totals.py
from .tax import rate_for


def line_total(item):
    return round(item.qty * float(item.unit_price), 2)


def compute_totals(items, region):
    subtotal = sum(line_total(i) for i in items)
    tax = round(subtotal * float(rate_for(region)), 2)
    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)
    total = subtotal + tax - discount
    return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}

=== tests/test_totals.py
from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"

=== scripts/check_done.py
#!/usr/bin/env python3
"""Stop-hook check: output/CHANGES.md exists and is non-empty, and tests/ passes.

Usage: python3 scripts/check_done.py   (run from the workspace root)
Exit 0 when fine (or pytest/tests are unavailable, so nothing can be checked);
exit 2 with an instruction on stderr otherwise. Never loops forever: the runner
caps blocking at a few attempts.
"""
import os
import subprocess
import sys


def main():
    problems = []
    path = os.path.join("output", "CHANGES.md")
    if not os.path.isfile(path) or not open(path, encoding="utf-8", errors="replace").read().strip():
        problems.append(f"{path} is missing or empty: write a short summary of what changed, why, and what you ran")
    if os.path.isdir("tests"):
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-x", "--no-header"],
                               capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr)
            if r.returncode == 1:
                problems.append("tests fail; fix the code (or state in CHANGES.md why a failure is unrelated):\n" + out[-1200:])
        except (subprocess.TimeoutExpired, OSError):
            pass
    if problems:
        print("Not done yet:\n- " + "\n- ".join(problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

=== .claude/settings.json
{"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "python3 scripts/check_done.py"}]}]}}
[ACTION] Bash {"command": "python -m pytest tests -q 2>&1 | tail -15", "description": "Run existing tests for baseline"}
[OBSERVATION]
F                                                                        [100%]
=================================== FAILURES ===================================
________________________________ test_simple_us ________________________________

    def test_simple_us():
>       assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
E       AssertionError: assert 20.0 == '20.00'

tests/test_totals.py:6: AssertionError
=========================== short test summary info ============================
FAILED tests/test_totals.py::test_simple_us - AssertionError: assert 20.0 == ...
1 failed in 1.48s
[ASSISTANT] The baseline already fails: `test_simple_us` expects the string `"20.00"` but gets the float `20.0`, which the spec also rules out. Next I'll fix the module: Decimal arithmetic, half-up rounding, tax on the net amount, and string output.
[ACTION] Edit {"replace_all": false, "file_path": "./invoicing/totals.py", "old_string": "from .tax import rate_for\n\n\ndef line_total(item):\n    return round(item.qty * float(item.unit_price), 2)\n\n\ndef compute_totals(items, region):\n    subtotal = sum(line_total(i) for i in items)\n    tax = round(subtotal * float(rate_for(region)), 2)\n    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)\n    total = subtotal + tax - discount\n    return {\"subtotal\": subtotal, \"discount\": discount, \"tax\": tax, \"total\": total}", "new_string": "from decimal import ROUND_HALF_UP, Decimal\n\nfrom .tax import rate_for\n\nCENT = Decimal(\"0.01\")\n\n\ndef _cents(value):\n    return value.quantize(CENT, rounding=ROUND_HALF_UP)\n\n\ndef line_total(item):\n    return _cents(item.qty * Decimal(item.unit_price))\n\n\ndef compute_totals(items, region):\n    rate = Decimal(rate_for(region))\n    subtotal = _cents(sum((line_total(i) for i in items), Decimal(\"0\")))\n    discount = _cents(sum((_cents(line_total(i) * i.discount_pct / 100) for i in items), Decimal(\"0\")))\n    tax = _cents((subtotal - discount) * rate)\n    total = _cents(subtotal - discount + tax)\n    return {\"subtotal\": str(subtotal), \"discount\": str(discount), \"tax\": str(tax), \"total\": str(total)}"}
[ACTION] Edit {"replace_all": false, "file_path": "./invoicing/tax.py", "old_string": "def rate_for(region):\n    return RATES[region]", "new_string": "def rate_for(region):\n    try:\n        return RATES[region.upper()]\n    except KeyError:\n        raise ValueError(f\"unknown region: {region!r}\") from None"}
[OBSERVATION]
The file ./invoicing/totals.py has been updated successfully.
[OBSERVATION]
The file ./invoicing/tax.py has been updated successfully.