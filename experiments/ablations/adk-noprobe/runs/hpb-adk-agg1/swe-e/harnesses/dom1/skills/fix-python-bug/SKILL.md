---
name: fix-python-bug
description: Practitioner checklist for resolving a bug report or docstring-conformance issue in a small Python repo (src/ + tests/) without breaking it. Use before editing source, and again before finishing.
---

# Fix a bug in a small Python codebase

## Analytic move: reconcile three sources
The bug report gives ONE symptom; the docstring/spec is the CONTRACT; the existing tests are a PARTIAL sample of it. "Fully meets its docstring" means the report's symptom is only the first failing case, not the whole job. A fix that makes the reported input pass but leaves other docstring clauses violated is incomplete.

1. Read the source file, the tests, and `tests/conftest.py` (if present) first. Note how tests import the module (e.g. the test file may insert `src/` into `sys.path` itself). Never change imports or layout to make tests run.
2. Split the docstring into numbered clauses (accepted inputs, each rule, each error condition, return type/units). Write the list down. Each clause needs at least one probe input that should succeed and one that should raise/fail.
3. Reproduce BEFORE editing: run the probes against the current code and confirm the reported symptom. If you cannot get anything to run, fix the invocation, not the code under test.
4. Run tests with `python3 -m pytest tests -q` from the workspace root (test files are pytest-style functions with no `__main__` block; `python3 tests/test_x.py` runs nothing useful). If pytest is missing, import the test module and call its `test_*` functions directly. A run that executes zero tests is not a pass.

## Hard rules
- NEVER overwrite, truncate or rewrite existing tests or conftest. Their content is the repo's regression guard. You may ADD new tests (append to the file or add a new `tests/test_*.py`), never delete or weaken existing ones.
- Do not create `__init__.py`, move files, or alter `sys.path` setup as a way to get past an import error; read the traceback and the conftest/test header to see how imports are intended to work.
- Keep the function name and signature exactly. Keep the docstring.
- Make the edit minimal but complete. A write that reproduces the existing file unchanged is not a fix: diff or re-read the file after writing and confirm the intended change is actually there.
- Do not stop on a tool/import failure: after at most two failed attempts at the same approach, change approach (different command, absolute path, `python3 -m pytest`) rather than editing unrelated files.

## Parsing/validation functions (string -> value) — expert checks
When the function parses text and the docstring says "raise ValueError for ...":
- Validate the WHOLE string: use `re.fullmatch` (not `match`/`search`/`findall`, which silently skip junk; avoid `$`, which accepts a trailing newline). `findall` ignoring non-matching text is the classic cause of "returns 0 instead of raising".
- Use `[0-9]` rather than `\d` (which accepts non-ASCII digits) unless the spec allows them.
- Empty and whitespace-only input must raise, not return 0.
- Honor stated case-insensitivity (`re.IGNORECASE` or `.lower()`), stated whitespace tolerance (leading/trailing/between parts), "at most once" and ordering constraints (encode them in the pattern with optional groups in the required order, so duplicates and out-of-order parts fail), and "at least one part present".
- For unit-suffixed formats, probe: a number with no unit, a unit with no number, unknown units, signs/decimals, duplicate and out-of-order parts. Each is invalid -> ValueError unless the spec says otherwise.
- Raise `ValueError` (with a message), not a bare return value or other exception type. Return the documented type and units. A zero value is valid and must be distinguished from invalid input.
- Where the spec is ambiguous (e.g. whitespace between a number and its unit), choose the reading most consistent with the docstring examples and say so in the final report; do not silently narrow what the examples show works.

## Before finishing — confirm each
1. Every docstring clause has a probe that you actually ran and the output matched (list success cases and error cases).
2. The full test suite passes with a non-zero test count, and original tests are byte-for-byte unchanged (re-read the test file).
3. New regression tests for the reported symptom and for the other clauses were ADDED (not replacing existing ones).
4. The source file differs from the original in the intended way (re-read it).
5. Any required deliverable copy (e.g. `output/<file>.py` named in the task) exists and is identical to the final source file; do the copy LAST, after the final edit.
6. Final message states what was wrong, what changed, what was tested, and any ambiguity decisions.
