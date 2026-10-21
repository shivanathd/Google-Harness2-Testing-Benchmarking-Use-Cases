KEEP_BASE. I made no edits to the harness.

- **What base1 did:** It read POLICY.md and the four CSVs. It then wrote one Decimal-based script and wrote output/answer.json as `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`.
- **How I checked it:** I re-derived the answer by hand from the source files. Each rule that could have gone wrong was handled correctly:
  - **UTC month boundary:** ch_028 (2026-09-01T03:49+05:30) falls on Aug 31 UTC and is excluded. ch_009 (2026-09-30T13:08-05:00) falls on Sep 30 UTC and is included.
  - **Minor units:** the script divided USD, EUR and INR amounts by 100 and treated JPY as whole yen.
  - **Test customers:** C09 and C10 are excluded everywhere. That drops ch_022, ch_090, ch_091 and the cb_5 chargeback.
  - **Chargebacks:** they are booked by `chargeback_at` UTC regardless of charge date. cb_2 reverses ch_000, an August charge, in September. cb_0 and cb_6 reverse ch_002 and ch_023.
  - **Fees and rounding:** it charged the 15.00 USD fee per chargeback and rounded only the final figure.
- **Why no change:** The run shows no divergence, no repeated failure and no realised risk. The agent applied every POLICY.md rule correctly without extra guidance. Adding a skill or always-on prose would cost context on every run and change no behaviour.