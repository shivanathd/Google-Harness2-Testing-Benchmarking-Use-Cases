# ops-m

- adopted: `agg1`  (run `hpb-adk-agg1/ops-m/agg1`)
- components: 1 skills; 999 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/log-request-failures (SKILL.md and scripts/request_window_stats.py)
candidates: agg1
change: Added a new skill and helper script. The skill sets out a procedure that treats the request as the unit of analysis: take the highest-attempt line, convert timestamps to UTC, use a half-open window, and read gzip by magic bytes. The helper prints the list of qualifying requests, tallies of skipped lines, and a code tally. It can write the answer file and refuses to write on a code tie or when a request maps to two users.
observed: In agg1 the agent loaded the skill first. It then ran `ls`, ran the helper once over all three log files with `--list`, and wrote output/answer.json as `{"failed": 19, "users": 8, "top_code": "E401"}`. That took 4 actions and had no shell errors. Base1 read app.log raw, grepped ERROR lines and tried to sum with awk. It hit an unbalanced-quote syntax error, resent the identical command, and finished with no answer file ("no deliverable produced"). The base run never decoded the gzip file. The agent in agg1 did not run any independent check of the helper's output. It wrote the answer as soon as the list printed. The skill, the trigger line and the tool guidance all arrived together, and there is only one rollout on each side.
verdict: confounded

component: systemprompt.md
candidates: agg1
change: Added a trigger paragraph. It says to load the `log-request-failures` skill for log-statistics tasks, never to count by grepping "ERROR", never to count mentally, and not to finish until the named deliverable exists under output/ and has been reopened.
observed: Agg1's first action was `load_skill log-request-failures`, which fits the trigger line. The base run, which had no such line, went straight to raw grep. The agent never reopened the written file, so the completion rule was not followed. I can't separate the trigger from the skill's presence, because the skill was never offered without the trigger.
verdict: confounded

component: tool_descriptions/tool_guidance.md
candidates: agg1
change: Added two bullets. One says `read_file` can't read .gz files and truncates long files. The other says to put anything beyond a simple pipe into a .py file, and to fix a syntax error once by moving the command to a file instead of resending it.
observed: Agg1 ran no complex one-liner and hit no syntax error, so neither bullet came into play. The failure these bullets target (a repeated identical awk command) appears only in base1, which didn't have them. Whether they would have prevented it is untested.
verdict: no observed effect

## Transferable lesson
- **cue**: A recurring analysis task over messy multi-file inputs (rotated or compressed files, mixed timezones, lookalike or continuation lines). It needs record-level aggregation with exact counts. An unaided run improvised shell one-liners, hit a quoting error, and delivered nothing.
- **lesson**: In the harness, put the deterministic parsing and aggregation in a helper script under a skill. The skill's procedure should name the unit of analysis, the window-boundary rule and the hazards to check for (gzip, mixed UTC offsets, non-record lines). Add one trigger line to systemprompt.md that routes this class of task to the skill and forbids counting by grep or by hand. Do not rely on tool-guidance warnings alone. Keep instance facts (file names, expected counts, the specific window) out of the skill text.
- **evidence**: The skill and trigger rows. Base1 ran only the improvised grep and awk path and ended with no output file. Agg1, which had the skill, trigger and guidance bundled, ran the helper once and wrote a complete answer file. The only evidence is one rollout per arm, and the skill, trigger and tool guidance changed together. This shows that the bundle is sufficient and that the unaided path failed. It does not show which part of the bundle did the work, and it does not show that the helper's numbers are correct. A decisions note says an independent check gave the same 19/8/E401, but that check was outside any rollout.
- **confidence**: low. There is one rollout per arm, the edits are confounded, and the agent did not verify the helper's output itself.
