KEEP_BASE. I made no changes to the harness.

The single rollout (base1) did the work correctly and I found no divergence to fix.

- **Reading the data:** It read the full 42-row file before computing. That showed two date formats (`2026-09-15` and `Sep 15, 2026`), quoted thousands separators, and parenthesised negatives such as `(954.34)`.
- **Duplicates:** It found six txn_ids that appear twice with identical rows (T11007, T11022, T11010, T11019, T11012, T11014). It asserted the copies were identical and counted each txn_id once.
- **Computation:** It used Decimal, rounded once at the end, and filtered to SETTLED rows dated in 2026-09. The result was 21 transactions and 18691.6368 USD.
- **Deliverable:** `output/answer.json` has the requested shape: `{"net_usd": 18691.64, "transactions": 21}`. The script printed the same JSON after writing, and the file reads back intact in the converted deliverable.
- **Reporting:** The final message stated the assumptions, including that T11007 is the only duplicate that affects the total.

I found nothing that a prose rule, skill, script or hook would have changed. There was no tool error, no repeated hand-rolled step and no skipped invariant. The task is a one-off 42-row file, so a script would be speculative. Always-on text would only add to the context every run pays for. Every candidate edit I considered was either already done correctly by the run or would restate the task's own wording.