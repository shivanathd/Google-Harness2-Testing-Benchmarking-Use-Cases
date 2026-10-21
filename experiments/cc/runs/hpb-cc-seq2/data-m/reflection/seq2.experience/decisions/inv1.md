KEEP_BASE. I made no changes to the harness.

- **Both rollouts agree.** base1 and base2 wrote the identical `output/answer.json`: `{"net_usd": 24317.47, "transactions": 16, "refunds": 5}`. The file is valid JSON with the three requested keys and 2-decimal net. base1 re-parsed the file after writing it.
- **Workspace traps handled.** Both runs deduplicated the exact-duplicate rows (S028, S004, S026) and stripped the thousands-separator commas from amounts. They counted only SETTLED rows with September `settled_on`. They converted refunds at the refund-day rate in the original transaction's currency. Both used a Decimal script, and base2 added an assertion that duplicate rows are identical.
- **No procedural divergence.**
  - Both did the same preview, read, script and write sequence. Neither hit a tool error, timeout or budget problem.
  - The `ls: ..: Operation not permitted` line in base1 was harmless and didn't change anything.
  - The only differences are in the final summaries. Rounding was not a divergence: base2's per-line rounding printed the same total as base1's unrounded sum.
- **Nothing to fix.**
  - There is no repeated failure, so a skill, script or plugin would only add context cost.
  - Always-on prose would add cost with nothing observed to correct.
  - I did not record workspace facts (S028/S004/S026 duplicates, 16 and 5 counts) because the runs got the answer right without them.