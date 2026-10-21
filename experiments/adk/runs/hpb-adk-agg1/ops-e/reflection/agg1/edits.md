component: skills/log-window-stats/SKILL.md (new skill)
candidates: agg1, inv1, dom1
change: The base harness had no skill. All three candidates added one that encodes these rules. An event is a header line, and indented traceback lines are continuation text, so their `user=` and `code=` are ignored. Level is the token after the timestamp, so an `INFO ... retrying after ERROR` line does not count. Timestamps are converted to UTC before filtering. The window is start-inclusive and end-exclusive. A tie check applies to top_code. The skill also gives a no-shell fallback of listing events by hand. agg1 merges dom1's detailed rules with inv1's reopen-and-validate step. inv1 wrote a shorter 5-step version. dom1 omitted the reopen step.
observed: base1 never loaded a skill. It read all 163 lines in one `read_file` and wrote `errors: 21` straight away, with no event list. agg1, inv1 and dom1 each loaded the skill as their first action, then ran the script. All three produced the same 15 listed events and wrote 15/6/E500. The skill text and the script were added together, so this run does not show which one fixed the count. One rollout per arm.
verdict: confounded

component: skills/log-window-stats/scripts/log_window_stats.py (inv1's script, kept in agg1; dom1 used its own window_stats.py)
candidates: agg1, inv1, dom1
change: inv1 and agg1 ship an argparse script. It parses the header separately and lists unparsed lines. It skips indented lines and filters on the exact level token. It prints each matched event with its UTC time, user and code, and it can write the three-key JSON with `--out`. It refuses to write (exit 2 or 3) on unparseable lines, a tied top code, or an empty match. dom1 shipped a shorter `window_stats.py`. That script prints the events and the summary but does not write the file. Its regex requires `user=` directly after `[service]`, so any non-matching line is skipped silently.
observed: The agg1 and inv1 rollouts each made one `run_command` call and the script wrote `output/answer.json` itself. The dom1 rollout ran its script, then hand-copied the printed dict with `write_file`. All three printed the same 15 events and the same tallies. There is no case here where the two scripts differ in result, so the robustness features were never tested.
verdict: no observed effect

component: systemprompt.md (trigger line)
candidates: agg1, inv1, dom1
change: The base prompt had no pointer to the skill. inv1 and agg1 added a trigger plus an always-on guard: "Never answer such counts from a quick read of the file: derive them from an explicit per-event list or the skill's script, and reopen the deliverable after writing it." dom1 added only a plain trigger: "When the task is counting events, users or top error codes from a service log over a time window, load the `log-window-stats` skill."
observed: All three rollouts called `load_skill` as the first action, so both wordings fired on this task. The guard sentence changed nothing visible. agg1 and inv1 never reopened the file after the script wrote it. dom1 lacked the sentence and also did not reopen it. The two wordings were never separated. Against base the effect is confounded, because the skill was added in the same edit.
verdict: confounded
