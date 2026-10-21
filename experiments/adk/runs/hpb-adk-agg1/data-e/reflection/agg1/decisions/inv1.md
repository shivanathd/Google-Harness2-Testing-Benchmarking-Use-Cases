**Evidence:** There is one rollout, base1. It ran out of calls (`LlmCallsLimitExceededError`, limit 40) and `answer.json` was never written.

**What went wrong in base1**
1. It wrote its script to `output/process_transactions.py`, which put scratch code in the deliverables folder.
2. It ran `import pandas`. pandas was missing, so the attempt to install it timed out.
3. It then ran the same command about 30 times, each failing on `ValueError: could not convert string to float: '(954.34)'`. It never edited the script between runs. This is the main failure and the one every change below targets.
4. The script was also wrong in other ways:
   - It filtered months with `str.contains('Sep')`, so ISO dates like `2026-09-15` would have been missed.
   - It didn't handle accounting negatives.
   - It didn't dedupe by `txn_id`, even though the file has 6 byte-identical repeated rows.
   - It wrote JSON as a list of records, not the `{"net_usd":..., "transactions":...}` object the task asks for.

**Changes**
- **`scripts/settled_revenue.py` (new).**
  - It uses only the standard library, since pandas isn't available.
  - It parses both date formats, thousands commas, and `(x)` or `-x` negatives.
  - It counts each `txn_id` once, converts with `fx.csv`, and filters on month and status.
  - It fails with exit 2 and writes nothing if a row has an unparseable date or amount, or a currency missing from fx.
  - It writes the answer in the requested shape and then re-reads the file to confirm it.
  - It prints audit lines covering duplicates dropped, rows excluded by reason, and the included count.
  - I ran it on the workspace sources and it produced `net_usd` 18691.64 over 21 transactions for 2026-09. That figure is hard-coded in `systemprompt.md` as a cross-check; I did not check it independently.
- **`systemprompt.md`, kept short.** It adds the call-budget rule from the 40-call failure and a rule never to rerun a command that just failed. It also says to keep scratch files out of `output/`, to re-read the deliverable at the end, and when to use the script. It lists the verified workspace facts: the two date formats, the accounting negatives, the exact duplicate rows, the three statuses and three currencies, and the Aug and Oct rows that are excluded.
- **`tool_descriptions/tool_guidance.md`.** It says paths are relative to the workspace root, because the first two `list_files` calls on `workspace` and `/` errored. It also says `exit=timeout` means do not retry, and that a traceback names the value to fix.
- **No skill, subagent or plugin.** One short always-on rule plus a script covers a procedure this small.