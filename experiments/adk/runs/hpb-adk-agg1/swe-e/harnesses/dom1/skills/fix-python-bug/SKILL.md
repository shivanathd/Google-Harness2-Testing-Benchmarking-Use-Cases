---
name: fix-python-bug
description: Practitioner checklist for resolving a bug report in a small Python codebase without breaking it - docstring-as-spec, test handling, edge-case matrix, parser/validator pitfalls, delivery copy.
---

# Fix a bug in a small Python codebase

ANALYTIC MOVE: reconcile three sources -- the bug report (symptom), the docstring/spec (controlling source for "fully meets"), and the existing tests (regression floor, never the whole spec) -- then change the code until all agree.

## 1. Before editing
- Read the target source, `tests/`, and `tests/conftest.py`. conftest often puts `src/` on `sys.path`; that only works under pytest. Run tests as `python3 -m pytest tests -q` from the workspace root. Running `python3 tests/test_x.py` directly fails with ModuleNotFoundError because conftest is not loaded -- that is a harness mistake, NOT a bug to "fix" by editing imports, adding `__init__.py`, or moving files.
- Reproduce the reported symptom with a one-off `python3 -c` call before changing code.
- Split the docstring into numbered, individually testable requirements (one per sentence/clause). The reported symptom is usually only one of them; the task says "fully meets its docstring", so every clause must hold.

## 2. Hard rules for what you touch
- NEVER overwrite, truncate or rewrite an existing test file or the import lines in it. A failing test run is information about the source or the command, not a reason to edit tests. To add coverage, append new test functions (or add a new file) and keep every existing test intact.
- Do not add files to `src/` (no `__init__.py`), rename the function, or change its signature unless asked.
- Edit with a targeted replacement of the function body, not by re-writing the whole file from a partial read. Keep the docstring.
- After editing, `git diff`-style check: the only changed existing files should be the one named in the task. Re-read the file you wrote.

## 3. Edge-case matrix (build it from the docstring, then run it)
For each docstring clause, test at least one accepting and one rejecting input, and compare actual vs expected values in a single script. For parser/validator functions also cover:
- empty string, whitespace-only, only a number with no unit ("30"), only a unit ("h"), trailing/leading garbage ("1h30", "1h x", "abc");
- unknown unit ("5d", "1x"), negative/sign/decimal ("-5s", "1.5h", "+5s");
- repeated unit ("1h1h"), out-of-order units ("30m1h"), zero values ("0s" is valid -> 0);
- case ("1H30M"), whitespace around and between parts ("  2h 5m 10s  ", "1h  30m");
- non-ASCII digits: `\d` matches e.g. Arabic-Indic digits in Python 3 str patterns; use `[0-9]` if only ASCII is meant;
- non-str input only if the docstring says so.
Prefer validating the WHOLE string with one anchored pattern (`re.fullmatch`, with optional groups per unit in required order) over `re.findall`/`re.search`, which silently skip garbage -- the classic cause of "returns 0 for valid input" plus "accepts invalid input". Make sure the empty/blank case raises ValueError rather than returning 0 (every group optional matches ""), and that a failing match raises ValueError, not returns a default.
- Workspace fact (this task, `src/durations.py`): the original regex `(\d+)([hm])` omits `s` (cause of `'45s' -> 0`), is unanchored, ignores case, order, repeats and garbage. Docstring requirements: units h/m/s; case-insensitive; whitespace around and between parts; each unit at most once in h-m-s order; ValueError for empty input, unknown units, non-duration text. Existing test only covers "1h30m" == 5400. Whether whitespace between a number and its own unit ("1 h") is allowed is not stated -- choose the stricter reading (parts are number+unit, whitespace only around/between parts) and say so in the final message.

## 4. Finish
- Run the full existing suite with pytest plus your edge-case script; report any failure honestly with output.
- Copy the final source file to the exact path the task names (here `output/durations.py`), e.g. `mkdir -p output && cp src/durations.py output/durations.py`, then diff the two to confirm identical.
- Final message: root cause, what changed, which edge cases were verified, any ambiguity resolved by judgment.
