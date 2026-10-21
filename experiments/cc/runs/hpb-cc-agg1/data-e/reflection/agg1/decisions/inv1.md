KEEP_BASE. I changed no files.

The only rollout, base1, was procedurally sound and finished.
- **Inspection:** It read both CSVs before computing.
- **Parsing:** It spotted every mess in the data: mixed date formats (`2026-09-15` and `Sep 15, 2026`), quoted thousands separators, parenthesised negatives, and 6 exact-duplicate rows. It handled all of them in a script.
- **Dedupe check:** It checked that duplicate `txn_id`s did not conflict before deduping.
- **Filter and rounding:** It filtered to SETTLED rows in September 2026 and rounded to 2 decimals using Decimal arithmetic.
- **Cross-check:** It compared the script's included count of 21 against a manual count.
- **Deliverable:** It wrote `output/answer.json` in the requested shape, `{"net_usd": 18691.64, "transactions": 21}`. The converted deliverable text matches.

I found no tool error, repeated mechanical step, skipped invariant or incomplete deliverable to fix, so I changed nothing. I did not recompute the figure myself. An always-on rule would only restate what the run already did, and one clean run is no evidence for a skill, script or plugin. Adding any of those would cost context and change nothing.