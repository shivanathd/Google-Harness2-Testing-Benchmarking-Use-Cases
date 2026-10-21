Rejected `systemprompt.md` text is now removed. I edited only that file, and I did not run the harness or re-read the rollouts this time.

- **What I removed:** the "Workspace facts" block with its specific transaction ids and the zero-rate date. Also the "Reference result" line with the net figure and the transaction and refund counts. A grep of the harness for those values finds nothing.
- **What replaced it:** one generic checklist. It tells the agent to re-derive the following from the inputs instead of being told them:
  - repeated `txn_id`s, each counted once;
  - thousands separators inside quoted amounts;
  - status values;
  - missing or zero fx rates for dates actually used;
  - a missing currency column in `refunds.csv`, handled by taking the original transaction's currency.
  The same checklist covers reporting counts as the task defines them and comparing the script's printed rows with the task wording.
- **Other edits:** the script command now takes the month from the task (`<YYYY-MM from the task>`) instead of a hardcoded `2026-09`. The description of the script's output now says "the three requested keys" instead of listing them.
- **Left unchanged:** the `scripts/net_revenue.py` and `scripts/check_output.py` scripts and the Stop hook in `hooks.json`. The `net_revenue.py` file still defaults to `2026-09` when run with no arguments.