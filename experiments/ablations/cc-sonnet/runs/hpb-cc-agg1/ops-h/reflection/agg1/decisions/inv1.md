**Failure traced.** In base1 the agent hand-rolled a parser in /tmp. It got correct-looking numbers: gateway 96 requests, 0.1354, 334 ms; search 119, 0.1513, 192 ms; billing 124, 0.1613, 393 ms. It then spent its remaining turns on a billing cross-tab and a look at the truncated lines. Its last action was a printout, `output/` stayed empty, and the deliverable reads "(no deliverable produced)". This is the same failure the library entries ops-m and ops-e record, so I took the fix that coincided with delivery there. That fix is a prompt procedure with a compute-and-write script, a reopen step and a Stop hook, copied over and re-grounded for this task. I only have one rollout per harness, so this is a hypothesis about what will fix it.

**Changes.**
1. `scripts/traffic_report.py` is new.
   - It does the whole computation as one command, with `--write output/answer.json` on the same command.
   - It skips invalid-JSON (truncated) lines and converts every timestamp to UTC before applying the half-open window.
   - It drops `/healthz` and counts status >= 500 as errors. Latency is `latency_ms`, or `latency_s * 1000` decided per row by key. p95 is nearest-rank, `ceil(0.95n)-1`.
   - It prints skip tallies per service, and it refuses to write if a service has zero rows or an unusable row.
   - I ran it on `source/logs` for 06:00–12:00 UTC. It reproduces the base1 numbers exactly.
   - The base1 cross-tab showed billing switching from `latency_ms` to `latency_s` at 09:00 UTC. Its in-window rows are 26/29/32 ms-rows for hours 6/7/8 and 20/21/28 s-rows for hours 9/10/11.
   - So the per-row key rule agrees with the runbook's 09:00 UTC cutover.
2. `systemprompt.md` gets a short log-analysis procedure block.
   - It says to read RUNBOOK.md first and run the script.
   - It states workspace facts: mixed offsets of -03:00, +01:00 and +00:00, so convert to UTC before windowing; billing's latency_s cutover at 09:00 UTC; and that nothing is excluded beyond the runbook's rules.
   - It tells the agent to write with `--write` in the same command, reopen the file and check keys and types, and not to treat a printout with an empty `output/` as finishing. It also tells the agent to stop side investigations once the numbers are cross-checked once. That last line targets base1's final turns on the billing cross-tab and truncated lines.
3. `hooks.json` and `scripts/check_output.py` are new, copied from the ops-m library entry with the helper name changed.
   - The Stop hook exits 2 while `output/` is empty or holds an empty or invalid JSON file, and otherwise lets the agent finish.
   - It targets exactly base1's ending. In the library it never fired, because the prompt change was enough there.
   - I kept it as a cheap backstop.

I did not add a skill, a subagent or a plugin. The task is a single mechanical procedure with no triggered sub-workflow.