The earlier rejection was for task-specific values in `systemprompt.md`. I fixed that by rewriting only that file.

- **Removed:** the whole "Workspace facts for the September 2026 data" bullet. It carried the duplicate-row ids, the "2,845.66" amount, the month and date window, the currency list, the verified counts and the net total.
- **Added:** one short bullet that gives the method. Before trusting the script, the agent scans the inputs once for these cases and checks each against the script's audit output:
  - exact duplicate rows
  - thousands separators in amounts
  - non-final statuses
  - dates outside the target month
  - currencies missing from the FX table
  - refunds whose original transaction is excluded or in another currency
- **Unchanged:** the other working rules, `scripts/reconcile_revenue.py`, `scripts/check_output.py` and `hooks.json`. I found no other instance values in the harness; a grep for the ids, the total and "September" matched only the removed bullet.
- **Evidence:** I did not re-read the rollout trajectory this time. The kept rules come from my earlier reading, which I did not redo.