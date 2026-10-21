**Evidence.** There was one rollout, base1, and it produced no deliverable. It ran `list_files` and three `read_file` calls on the CSVs. Its last message was a three-step plan ("Let's proceed with the calculations") with no further tool call. So `output/answer.json` was never written. The base harness was a single sentence with nothing on procedure, scripts or completion.

**Changes**
1. **New skill `skills/payment-revenue-reconcile/` with `scripts/net_revenue.py`.**
   - Motivation: base1 read the files, then stopped without computing anything or writing the file. The joins it would have had to do by hand are mechanical. They are deduplication, thousands-comma amounts, per-day FX lookup, and refund currency taken from the original transaction.
   - The script is stdlib-only and takes `transactions.csv refunds.csv fx_daily.csv YYYY-MM --out output/answer.json`. It prints an audit and writes the file as `{"net_usd","transactions","refunds"}`. It then re-reads the file to check it, so a successful write isn't taken on trust.
   - It exits loudly on an unparseable amount or date, a missing or zero FX rate on a needed date, a refund pointing to an unknown txn_id, or a SETTLED row without `settled_on`. It does not skip rows silently. It warns when a refund sits on a non-SETTLED transaction.
   - I ran it against `source/` and it worked: 16 transactions and 5 refunds for 2026-09. I did not write that answer into the harness.
   - The skill follows the library's `data-e` entry, whose script was written for a different schema and was not copied.
2. **Verified workspace facts in the SKILL.md, labelled as workspace facts.**
   - transactions.csv has 43 rows and 40 unique ids. S004, S026 and S028 are duplicated verbatim, and S004 and S028 are SETTLED in September.
   - Amounts with thousands commas are quoted.
   - INR on 2026-10-31 has a rate of 0, outside the period.
   - The refunds in September are R01, R04, R06, R08 and R09. R00, R03 and R05 fall in October, and R02 and R07 in August.
3. **`systemprompt.md` trigger line plus an act-don't-plan rule.** The trigger line names the skill. The rule is "Never end a turn with only a plan… re-read the deliverable once." It directly addresses base1's plan-then-stop ending. It also sets the budget and a bounded retry rule: no re-running a failed command, so an error gets fixed rather than looped on.

`guardrails.md`, `LongTermMEMORY.md` and `tool_guidance.md` are unchanged. I did not add a plugin because there is no repeated evidence that prose gets skipped (k=1).