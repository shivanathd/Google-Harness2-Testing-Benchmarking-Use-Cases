KEEP_BASE. I changed no files in `context/harness/`.

- **What the run did:** base1 is the only rollout. It read POLICY.md and all four CSVs in two commands, then wrote one short Decimal script. The script gave 9 transactions, 3 chargebacks and a net of 5072.12. It then wrote `output/answer.json` as `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. The agent did not reopen that file after writing it. The Write call confirmed creation, and I checked the contents in `deliverables/base1`.

- **My re-derivation from the source CSVs:** I got the same counts and net.
  - **Late-August captures:** ch_000 and ch_028 convert to UTC dates of Aug 31, so neither counts as September revenue. ch_000's September chargeback (cb_2) is still booked in September, with its reversal and fee.
  - **Test customer:** cb_5 (ch_022, customer C09) is excluded because C09 is a test customer.
  - **Test-customer charges:** ch_090 and ch_091 (large C09 charges) are excluded for the same reason.
  - **UTC conversion:** the script used `astimezone(utc)` on both `captured_at` and `chargeback_at`.
  - **Minor units:** it divided USD, EUR and INR by 100, left JPY as whole yen, and rounded once at the end.

- **Why no edit:** the run showed no divergence, tool error, budget blow-up or missed deliverable that any text would have changed. There is only one rollout, so nothing to compare against.

- **Library example not copied:** the `data-m` library harness (a reconcile script plus a Stop hook) came from a task where the base run dumped reference tables and never wrote its output. Nothing in base1 resembles that failure. That harness is also hard-coded to transactions, refunds and daily FX columns, which don't match this workspace's charges, chargebacks and monthly FX. Copying it would add always-on cost with no moment in a trajectory behind it.