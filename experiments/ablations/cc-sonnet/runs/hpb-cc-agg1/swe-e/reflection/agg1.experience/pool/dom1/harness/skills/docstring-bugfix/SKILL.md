---
name: docstring-bugfix
description: Fix a bug in a small Python function whose docstring states the contract; turns the docstring into a checklist, tests each clause, and delivers the file.
---

# Fixing a function against its docstring

The bug report names ONE symptom; the docstring is the controlling spec and usually lists more
requirements than the symptom shows. The existing tests are only a floor (often a single case).

1. CLASSIFY: split the docstring into atomic clauses (accepted inputs, units, case, whitespace,
   ordering, repetition, each error condition, return type/units). Write them as a numbered list.
2. TRACE: for each clause, name the input that exercises it and the exact expected value or
   exception. Include at least one input that must be REJECTED per clause (empty, whitespace-only,
   unknown unit, bare number with no unit, wrong order, repeated unit, stray characters, negative
   or signed numbers, interior junk) and the boundary where it is merely tolerated (leading/trailing
   whitespace, mixed case, a part omitted, zero values).
3. Prefer one anchored whole-string match (fullmatch/strict parse) over scanning with findall:
   scanning silently skips junk, which violates every "raise ValueError" clause. Reject results
   where nothing was parsed. Keep the function name, signature, and the docstring text.
4. EXPECTED VALUES: compute them by hand from the arithmetic, once, carefully, and write the sum out
   (e.g. h*3600 + m*60 + s). If a check disagrees with the code, recompute the expectation before
   touching the code -- decide which side is wrong. In this workspace the example "2h 5m 10s"
   is 7200+300+10 = 7510 (an earlier run asserted 7335 and wrongly suspected the code).
5. Add regression tests to the existing tests file (keep the existing test), covering every clause
   from step 2, then run the full test file. Ambiguous case (e.g. space between number and unit,
   "1 h"): follow the docstring literally -- it allows whitespace around and between PARTS -- and
   state the choice in your final message rather than guessing silently.
6. DELIVER: the task's required copy (in this workspace output/durations.py, a byte-identical copy
   of src/durations.py) must exist when you finish. Create it right after the first passing edit,
   and re-copy after any later edit; then `diff` the two. A failing self-check is not a reason to
   end without the deliverable.
7. FINAL MESSAGE: list which docstring clauses you verified and any behaviour you chose where the
   docstring is silent.
