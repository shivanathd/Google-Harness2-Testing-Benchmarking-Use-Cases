---
name: fix-python-bug
description: Checklist for resolving a bug report in a small Python codebase - docstring as contract, real fix, edge-case probes, protected tests, verified output copy.
---

# Steps
1. Read the target source, every test file and conftest.py (read-only). Existing tests are protected: never overwrite or truncate them. Add new tests only by appending, or in a new file such as tests/test_<module>_extra.py.
2. Turn the docstring into a numbered list of clauses (accepted forms, units, case, whitespace, ordering/uniqueness, each error condition and the exception type). The reported symptom is usually only one clause the code violates; compare the code to EVERY clause.
3. Reproduce first: `PYTHONPATH=src python3 -c "..."` with the reported example, and see the wrong output before editing.
4. Fix the cause. write_file replaces the whole file, so send the complete corrected source; keep the function name, signature, return type and imports. Then re-read or diff to confirm it changed.
5. Probe each clause. For a parser: empty and whitespace-only input, unknown unit, number without unit, unit without number, junk before/between/after parts (regex `findall` silently skips junk; use anchored/fullmatch parsing so non-matching text raises), duplicate unit, wrong order, uppercase, inner/outer whitespace, zero and leading-zero values. Invalid input must raise the documented exception, never return 0 or a partial result.
6. Run `python3 -m pytest -q tests` from the workspace root. Previously passing tests must still pass. Do not add `__init__.py` or edit tests to fix an import error.
7. Copy the final source to the requested output path with `cp` and `diff` the two. Confirm the copy is the fixed version, not the original.
