I removed the "Workspace facts" block from `skills/fix-python-bug/SKILL.md`. It held facts about this instance's files: the invoicing issue #142 bug locations and the hand-computed expected values. I did not re-read the trajectories this round, and the block's content is unchanged from the earlier attempt.

I replaced the block with a short "Before finishing" checklist of checks the agent re-derives itself:
- Hand-compute one example from the spec, including a half-cent case, and confirm the output matches.
- Confirm differently-cased or spaced inputs give identical results, and that bad input raises the spec's exception.
- Confirm any test that failed before the change now passes without editing that test.

I did not change the rest of the skill, which is general procedure and the money/rounding checklist. I also left `systemprompt.md` alone. Its existing trigger line for `fix-python-bug` still names the skill, so it passes the trigger-line rule.