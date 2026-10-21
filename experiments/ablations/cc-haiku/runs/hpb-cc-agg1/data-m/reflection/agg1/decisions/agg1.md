kept -> MERGE of pool/dom1 (skill + trigger) with two short INV rules, not wholesale adoption of either candidate -> dom1 alone lacks the completion and zsh rules that answer base1's failures (silent stop after the FX listing at rollout line 252, and `echo ====` aborts at lines 37, 82 and 96). inv1 alone carries about 850 bytes of always-on prose for a procedure the skill form covers. The workspace CLAUDE.md sizes (base 172 B, dom1 328 B, inv1 1063 B) track systemprompt plus tool_guidance, so the always-on cost is real. Correctness: both candidates wrote 24317.47 / 16 / 5, and my independent recompute from context/source matches (16 recognised, 5 refunds, gross 26983.86, refunds 2666.39), so the merge does not depend on which candidate was right.

kept -> skills/revenue-reconciliation/SKILL.md (dom1 text, unchanged except the next line) -> pool/dom1 rollout line 1 invoked the skill as its first action, and the run delivered the correct answer after an in-code profile (dup identity, status, FX coverage, refund join). The skill holds no task ids, dates or counts (grep clean). Base1 has no skill and delivered nothing (1/1).

revised -> skill "Missing rate" line: "stop and report" changed to "name the missing (date, currency) and the lines it leaves out in your final message, and still write the deliverable" -> no FX gap occurs in this export set, so this is a downside fix and not a trajectory moment. The original line ends the run with no output/, which is the costliest failure, and it contradicts the Artifact contract in the same file.

kept -> systemprompt trigger line ("When computing a period revenue figure ... load the `revenue-reconciliation` skill.") -> the name matches the directory verbatim, and dom1 rollout line 1 fired it (1/1 candidate). Without a trigger the skill is never opened.

kept -> systemprompt completion sentence (from inv1, merged with the skill's reopen check) -> base1 ended after its third observation (rollout line 252) with no tool call, no text and no output/ (deliverables/base1.md: "no deliverable produced"). This is 1/1 on the base set, so it is kept as a short generic rule rather than an enforcement mechanism. Both candidates reopened and checked their file.

dropped -> systemprompt "enough evidence" line (inv1) -> no rollout over-explored: base1 made 3 calls and stopped, inv1 made about 4 inspection calls before computing, and dom1 made about 4 reads. The line's premise is not in the evidence.

revised -> tool_guidance.md zsh rule, cut to one sentence -> base1 hit "(eval):1: === not found" at lines 37 (exit 1, && chain aborted, refunds not printed), 82 and 96. inv1 avoided the token with `----` and had no shell errors, and dom1 read files with the Read tool and had none. This is a fixed zsh behaviour, not sampling noise, and it is one line of always-on text.

dropped -> inv1 fallback paragraph ("after one failed fix switch to python3 -c") -> base1 recovered on the next call (line 96 succeeded with `;`), so the fallback was not needed in any rollout (1/1).

dropped -> hooks.json Stop gate that blocks finishing without output/ -> base1 produced nothing (1/1 base). The rule requires repeated evidence before enforcement, and both candidates delivered, so no second non-delivering rollout exists. Revisit if another rollout ends with no output/. plugin/*.ts is also not run in this rig.

dropped -> a calc helper under scripts/ -> both candidates hand-rolled one correct calculation in a single call each. Nothing was slow or wrong, and no script is named anywhere.

kept (unchanged, empty) -> guardrails.md and LongTermMEMORY.md -> no standing rule or durable domain fact appears in any trajectory outside the skill.

kept -> sub_agents (none) -> no bounded sub-task with a large input and small answer appears in any rollout.

Validation: systemprompt.md and tool_guidance.md contain no braces (only the pre-existing JSON example in plugin/README.md, which is not always-on). The skill's directory name appears verbatim in systemprompt.md, and its frontmatter has name and description.