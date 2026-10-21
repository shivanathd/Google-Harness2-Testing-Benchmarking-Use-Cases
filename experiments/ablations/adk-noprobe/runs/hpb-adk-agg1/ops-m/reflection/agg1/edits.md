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
