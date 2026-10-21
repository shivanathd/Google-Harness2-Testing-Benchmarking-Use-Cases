---
name: fix-python-bug
description: Practitioner checklist for resolving a bug report in a small Python codebase - turning the docstring into a contract, fixing the cause, proving it with tests, and not breaking existing behaviour.
---

# Analytic move
TRACE the reported symptom to its root cause in the source, then RECONCILE the implementation against its docstring (the controlling spec; the bug report is only one example of a violation).

# Steps
1. Read the target source file and every test file (read-only). Existing tests are protected fixtures: NEVER overwrite, truncate or rewrite them. Add new tests only by appending to them or in a new file (e.g. tests/test_<module>_extra.py).
2. Turn the docstring into a numbered list of clauses (accepted forms, units, case, whitespace, ordering/uniqueness, each error condition and exception type). The reported symptom is usually only one of several clauses the code violates. Compare the code to EVERY clause, not just the one reported.
3. Reproduce first: run the failing example in a one-liner (`python3 -c ...` with `sys.path` set to src/) and see the actual wrong output before editing.
4. Fix the cause with a minimal edit to the source file only (use Edit, not a full rewrite). Keep function name, signature, return type and imports that others may use.
5. Probe edges against the contract, one case per clause. For a parser: empty and whitespace-only string, unknown unit, number without unit, unit without number, garbage before/between/after parts (a regex `findall` silently skips junk - use fullmatch/anchored parsing so non-matching text raises), duplicate unit, wrong order, uppercase, inner/outer whitespace, zero values, leading zeros, a non-str input if the docstring implies it. Invalid input must raise the documented exception, never return 0 or a partial result.
6. Run the suite with `python3 -m pytest -q` from the workspace root (the existing conftest/test files already handle imports; do NOT edit tests or add `__init__.py` to fix import errors - a "No module named" error means you ran the wrong command, e.g. executing a test file as a script). Run it before and after the change; the previously passing tests must still pass.
7. Copy the final source to the requested output path with `cp` (byte-identical) and `diff` the two. Confirm the deliverable file is the fixed version, not the original.

# Before finishing, confirm
- existing tests unchanged (diff vs. original) and passing; new tests cover each docstring clause;
- every docstring error clause is raised with the exception type the docstring names;
- output file exists and equals the fixed source.
