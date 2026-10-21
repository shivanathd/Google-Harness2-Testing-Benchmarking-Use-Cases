**Change made.** I replaced the "Workspace facts" block in `LongTermMEMORY.md` with a short list of checks the agent has to re-derive on every bug-fix task. The reviewer said that block described this instance's files, so I removed it.

**What was removed.**
- The package layout (`totals.py`, `tax.py`, `models.py`).
- The `RATES` dict and its string keys.
- The `LineItem` field types.
- The statement that the existing code returns floats.
- The specific rounding and region rules.

All of that is read from the source and `docs/ROUNDING.md` within the first few tool calls.

**What was kept.** Procedure only:
- Turn each bullet of the cited spec into one probe. This covers return types and format, rounding mode, case handling and error type.
- Compare the code's return types with the spec's, not just the reported symptoms. The issue in `base1` lists three symptoms. The spec also requires two-decimal strings, so the symptom list covers only part of what the spec requires.
- Run the issue's own example before and after the edit.
- Fix the source in place, keep public names and signatures, and write the file the task names.

**Evidence from `base1`.** It read the issue, the spec and the tests correctly. It then ended with "Let's start by implementing the fix" and made no edit, no `output/CHANGES.md` and no verification. The `systemprompt.md` already says "Never end a turn by only saying what you will do next", and `hooks.json` plus `scripts/check_output.py` already block finishing before the fix and deliverable exist. A single trajectory shows no new gap in those components, so I left `systemprompt.md`, `guardrails.md`, `tool_guidance.md`, `hooks.json` and the script unchanged. I did not check whether the Stop hook actually fired in `base1`.

I did not add any skills or plugins, so the trigger-line, template-brace and script-existence rules don't apply to this edit.