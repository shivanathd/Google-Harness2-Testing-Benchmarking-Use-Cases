**Evidence:** There is one rollout, base1. It produced `{"errors": 15, "users": 6, "top_code": "E500"}`. I recomputed this from `source/app.log` with an independent parser and got the same figures: 15 errors, 6 distinct users, and E500 at 5 against E403 and E401 at 4 each. The base run was correct without any harness help.

**Traps it handled by itself:**
- It converted each timestamp from its own UTC offset before applying the window.
- It used the half-open window.
- It ignored the traceback continuation lines, whose embedded `upstream ERROR user=… code=…` text carries a different user and code.
- It ignored INFO/WARN lines whose message says "retrying after ERROR".

**Changes:**
1. I added `skills/log-incident-stats/SKILL.md` and a one-line trigger in `systemprompt.md`. The skill sits outside always-on context, so it costs nothing until a log-statistics task invokes it. It writes down the practitioner rules from the rollout: define events by header line, take level from the header token, convert to UTC, use a half-open window, count distinct users over in-window errors only, and check for a tie at the top code. It also lists reconciliation checks to run before finishing. Its workspace-facts section is labelled as this instance and says to re-verify.
2. I made no other changes. The other harness files are empty by design, and the run showed no procedural failures to fix. This is a low-risk, additive move rather than a fix for an observed failure.