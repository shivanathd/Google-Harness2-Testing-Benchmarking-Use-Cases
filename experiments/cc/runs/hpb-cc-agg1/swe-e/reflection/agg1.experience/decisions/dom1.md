KEEP_BASE. I changed no harness files.

I read `task.md`, the source, the harness and the only rollout, `base1`. The harness is empty apart from a one-line system prompt. The `base1` run produced a correct fix without any guidance.

- **Docstring clauses:** The agent enumerated each clause of the docstring: units h/m/s, case-insensitive, whitespace around and between parts, each unit at most once in h-m-s order, and `ValueError` for empty, unknown or malformed input. It replaced the lossy `re.findall` with a `re.fullmatch` pattern that covers all of them.
- **Verification:** It ran its own check script covering valid inputs, including `"45s"` and `"2h 5m 10s"`, and 12 invalid inputs. It confirmed the existing test still passed and that `output/durations.py` matches `src/durations.py`.
- **Judgement call:** It flagged that `"1 h"` is rejected. The docstring only allows whitespace between parts, so this is a defensible reading.
- **Not changed:** The function name and signature are unchanged.

Two small gaps are visible in the rollout. The agent did not add a regression test to `tests/test_durations.py`. The pattern's `\d` also accepts non-ASCII digits. Neither is a failure, and with one correct run there is no divergence or repeated error to justify always-on text or a new skill. Adding either would cost context on every run and fix nothing observed.