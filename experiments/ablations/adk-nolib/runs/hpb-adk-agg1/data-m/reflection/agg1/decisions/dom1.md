This attempt only fixes the rejection. I did not re-read the trajectories or change anything else.

- **What was wrong:** `skills/revenue-reconciliation/SKILL.md` had a paragraph about this task's own data. It named the refund ids, the repeated transaction ids, the row and refund counts, the FX date window and the zero-rate date.
- **What I changed:** I replaced that paragraph with a generic checklist of data-shape checks to run on any set of transaction, refund and FX exports. The checklist covers these checks:
  - repeated rows for the same transaction id;
  - thousands separators in amounts;
  - multiple currencies and mixed statuses;
  - a refunds file with no currency column, where the currency comes from the original transaction;
  - refunds dated outside the requested month;
  - FX coverage and zero rates, judged only against the dates actually needed.
- **What I checked:** A grep of the harness for the removed ids, counts and dates (S0/R0 ids, "2026", "September", "43", "203") now finds nothing.
- **Left alone:** the trigger line in `systemprompt.md`, the numbered rules, the deliverable shape and `scripts/recon.py` are unchanged. The skill is still named in the always-on text and its script still ships with it.