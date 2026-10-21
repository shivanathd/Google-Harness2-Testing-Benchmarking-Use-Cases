KEEP_BASE. I changed no files.

The single rollout (base1) went through the right steps:
- **Read first:** it read `src/durations.py` and the test file before editing.
- **Fix matched the docstring:** its one edit replaced the regex with a `fullmatch` parser. That covers `s`, case-insensitivity, whitespace, h-m-s order with each unit at most once, and `ValueError` for empty or malformed input.
- **Checked beyond the existing test:** it ran its own script from a scratch directory with `python3 -I`. The script covered the docstring examples and 12 invalid inputs. It also ran the existing test.
- **Checked the deliverable:** it created `output/` and copied the file. It confirmed the copy with `cmp`, and `deliverables/base1/output__durations.py.txt` is identical to the fixed `src/durations.py`.
- **Reported the one judgement call:** `"1 h"` raises `ValueError`, and the summary says how to allow it.

I found no tool error, repeated mechanical step, skipped invariant or budget problem that a skill, script or plugin would address. Any added always-on text would cost context on every run for no demonstrated gain. The remaining risks are one-off judgement calls (for example, whether `\d` should accept non-ASCII digits). I did not turn those into process rules because no run diverged on them.

I did not run the fixed code myself. My conclusion rests on the rollout's own check output and on reading the fixed file in the deliverables.