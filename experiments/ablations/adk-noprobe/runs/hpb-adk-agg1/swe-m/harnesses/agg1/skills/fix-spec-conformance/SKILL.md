---
name: fix-spec-conformance
description: Practitioner checklist for resolving an ISSUE.md that says a function must "follow docs/X.md" (money/rounding/tax/region rules, parsing rules) in a small Python repo. Covers reconciling issue vs. spec doc vs. tests, and Decimal money pitfalls.
---

# Resolve an issue against a written spec (ISSUE.md + docs/*.md)

## Analytic move: reconcile three sources, then trace each spec clause to code
- ISSUE.md lists SYMPTOMS (a sample). The docs/ file is the CONTRACT. tests/ is a thin sample and may pass on broken code. The job is every clause of the doc, not only the listed symptoms.
- Do: (1) read ISSUE.md, the docs file, every module the function calls (not just the named one, e.g. a helper module for rates), and tests/. (2) Number each spec bullet. (3) For each, name the line of code that implements it and whether it is wrong. (4) Fix, then run a probe per clause with hand-computed expected values.
- Bugs often live in a helper the issue does not name (lookup tables, normalisers). Fix them where they are, keeping public names and signatures.
- Files are at the workspace root; there may be no `src/`. The only required deliverable is the one the task names; the code fix is made in place. Do not stop after announcing a plan: the work is the edit plus the probes.

## Money / rounding rules (Decimal)
- Build every Decimal from a STRING (`Decimal(str(x))` for ints/strs). Never `Decimal(float)`; never `float()`; never builtin `round()` (it is float and half-even).
- Round with `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` exactly at the points the spec names, in the spec's order; do not round earlier/later or fold steps together (per-line rounding then summing differs from rounding the sum).
- Output is the type the spec says: money as str with exactly two decimals (`format(d, ".2f")` on the quantized value), including "0.00" for empty input and a zero amount. Check every key of the returned dict, not just `total`.
- Percentages: `x * pct / 100` in Decimal. Taxable base is what the spec states (e.g. net of discount), and the total formula sign for each term must match the spec text literally.
- Keys that are case-insensitive: normalise (`.strip().upper()` or per spec) in the lookup function; an unknown key must raise the exception type the spec names (`ValueError`), not leak `KeyError`. Use `raise ValueError(...) from None`.

## Tests
- Check what the existing tests cover. If they pass on the broken code they prove nothing about the issue: never edit them; add a new test file with hand-computed cases per spec clause (include a half-cent rounding case, a mixed-case key, an unknown key, and an empty/zero input).

## Before finishing, confirm each
1. Each spec bullet has a probe you ran whose output matched your hand-computed value (list them).
2. Every symptom listed in ISSUE.md was reproduced before the edit or is covered by a probe after it.
3. Every returned amount is `str` with two decimals; no float remains in the money path (grep for `float(` and `round(`).
4. Public function names/signatures unchanged; original tests untouched and passing with a non-zero count.
5. The deliverable the task names (e.g. a CHANGES file) says what was wrong (per symptom and per spec clause), what changed in which file, and what was tested.
