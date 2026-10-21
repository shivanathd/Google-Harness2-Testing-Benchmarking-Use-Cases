- **Evidence:** the only rollout, base1, never wrote `output/answer.json`. It filtered September with `str.contains('Sep')`, which misses the ISO-dated rows. It then called `float()` on `(954.34)` and hit the same ValueError about 35 times. It reran the unchanged script until the 40-LLM-call limit. Its only deliverable is a script that, as written, would also write answer.json in a records-list shape.
- **New skill `skills/payment-revenue-reconcile/SKILL.md`:** it records the quirks I checked in `source/transactions.csv`:
  - Six txn_ids are repeated: T11007, T11010, T11012, T11014, T11019, T11022.
  - Dates come in two formats.
  - Amounts include thousands separators and `(x)` accounting negatives.
  - Statuses are SETTLED, PENDING and VOID.
  - The files have CRLF line endings.
  - FX is multiplied as `usd_per_unit`, with USD, EUR and INR all mapped.
  
  It also gives the domain rules and a finish checklist:
  - Dedupe by txn_id.
  - Filter by parsed date, not a text match.
  - Keep SETTLED refunds as negatives.
  - Round once at the end.
  - Write answer.json as a plain object, not the pandas records orient base1 used.
- **New script `skills/payment-revenue-reconcile/scripts/settled_revenue.py`:** stdlib only, because pandas was missing in the run and a pip install timed out. It parses the dates and amounts, dedupes by txn_id, flags conflicting duplicates, converts to USD, prints a per-currency reconciliation and writes the JSON. I ran it on this workspace's source files and it ran cleanly, with no conflicting duplicates and nothing unparseable. I did not copy its numeric result into the harness.
- **`systemprompt.md`:** added the required trigger line for the skill, plus one short line saying not to rerun an unchanged failing command. The second line is a procedure nudge. I added it because of the repeated-failure loop, and a parallel procedure candidate may supersede it.