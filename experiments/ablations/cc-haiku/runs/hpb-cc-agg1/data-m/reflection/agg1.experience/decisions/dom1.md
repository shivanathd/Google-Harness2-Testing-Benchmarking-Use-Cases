Revised after rejection. The skill no longer records this instance's data; the trigger line is widened in a one-line edit.

**Fixes for the rejection**
- `skills/revenue-reconciliation/SKILL.md`: removed the "Workspace facts for this export set" block entirely. It held S004/S026/S028 duplicates, status counts, the 43/40 row counts, the refund-month tallies, and R00/S033. It is replaced by a "Profile the exports before summing" section of checks the agent runs on whatever files it receives: duplicate txn_id identity, status tabulation, currency and FX coverage, refund join, and refund month tabulation. No ids, counts or windows remain.
- `SKILL.md` Rounding rule: "In this data, rounding each line first moves the total by one cent" became the generic "can move the total by a cent". Refund currency rule: "Refunds carry no currency column" became conditional ("if the refunds file has no currency column").
- Verified by grep that `context/harness/` has no S0xx/R0x ids, 2026 dates, month names, or template braces.

**Change from the earlier attempt**
- `SKILL.md` Checks: added one check that a refund whose original is not recognised in the period is named in the final message with the rule applied. This is a stated uncertainty, not a fact about this data.

**Trajectory moment behind the remaining edits**
- `base1.md` (lines 1–98): the only rollout made four Bash calls that dumped the CSVs and FX tables, never invoked the `revenue-reconciliation` skill, and never wrote `output/answer.json` (deliverables/base1.md: "no deliverable produced"). The always-on trigger was present but did not match the agent's behaviour.
- `systemprompt.md` trigger line: reworded from "reconciling … into a period revenue figure" to "computing a period revenue figure (net, recognised or gross) from payment, settlement, refund or FX exports". This uses the task's own wording ("Compute … net revenue … from transactions.csv, refunds.csv and fx_daily.csv"). The change is low-confidence, since the rollout shows one run and the old wording was close. It is a single-line swap at no added always-on cost.

**Not changed**
- No edits to the plugin, scripts, or subagent components. `plugin/README.md` and `scripts/README.md` are comment-only, and no hooks.json or script exists.
- `guardrails.md`, `LongTermMEMORY.md`, and `tool_guidance.md` stay empty.
- Did not add guidance on exploration volume or reading order. The rollout's failure looks like over-dumping data, but that is procedure, which is out of scope for this dimension.