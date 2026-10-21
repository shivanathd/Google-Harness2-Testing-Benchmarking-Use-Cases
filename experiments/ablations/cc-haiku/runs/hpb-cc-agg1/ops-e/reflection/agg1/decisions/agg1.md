revised -> harness as a whole: MERGE, not KEEP_BASE and not a wholesale adoption -> base1 produced nothing (0/1 base rollouts wrote output/answer.json; it ends at a tool observation after printing the figures, base1 line 225). dom1 and inv1 each delivered the file (1/1 each). No merged edit comes from a non-delivering rollout. The "produced nothing" signal rests on a single base sample, so the edits are on-demand and cheap, not always-on.

kept -> systemprompt.md base line (unchanged) -> the unmodified base instruction ("write the requested deliverables under output/") did not yield the file in base1 (0/1), so it stays as the anchor line.

revised -> systemprompt.md: one trigger line naming `log-window-stats` -> dom1 line 1 and inv1 line 1 both called Skill `log-window-stats` as their first action (2/2 candidate rollouts loaded it); base1 loaded nothing. Wording uses the task's own framing ("incident or traffic statistics from service logs over a time window").

revised -> skills/log-window-stats/SKILL.md, merged from dom1's contract, event, time, statistics and check sections -> dom1 wrote output/answer.json and parsed it with the key and type check (pool/dom1 lines 202-207); base1 wrote no file. The file-is-the-deliverable rule lives in the skill, which the run loads at its first step, so no extra always-on prose is needed. Added a closing one-line final message (inv1 gave one, dom1 ended after verification with none).

dropped -> dom1's "Facts observed in this workspace" section (163 lines, 130 headers, offset forms, traceback-text mismatch, raw-string undercount) -> these are facts about this matter's app.log. The dom1 run never referred to them; its own stats.py reached 15/6/E500 unaided (pool/dom1 lines 180-199). A library skill must not carry one dataset's counts. No answer figures appear in any harness file.

revised -> SKILL tie and empty-window rules (alphabetically first tied code and name every tie; errors 0 gives top_code "") -> no rollout hit either case, so this is unverified. dom1's spec said top_code "has no defined value" when errors is 0, which conflicts with the task's typed-string deliverable, so the case had to be decided.

revised -> helper path in SKILL.md made skill-relative (`<skill-dir>/scripts/window_stats.py`) -> inv1 line 20: the run executed `.claude/skills/log-window-stats/scripts/window_stats.py` because the path the candidate SKILL.md stated (`skills/log-window-stats/...`) was not where the runtime placed the skill. The agent corrected it by itself.

kept -> skills/log-window-stats/scripts/window_stats.py (copied byte-for-byte from inv1; read as text, never executed from the candidate) -> inv1 line 20 ran it once and got headers 130 + continuation 33 = 163 non-blank lines, unparsed [], ERROR present in levels, and 15/6/E500. My independent recount on a copy of app.log outside the harness gave the same 15/6/E500 and the same 130/33 split.

dropped -> inv1's always-on procedure steps 1, 3, 4 and 6 -> the content moved into the on-demand skill rather than always-on. Step 1 (read CLAUDE.md) is redundant: the workspace CLAUDE.md is the always-on prompt already in context. Its sizes are 172/327/978 bytes, which equal systemprompt bytes 152/307/958 plus a constant 20 bytes across all three arms. No run opened it (base1 line 1, inv1 line 2, dom1 line 4 listed it and did not read it).

dropped -> inv1's scripts/check_json_output.py -> no rollout got the deliverable shape wrong (3/3 that wrote a file had exact keys and types). dom1 verified shape with a one-line parse (pool/dom1 line 203), so the checker adds surface without a demonstrated failure.

dropped -> a Stop hook (hooks.json) that blocks finishing until output/ is written -> the only mechanism that enforces "the file exists", but its sole evidence is base1 ending without the file (1/1, which the rules treat as noise). The plugin README's hooks.json form is unverified in this rig, and a malformed file could fail validation and discard the whole harness. Revisit if another base-set rollout ends without output.

kept -> LongTermMEMORY.md, guardrails.md, tool_guidance.md, plugin/README.md, scripts/README.md, skills/README.md (all unchanged) -> no trajectory moment shows a durable domain fact or a standing rule; the only facts available are this matter's answer and data.

kept -> validation of the proposal -> the trigger names `log-window-stats` verbatim in systemprompt.md; grep finds no `{{` or `{%` anywhere in the harness; the SKILL.md frontmatter name matches its directory and has a description; the helper ships under skills/log-window-stats/scripts/ and is not referenced from always-on text.