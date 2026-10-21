# data-e

- adopted: `agg1`  (run `hpb-adk-agg1/data-e/agg1`)
- components: 1 skills; 635 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/payment-revenue-reconcile/ (SKILL.md and scripts/net_revenue.py) plus its trigger line in systemprompt.md
candidates: dom1, agg1. The adopted harness is identical to agg1 here.
change: Adds a skill with checkable rules and a stdlib-only script that cleans, dedupes, filters and converts. The rules are: dedupe on txn_id before filtering, treat `(x)` and a leading `-` as negatives, parse mixed date formats into real dates, match status exactly, multiply by the FX rate, and round only the final total. The script stops on anything it can't parse instead of skipping it, and prints an audit and the JSON values. It does not write the deliverable. A line in systemprompt.md tells the agent to load the skill for payment or finance exports. dom1's SKILL.md also stated "Script result: net_usd 18691.64, 21 transactions", and agg1 removed that line.
observed: base1 (no skill) never wrote answer.json. It crashed on `(954.34)`, re-ran the same script about 30 times and hit the 40-call limit. Its `str.contains('Sep')` month filter was also wrong, and it didn't dedupe. In dom1 and agg1 the first action was `load_skill`, the second ran the script once, and the third was `write_file`. Both produced `{"net_usd": 18691.64, "transactions": 21}` in 3 actions. The agg1 and dom1 rollouts are nearly identical, so removing the stored answer from the skill's workspace facts changed nothing observable. Each arm has one rollout, but the base-versus-skill contrast is stark. inv1 reached the same answer with a different, unskilled script, so the benefit comes from having a tested script, not from the skill packaging.
verdict: helped

## Transferable lesson
- **cue**: A task turns a messy tabular export (mixed date formats, accounting-style negatives, repeated IDs, reference-rate tables) into one or two summary numbers. The base harness has only prose guidance, and an ad hoc script crashes on a malformed value, so the agent loops on it until its call budget runs out and no deliverable gets written.
- **lesson**: Add a tested, stdlib-only script to the harness (a skill's scripts/ directory or workspace scripts/) and name it in systemprompt.md with a trigger line. The script should dedupe by ID before filtering, parse real dates, parse accounting negatives, and exit loudly on any value it can't parse. It should print an audit and the final values for the agent to write out. Keep expected answers and dataset-specific figures out of always-on text. Treat a generic retry-limit paragraph as insurance only, because no rollout showed it firing.
- **evidence**: Skill and script row. base1 had no script, crashed on `(954.34)`, re-ran about 30 times and never wrote the file. dom1 and agg1 loaded the skill, ran the script once and wrote the correct file in 3 actions. inv1, with a different script and no skill, was correct in 2 actions. Three independently built script-bearing harnesses succeeded where the unscripted base failed. The retry-paragraph row shows no effect, so the lesson rests only on the script.
- **confidence**: medium. The contrast is clear and repeated across three script-bearing candidates against one failed base rollout. But each arm has k=1, all candidates share the same task and data, and the script rows can't be separated from the skill packaging or the trigger line.
