component: systemprompt.md (work procedure plus checks list)
candidates: inv1, agg1 (the two harnesses are byte-identical)
change: The base prompt was a single sentence. The edit added an "act, don't narrate; never end a turn on a plan" rule and a read-once, then compute-with-code procedure. It named the script command `python3 scripts/revenue_recon.py . YYYY-MM`, told the agent to run the checker afterwards, and added generic data checks: duplicate ids, thousands commas, zero FX rates, refund currency taken from the original transaction, and a count tally.
observed: base1 read all three CSVs, then ended on a plan with no `answer.json`. inv1 and agg1 ran the script as their first action and wrote `output/answer.json` with 24317.47, 16 transactions and 5 refunds. The prompt text, the script and the hook all changed together, so none of them is isolated. The run never exercised the checks list, because the script ran immediately and the agent did no manual tallying. The final chat message said 24317.48 while the file said 24317.47, so the "re-read and confirm" instruction was not followed.
verdict: confounded

component: scripts/revenue_recon.py
candidates: inv1, agg1
change: Added a deterministic script. It dedupes by txn_id, strips thousands commas, recognises SETTLED rows with settled_on in the month at the settled_on rate, applies refunds at the refunded_on rate using the original transaction's currency, and exits 1 on a missing or zero rate. It prints a per-row breakdown and writes the answer file. Its usage is `<data_dir> <YYYY-MM>`, and the prompt gives the exact command with `.` as the data dir.
observed: In inv1 and agg1 the first call succeeded. Output was 43 rows deduped to 40 ids, 16 transactions and 5 refunds, with net 24317.47. Both runs hit this at the same point, so there is only one distinct trajectory, and it is duplicated. The base run never computed anything, so the script is the most likely cause of the delivered file. I cannot separate it from the prompt line that points to it. I did not recompute the figure independently.
verdict: confounded

component: scripts/check_output.py and hooks.json (Stop hook)
candidates: inv1, agg1
change: Added a Stop hook that blocks finishing unless `output/answer.json` exists and parses with the correct key types.
observed: The hook never fired. The file already existed in both runs before the stop, so there was no execution contrast. It targets the base failure mode (ending on a plan), but it is untested.
verdict: no observed effect

component: skills/revenue-reconciliation (SKILL.md and scripts/recon.py) plus a systemprompt.md trigger line
candidates: dom1
change: Added a domain skill with rules for this task. It was loaded through `load_skill` and had its own `recon.py`, whose usage is `SRC_DIR YYYY-MM [OUT]`. The `scripts/revenue_recon.py` and Stop hook files were absent, and the systemprompt was reduced to a trigger line plus an "actually compute and write the file" sentence.
observed: dom1 loaded the skill, then called `recon.py` five times with the wrong arguments. It passed `workspace` as the directory, then the three filenames. Each call crashed with FileNotFoundError or NotADirectoryError. The agent tried to find a workspace directory through several `list_files` calls and ended on "let's try again" with no `answer.json`. The skill's rules were sound. The failure was an interface problem: the agent misread the `<dir with the 3 CSVs>` placeholder, and the script gave a raw traceback instead of a usage message. The skill also said to run `recon.py` from a different path than the data, with no worked example of the directory argument. There was no run of this skill with a correct invocation, so its domain content is untested.
verdict: hurt

component: LongTermMEMORY.md, guardrails.md, tool_descriptions/tool_guidance.md, plugin/ and skills/README.md
candidates: none (these match the base, or are placeholder READMEs)
change: No candidate changed these components.
observed: Nothing to observe.
verdict: no observed effect
