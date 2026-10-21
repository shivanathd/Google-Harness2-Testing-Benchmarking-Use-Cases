Evidence: there was one rollout, base1. It got the right answer on its own: 16 transactions, 5 refunds, net_usd 24317.47. It kept each of S004, S026 and S028 once by txn_id, because they appear twice as identical rows. It stripped the thousands-separator commas from quoted amounts. It excluded PENDING and VOID rows. It assigned refunds by refunded_on and converted them using the original transaction's currency. It converted each row at its own day's rate and rounded once at the end. I did not recompute the figures. I checked them only against the rollout's printed row lists and source heads.

Because the base run needed no correction, I made no change to behaviour already shown to work. I made one low-cost addition so the next task in this data domain starts with the practitioner checklist instead of rediscovering it:

- **Added `skills/revenue-reconciliation/SKILL.md`.** It is loaded on demand and covers these points:
  - Profile each file first. Look for duplicate txn_ids, status values, and amounts with commas. Look up the refund's currency from the original transaction. Check that `usd_per_unit` is multiplied and that FX rows are unique and complete.
  - Recognition rules: use settled_on, assign refunds by refunded_on, convert at each row's own day's rate, and round once at the end.
  - Pre-finish checks: gross minus refunds equals net, and the counts equal the list lengths.
  - Workspace facts, labelled as such and to be re-verified. These are the duplicate IDs S004, S026 and S028, the five September refunds (R01, R04, R06, R08, R09), the FX coverage, and the result obtained. The evidence supports each fact.
- **Added a trigger line to `systemprompt.md`** pointing to the `revenue-reconciliation` skill, so the skill is not dropped at validation.

No always-on prose was added beyond that single line. I added no scripts or plugins, and I left the deliverable shape (`{net_usd, transactions, refunds}`) entirely to the task.