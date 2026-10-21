[ACTION] load_skill {"name": "fix-python-bug"}
[OBSERVATION]
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

[ACTION] list_files {"path": "src"}
[OBSERVATION]
src/durations.py
[ACTION] read_file {"path": "src/durations.py", "start_line": 0, "max_lines": 200}
[OBSERVATION]
[14 lines total]
import re


def parse_duration(text: str) -> int:
    """Convert a duration such as "1h30m", "45s" or "2h 5m 10s" to seconds.

    Units are h, m and s, case-insensitive; whitespace around and between parts is
    allowed. Each unit may appear at most once, in h-m-s order. Raise ValueError for
    empty input, unknown units, or text that is not a duration.
    """
    total = 0
    for num, unit in re.findall(r"(\d+)([hm])", text):
        total += int(num) * (3600 if unit == "h" else 60)
    return total
[ACTION] read_file {"max_lines": 200, "path": "tests/test_durations.py", "start_line": 0}
[OBSERVATION]
[5 lines total]
from durations import parse_duration


def test_hours_minutes():
    assert parse_duration("1h30m") == 5400
[ACTION] run_command {"command": "python3 -c \"from durations import parse_duration; print(parse_duration('45s'))\""}
[OBSERVATION]
exit=1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from durations import parse_duration; print(parse_duration('45s'))
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'durations'. Did you mean: 'fractions'?

[ACTION] run_command {"command": "python3 -m pytest -q tests/test_durations.py"}
[OBSERVATION]
exit=0
.                                                                        [100%]
1 passed in 0.01s

[ACTION] run_command {"command": "python3 -c \"from durations import parse_duration; print(parse_duration('45s'))\""}
[OBSERVATION]
exit=1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from durations import parse_duration; print(parse_duration('45s'))
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'durations'. Did you mean: 'fractions'?

[ASSISTANT] The `ModuleNotFoundError` suggests that the `durations` module is not being found when executed from the command line. This could be due to the current working directory not being set to the workspace directory. Let's fix this by running the command from the workspace directory and then proceed with the bug fix. 

First, I'll run the command from the workspace directory to ensure the module is found. Then, I'll proceed to fix the bug in the `parse_duration` function. 

Let's start by running the command from the workspace directory.