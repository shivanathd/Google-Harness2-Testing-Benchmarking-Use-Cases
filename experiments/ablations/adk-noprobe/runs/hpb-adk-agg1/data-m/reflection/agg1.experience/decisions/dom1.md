I fixed the rejection by removing this task's own data from the harness. I didn't re-read the trajectories this round, since the change only strips instance data.

- **`skills/payment-revenue-reconcile/SKILL.md`:**
  - I deleted the whole "Workspace facts" block: the duplicate txn_ids, the file column lists, the refund date spread and the INR zero-rate date.
  - The refund-timing sentence named specific months, so I reworded it generically: a refund issued in the month for an earlier sale counts, and a later refund of an in-month sale does not.
  - I added check 6, which tells the agent to re-derive the input facts itself. That covers column names, distinct statuses and currencies, date formats, exact versus conflicting duplicate ids, refunds pointing to missing or non-SETTLED txns, and zero or missing FX rates on any date used.
  - The skill is still triggered from `systemprompt.md`, which I did not change.
- **`scripts/net_revenue.py`:** it defaulted to the month 2026-09, which is this task's time window. I removed the default, so the script now exits with an error asking for the month unless one is passed. The docstring says the same. A syntax check passed, but I did not run the script.
- **Rest of the harness:** a grep for the removed ids and the month default found nothing left in the harness.