**Evidence reviewed:** one rollout (base1), its deliverable `output/answer.json` = `{"net_usd": 18691.64, "transactions": 21}`, the two source CSVs, and the base harness. I recomputed the total independently from `context/source/`: 21 distinct SETTLED September rows, 18,691.6368 before rounding, 18,691.64 after. The rollout's answer is correct. There is only one run, so there is no divergence to compare.

**Changes**

1. **`skills/settled-revenue-reconciliation/SKILL.md` (new), with a trigger line in `systemprompt.md`.**
   - *Moment:* base1 lines 81–82 chose duplicate-collapsing and parenthesis-as-negative on its own judgment. Its final message (lines 118–121) then flagged the parenthesis convention as unresolved: "If the processor means something else by parentheses, the total changes." The total depends on that convention, so it is a decision the run had to improvise.
   - *What the skill encodes:* the settled-status and period rules; identifier identity (count once, and report a conflict rather than pick a copy silently); parse completeness; amount notation (parentheses and leading minus are negative unless the export documents otherwise, and the convention must be stated); per-unit FX multiplication; rounding once at the end; and consistency checks. It also covers what the final message must report.
   - *Why this form:* it is a recognisable trigger (a processor export becoming a revenue figure), so it is on demand and costs nothing until invoked. The always-on cost is one trigger line.
   - *What I deliberately left out:* the FX rates, transaction IDs, counts, and the answer. These are matter facts, and the mission says not to store them as durable anchors. The skill says where to read them.
   - No scripts are named, and there are no template braces (checked).

**No change:** `LongTermMEMORY.md`, `guardrails.md`, and `tool_guidance.md` remain empty; the READMEs under `plugin/`, `scripts/`, and `skills/` are untouched. I did not add a hook or a plugin, because the single run showed no repeated failure that a tool-loop check would catch.

**Limits:** the workspace `CLAUDE.md` appears in the rollout's directory listing, but its contents are not in `context/`, so I could not account for it. The change rests on one trajectory. It is a risk-based addition, not a fix for an observed failure, and a later comparison should weigh it accordingly.