**What went wrong in base1.** The single rollout never produced `output/answer.json`. It ended with `LlmCallsLimitExceededError` (40-call cap) after running the same crashing command about 32 times in a row. The trace shows these moments:
1. The agent wrote a pandas script. `ModuleNotFoundError` followed, then a pip install that timed out.
2. It then hit `ValueError: could not convert string to float: '(954.34)'`. It re-ran the identical command with no edit until the cap.
3. The script had other latent bugs. It filtered September with `str.contains('Sep')`, which misses ISO dates like `2026-09-15`. It didn't dedupe `txn_id`. It would have written a list-shaped JSON via `to_json(orient='records')` instead of the requested object.

**Changes** (all on disk in `context/harness/`):
- **`scripts/net_revenue.py`** (new, stdlib-only). This is the mechanical-extraction fix: it replaces the hand-rolled pandas script that crashed. It does the following:
  - Parses both date styles, and amounts with thousands separators, plain negatives and parenthesised negatives.
  - Counts each `txn_id` once, and reports exact versus conflicting duplicates.
  - Filters on SETTLED status and the parsed month.
  - Multiplies by `usd_per_unit`, rounds half-up to 2 decimals, and writes `{"net_usd","transactions"}`.
  - Re-reads the file to check its shape, and exits non-zero with a message on any unparseable value rather than guessing.
  - I ran it on the workspace source: 36 unique txn_ids, 6 exact-duplicate rows skipped, and the output was `{"net_usd": 18691.64, "transactions": 21}`.
  - I replaced `scripts/README.md` with this script. I deleted the README only because the script now occupies the directory.
- **`systemprompt.md`** (short additions):
  - Tool-error handling for the observed pandas/pip failure: Python is stdlib-only, don't retry installs, never re-run a failed command unchanged, and change approach if the same error appears twice. This targets the 32-fold repetition.
  - Sequencing: inspect the whole input once and list the formats present, write the deliverable early, and reopen it to check its shape. The shape check means a single JSON object with exactly the requested keys. Keep scratch scripts out of `output/`.
  - Workspace facts, labelled as such: date styles, amount styles, duplicate txn_id rows, statuses, and fx units. It also names the one-line script invocation.
- **No skill and no hook.** The failure was a loop that hit the call cap, not a stop-time skip or a recurring triggered procedure. A Stop hook would not have fired, so it isn't justified by this evidence.