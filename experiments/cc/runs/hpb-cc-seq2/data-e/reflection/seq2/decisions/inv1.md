KEEP_BASE. I changed no files in the current checkpoint.

- **Runs agree.** base1 and base2 wrote identical files: `{"net_usd": 18691.64, "transactions": 21}`. That matches the shape the task asked for.
- **Same method, no divergence.** Both runs read the full CSVs and handled every trap in `transactions.csv`:
  - Two date formats.
  - Quoted thousands separators.
  - Parenthesized negatives such as `(888.14)`.
  - Six repeated `txn_id`s (42 rows, 36 unique), which they deduplicated after confirming the repeats were identical.
  - Non-SETTLED rows and out-of-month rows, including T11022 dated 2026-10-26.
  - Currency conversion with `Decimal`, rounded once at the end.
- **No tool errors.** The only error was the harmless `ls: ..: Operation not permitted`, which both runs ignored without losing anything. Neither run repeated a call blindly or lost time to a failure.
- **No completion risk.** Each run wrote `output/answer.json` after one calculation pass. Neither came near running out of budget or finishing without a deliverable.
- **Nothing to attach a change to.** I can't name a trajectory moment where extra text, a skill, a script, or a plugin would have changed behaviour. Adding any of them would only cost context.
- **Dedup facts stay out.** I did not record the dedup and format facts for this workspace. Both runs found them without trouble, and they belong to a parallel candidate that owns subject matter.