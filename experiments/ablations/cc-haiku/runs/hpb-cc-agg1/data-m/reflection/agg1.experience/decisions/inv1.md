Evidence: one rollout (base1). It made three shell calls, then ended with no assistant text and no output/answer.json. The deliverable folder reads "(no deliverable produced)". No run was available to compare against, so each change rests on this single trajectory.

1. **context/harness/systemprompt.md**: added an "enough evidence" line and a completion condition (deliverable exists, reopened and checked for the requested fields, then a short final message).
   - Moment: after the third observation (rollout line 98, the FX-rate listing) the run stopped with no further call. It never computed anything and never wrote output/. The prompt's only instruction was "write the requested deliverables under output/", and it was skipped.
   - The "enough evidence" line addresses the same gap. The run spent its calls on inspection and never reached computation.

2. **context/harness/tool_descriptions/tool_guidance.md** (was empty): added a zsh note and a bounded fallback.
   - Moment: the same zsh failure occurred twice in one run. Line 35 (`cat ... && echo ==== && cat refunds.csv`) returned "Exit code 1" with "(eval):1: === not found", and the `&&` chain stopped before refunds printed. Line 83 repeated the same unquoted `echo ====` pattern and hit "(eval):1: === not found" again. Only the third call (line 97), which dropped the `====` separator, ran to completion.
   - The note says to quote such tokens, read the error line before re-running, and after one failed fix switch to a `python3 -c` one-liner.

Considered and not changed:
- **No Stop hook (hooks.json) to block exit without a deliverable.** The rule requires repeated evidence that prose is skipped, and this is one run. If other candidates or rollouts also end silently without output/, this is the next lever, using the hooks.json Stop form the plugin README describes.
- **No script.** Nothing repeated enough to justify one, and the failure was a one-off.
- **CLAUDE.md is in the workspace (172 bytes) and the run never opened it.** Its contents are not in context, so I could not tell whether it matters. Worth checking whether the runtime already loads it.
- **Quoted thousands-separator amounts in transactions.csv** (for example "2,845.66") break `cut -d,` and `awk -F,`. The run never hit this because it did not split those rows, so it is a risk, not a realised failure. I left it out. It is a data-format fact, and the parallel candidate owns those.
- **LongTermMEMORY.md and guardrails.md** stay empty. Nothing in this trajectory was a domain fact or a standing rule.