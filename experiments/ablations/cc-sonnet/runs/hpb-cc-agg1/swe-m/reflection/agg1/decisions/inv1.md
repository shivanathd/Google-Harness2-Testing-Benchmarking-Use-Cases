**Evidence.** There is one rollout, `base1`.
- It read the issue, docs and source, and ran the baseline tests. One test already failed, because `test_simple_us` expects `"20.00"` and the code returned a float.
- It then edited `invoicing/tax.py` and `invoicing/totals.py` (Decimal math, tax after discount, `region.upper()`, `ValueError` for an unknown region).
- The trajectory ends right after those two edits. It never re-ran the tests, never ran the issue's examples, and never wrote `output/CHANGES.md`, which `task.md` requires.
- It also never opened `CLAUDE.md`, although `ls` showed it.
- The earliest divergence is the missing deliverable and missing verification after the last edit.
- The library entry `swe-e` records a similar failure: a run ended before the output file existed. Its lesson was that the copy-to-output rule belongs in always-on text, written right after the first edit, and that a skill alone did not work. It also saw no evidence that a Stop hook or script fired.
- I treated that lesson as a hypothesis only, and I'm not asserting it from experience here.

**Changes.**
1. `systemprompt.md` now holds a short issue-fix workflow, in always-on text.
   - It says to read `ISSUE.md`, `CLAUDE.md`, the spec docs, the source and the tests.
   - It says to satisfy every issue bullet and every spec rule, including return types and formats, rounding, case handling and error types.
   - It says to write `output/CHANGES.md` right after the first fix edit and update it after later edits.
   - It says to verify with the existing tests plus a script that reproduces each issue bullet and edge cases.
   - It says to add regression tests to `tests/`.
   - It says to finish only when tests pass or any failure is explained, and to re-read `CHANGES.md` once.
   - Motivation: `base1` stopped after its edits with no deliverable and no verification. A workspace fact is encoded as procedure: in this workspace a baseline test already fails, because the existing test expected strings.
   - I kept this in always-on text rather than a skill because the `swe-e` evidence says the skill version hurt. The prompt is short and has no template braces.
2. I added `scripts/check_done.py` and a Stop hook, `hooks.json`.
   - The script checks that `output/CHANGES.md` exists and is non-empty, and that `python -m pytest tests` does not exit with failures (return code 1).
   - If pytest is missing or times out, it lets the run finish.
   - It exits 2 with the reason on stderr, and the runner caps blocking at 3 attempts, so valid completion is never blocked for good.
   - I tested it by hand in a scratch directory: it blocks on a missing `CHANGES.md` or a failing test, and passes when both are fine.
   - Motivation: the `base1` run ended with no `CHANGES.md` and unrun tests. This is the "exit before a deliverable exists" case. The `swe-e` hook never visibly fired, so this one is a backstop and the prompt rule is the main lever.

I made no edits to `guardrails.md`, `LongTermMEMORY.md`, tool guidance, skills or sub-agents, because no trajectory moment motivated them.