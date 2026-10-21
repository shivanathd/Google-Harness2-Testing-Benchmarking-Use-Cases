**Evidence.** There is one rollout, `base1`, and it produced no deliverable. It read all three CSVs, then ended with a plan in prose ("I will compute…"). It never ran a calculation and never wrote `output/answer.json`. The harness it ran on was an empty stub with no domain knowledge. The library entry `data-e` showed the same kind of task failing without a tested script and succeeding with one.

**Changes**
1. Added `skills/payment-revenue-reconcile/SKILL.md` and `skills/payment-revenue-reconcile/scripts/net_revenue.py`. I wrote the script new rather than copying the library one, because that one assumes a single `date` column, no refunds file and a single flat FX rate. This task has `settled_on`, a separate `refunds.csv` and daily per-currency FX. I ran the script with `python3 -I` against `source/`. It produced 16 recognised transactions and 5 refunds, with the net total and the audit printed. I did not write the answer into the harness. The script does these things:
   - It dedupes on `txn_id` before filtering.
   - It keeps only SETTLED transactions whose `settled_on` falls in the month.
   - It strips thousands commas from amounts.
   - It converts each transaction at the `settled_on` rate.
   - It takes each refund's currency from the original transaction and converts at the `refunded_on` rate.
   - It counts a refund by its own `refunded_on` month, whatever month the original settled in.
   - It exits loudly on a missing or zero FX row, an unparseable value, or a refund pointing at an unknown `txn_id`.
   - It prints an audit and the JSON values, and it does not write the deliverable. The deliverable shape is therefore unchanged: `net_usd`, `transactions`, `refunds`.
2. The skill file holds the checkable rules and the verified workspace facts, each labelled as "verified here":
   - 43 transaction rows, 40 unique ids, and S004, S026 and S028 repeated verbatim.
   - 5 of the 10 refunds fall outside September, including the two dated 2026-10-31.
   - INR is 0 on 2026-10-31, the only FX anomaly. It is outside September, so it does not affect the result.
   - Transactions created in September can settle in October, so they are not September revenue.
3. `systemprompt.md` now has a trigger line naming `payment-revenue-reconcile` and telling the agent to write the deliverable early, since base1 never wrote one. Nothing was cut because the prompt was already one line.

I changed no other file and added no stored answer.