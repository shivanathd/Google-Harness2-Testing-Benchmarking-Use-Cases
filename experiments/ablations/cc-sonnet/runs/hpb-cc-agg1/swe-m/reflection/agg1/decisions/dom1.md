**What I read:** `task.md`, the harness, `source/`, the only rollout (`base1`), and the library's `swe-e` harness. I did not run any harness code.

**What `base1` did:**
- It read the docs, ran the baseline, and found that the existing test already fails because the code returns a float.
- It then made two edits: `rate_for` now upper-cases the region and raises ValueError, and `totals.py` was rewritten with Decimal and half-up rounding.
- The trajectory stops there. It never re-ran the tests and never wrote `output/CHANGES.md`, which the task requires.
- It never read the root `CLAUDE.md`, although its first `ls` listed that file.
- Its code looks right on a read-through, but nothing in the trajectory confirms it, and there are no regression tests.

**Changes:**
1. `systemprompt.md` (replaced the one-line base text).
   - Why: the `base1` run ended right after the edits, with no test run and no `CHANGES.md`.
   - The new text says to treat the cited doc as the spec and the issue as samples only. It says to read `CLAUDE.md`, and to write `output/CHANGES.md` as soon as the fix passes the existing tests. It also says never to end a turn right after an edit.
   - The library's `swe-e` lesson says to keep the write-the-deliverable-early rule in the always-on prompt, not in a skill. I followed that. Its confidence is low, since it rests on one rollout per variant.
   - The same file holds the trigger line for the new skill.

2. New skill `skills/spec-doc-money-fix/SKILL.md`, loaded for money, rounding, tax, discount or docs-rules issues.
   - **Clause checklist:** each doc bullet maps to a code line and a test. It covers the string-with-two-decimals return format, the order of operations (discount before tax), rounding at each step the doc names, case-insensitive region codes, and ValueError raised before any arithmetic.
   - **Decimal pitfalls:** build Decimals from the strings, never from floats. Use `quantize` with `ROUND_HALF_UP`, not `round()`. `sum()` needs a Decimal start value for empty input. Check other callers if a helper's return type changes.
   - **Hand-computed values for this workspace:** the ISSUE example gives subtotal "59.97", discount "6.00", tax "10.79" and total "64.76". A 0.125 unit price gives "0.13", and qty 3 gives "0.38". RATES are listed, and an unknown region raises ValueError. These are labelled as workspace facts to recompute.
   - **Tests and `CHANGES.md`:** the tests to add, and what `CHANGES.md` should contain: files changed, one line per symptom and per extra doc clause, tests added, and the test result.
   - The skill does not change the deliverable's shape. `CHANGES.md` stays short, as the task asks.

I made no changes to guardrails, memory, tool guidance, scripts or plugins, because the single rollout gives no evidence for them.