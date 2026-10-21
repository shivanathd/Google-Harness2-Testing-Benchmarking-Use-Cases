[ACTION] load_skill {"name": "fix-python-bug"}
[OBSERVATION]
---
name: fix-python-bug
description: Practitioner checklist for resolving an issue in a small Python repo, esp. money/rounding/tax code where a spec doc (docs/*.md) is the controlling source. Covers spec-to-clauses, root-cause tracing, protected tests, CHANGES.md contents.
---

# Analytic move
TRACE each symptom in ISSUE.md to a line of code, then RECONCILE the code against EVERY clause of the controlling spec (the doc the issue names, e.g. docs/ROUNDING.md), not only the reported symptoms. Issue bullets are usually a subset of the spec violations.

# Steps
1. Read ISSUE.md, the named spec doc, EVERY source file under the package (including helpers such as tax.py / models.py, where a bug may live), and tests/. Do this before saying what you will do. Existing tests are protected: never overwrite them; add new tests only in a new file (tests/test_<module>_extra.py).
2. Number the spec clauses (type of every returned value, rounding mode and WHERE each rounding happens, formula order, case/whitespace handling, which exception for bad input). Mark which clause each code line violates. Also check the existing tests' expectations: a test that currently fails is a clause the code violates (return type), not a test to change.
3. Edit the source files in place under the package (not a copy in output/). Keep public function names, signatures, return shape (same dict keys). Replace the whole function body rather than patching around float code.
4. Probe: run the issue's examples with `python3 -c` (from the workspace root, package importable) and compare to hand-computed expected values, then run `python3 -m pytest -q tests` (or plain python if pytest is missing).
5. Write output/CHANGES.md (a short summary; it is the requested deliverable, so create it even if everything else is done): per file what changed and why, mapped to each issue bullet and spec clause, plus what you tested. Do not end the run before it exists.

# Money / rounding checklist (apply when the spec says Decimal / cents)
- Build Decimals from strings (`Decimal(item.unit_price)`, `Decimal(rate_string)`), never from float; int qty and int pct are exact in Decimal.
- Round with `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`. Python's `round()` is banker's/float and is wrong here (0.125 -> 0.13 half-up; float round gives 0.12).
- Round at each step the spec names (line gross, line discount, tax), then SUM the rounded values; do not sum raw values and round once.
- Follow the spec's formula order literally: tax base = subtotal - discount (net of discount), total = subtotal - discount + tax.
- Return every amount as a str with exactly two decimals (`format(x, "f")` after quantize, or `str` of a quantized Decimal). Empty item list -> "0.00" for all four keys. Check that "-0.00" cannot appear.
- Region lookup: normalize case (and strip) once, and an unknown region must raise ValueError (a bare KeyError from a dict lookup is a spec violation). If the lookup lives in a helper (rate_for), fix it there so every caller gets the behaviour; keep its signature.

# Before finishing
- Hand-compute one example by the spec (including a half-cent case) and confirm the output equals it; confirm differently-cased/spaced inputs give identical results and bad input raises the spec's exception.
- Confirm any test failing before your change now passes without editing that test.

[ACTION] list_files {"path": "workspace"}
[OBSERVATION]
ERROR: ValueError: no such directory: 'workspace' (paths are relative to the workspace root)
[ACTION] list_files {"path": "/"}
[OBSERVATION]
ERROR: ValueError: path is outside the workspace
[ACTION] list_files {"path": "/home/runner/work/fix-python-bug/fix-python-bug"}
[OBSERVATION]
ERROR: ValueError: path is outside the workspace
[ACTION] list_files {"path": "/home/runner/work/fix-python-bug/fix-python-bug"}
[OBSERVATION]
ERROR: ValueError: path is outside the workspace
[ACTION] list_files {"path": "/home/runner/work/fix-python-bug/fix-python-bug"}
[OBSERVATION]
ERROR: ValueError: path is outside the workspace
[ASSISTANT] It seems there is an issue with accessing the workspace directory. Let me try a different approach to resolve this. I'll attempt to list the files in the current working directory to identify the correct path.