I fixed the rejection by removing the "Workspace facts" block from `skills/fix-python-bug/SKILL.md`. That block held facts about this instance's files: the `parse_duration` regex bug, the single existing test case, and the specific probe strings. I did not re-read the trajectories or other evidence this turn, so this edit comes from the rejection feedback alone.

I also reworded three generic parsing bullets that still carried duration-specific examples:
- **Unit-suffixed formats:** the "number with no unit / unit with no number" line now lists the classes to probe (missing unit, missing number, unknown unit, signs and decimals, duplicate and out-of-order parts) instead of literal strings like "1h30".
- **Return type:** "Return the documented type (int for seconds)" now reads "Return the documented type and units."
- **Zero:** the `"0s" -> 0` example became "A zero value is valid and must be distinguished from invalid input."

What stays is the procedure the agent re-derives on each task:
- Split the docstring into numbered clauses and probe each one.
- Reproduce the symptom before editing.
- Never overwrite or weaken existing tests.
- Use `re.fullmatch` and `[0-9]` for string-to-value parsers.
- Run the confirm-before-finishing checklist.

The trigger line in `systemprompt.md` is unchanged and still names `fix-python-bug`, so the skill passes the naming rule.