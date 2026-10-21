KEEP_BASE. I made no changes to the harness.

The only rollout, base1, handled every practitioner trap in this workspace correctly without any harness help:
- **Dates:** it noticed the mixed formats (`2026-09-15` and `Sep 15, 2026`) before computing and parsed both.
- **Duplicates:** it noticed that T11007, T11022, T11010, T11019, T11012 and T11014 each appear twice. It asserted the repeated rows were identical, then counted each `txn_id` once, as the task says.
- **Amounts:** it read the parenthesised amounts `(954.34)` and `(888.14)` as negative. It also handled the thousands-separator commas in amounts like `"1,944.41"`.
- **Filtering:** it kept only SETTLED rows dated 2026-09-01 to 2026-09-30 and excluded the PENDING, VOID, August and October rows.
- **Conversion:** it multiplied by `usd_per_unit` using `Decimal` and rounded once at the end.
- **Result:** it wrote `{"net_usd": 18691.64, "transactions": 21}` in the requested shape and stated its assumptions.

There was no divergence between runs, no repeated failure and no visible near-miss that a harness line would have changed. Adding always-on text would cost context on every run. A skill would also need a trigger line in the always-on text, and I can't tie it to a specific moment in the trajectory. The workspace facts (the duplicate IDs, the parenthesis convention, the date formats) are specific to this matter, so I did not store them as durable memory.