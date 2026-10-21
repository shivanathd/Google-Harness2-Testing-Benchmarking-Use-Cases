component: systemprompt.md
candidates: agg1
change: Added one always-on paragraph. For counting or statistics tasks on service logs, it says to load the `log-incident-stats` skill (or read its SKILL.md) before counting. It also says never to select events by substring match on "ERROR" and never to count in your head.
observed: In base1 the first actions were list_files and read_file on app.log. The agent then wrote 21/6/E500 straight away, with no UTC conversion and no event list. In agg1 the first action was `load_skill log-incident-stats`, before any reading of the log. The trigger line is the plausible cause of that difference. The same rollout also changed the toolset (see the next row), so the effect of the line alone is not isolated.
verdict: confounded

component: skills/log-incident-stats/SKILL.md
candidates: agg1
change: New skill with a method for these logs:
- Only timestamp-led lines are events, and the level is the token right after the timestamp.
- Indented traceback lines and INFO "retrying after ERROR" lines are not events.
- Convert every timestamp to UTC, treat the window as half-open, and check for ties on the top code.
- Write out the list of qualifying events and reconcile the counts against it.
- Check the output keys and types.
observed: The agg1 trajectory loaded the full text of the skill, and the answer was correct at 15/6/E500. Base1 answered 21, which is consistent with counting traceback and "retrying after ERROR" lines and with ignoring offsets. agg1 never did the hand reconciliation (section 4). It went straight to the script and relied on the script's printed counts. The skill's checklist therefore shows no direct effect, because the script did the work. Only one rollout exists per arm.
verdict: confounded

component: skills/log-incident-stats/scripts/log_window_stats.py
candidates: agg1
change: Added a helper script. It treats an event as a line that starts with a timestamp and takes the level from the token after it. It converts timestamps to UTC and applies a half-open window. It prints the user set, the code tally and a tie warning. `--write` refuses to write on a tie or on bad lines.
observed: In agg1 the script was run once, with `--write` and without `--list`. It printed events=15 distinct_users=6, codes E500:5 and E403/E401:4, and continuation_lines_skipped=33. It wrote the correct JSON. Base1 had only list_files, read_file and write_file, and no shell. The script was usable in agg1 because run_command was available, so the toolset differed between the two runs. That makes this the likeliest cause of the corrected answer, but the run does not separate "had a shell" from "had the script". The script's encoded rules (header-line-only fields, UTC window, level position) match the traps visible in the log.
verdict: confounded

component: skills/README.md, plugin/README.md, scripts/README.md
candidates: agg1
change: Placeholder README files accompanied the new skill directories.
observed: Not read in the agg1 trajectory.
verdict: no observed effect
