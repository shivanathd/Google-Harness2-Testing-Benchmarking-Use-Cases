Evidence caveat: all three rollouts failed to deliver. None fixed the bug or wrote output/CHANGES.md: base1, dom1 and inv1. Every edit below rests on weak evidence, and the merged harness has not been run.

kept -> inv1 systemprompt.md rules (never end a turn on intent, read-then-edit-then-verify order, protect tests) -> base1 ended on "Let's start by implementing the fix" with no edit and no CHANGES.md. The library lesson also says prose alone has little effect, so this is only a cheap supplement to the hook.

kept -> inv1 path guidance in systemprompt.md and tool_descriptions/tool_guidance.md (root-relative paths, start with list_files ".") -> base1 spent 2 calls on "workspace" and "/" errors. dom1 never recovered: it called list_files three times on an absolute path and produced nothing. inv1 had the guidance and went straight to list_files "." and read the files.

kept -> inv1 hooks.json and scripts/check_output.py (Stop hook gating on CHANGES.md, compilation, a modified source file and passing tests) -> in inv1 the hook blocked finishing three times, with the failing-test output shown. The library entry swe-e shows a hook-enforced deliverable appearing where prompt-only runs produced nothing. This is the only deterministic lever on delivery. The hook did not cause a fix in inv1.

revised -> check_output.py: added a source-digest check that blocks when the source is byte-identical to the previous stop attempt -> inv1 wrote the identical buggy invoicing/totals.py three times (449 chars each). The mtime heuristic passes on a no-op write. The library's swe-e rollouts show the same no-op rewrite. The check is deterministic and not a free-text reminder. It is untested in a run. I only checked that the script compiles.

kept -> inv1 LongTermMEMORY.md (re-derive spec-clause probes, compare return types with the spec) -> short and generic. In inv1 and base1 the agent never noticed that the test expects strings while the code returns floats. Weak support.

kept -> dom1 skills/fix-python-bug/SKILL.md, loaded on demand -> it was dom1's first action and cost one call. dom1 never got to use it, because it stalled on paths, so there is no behavioural evidence. It is the only component that carries Decimal, ROUND_HALF_UP and spec-clause knowledge, which is what inv1's no-op rewrites lacked. It costs nothing until loaded. I added its trigger line to systemprompt.md, placed after reading the files so it does not replace the first listing call.

revised -> systemprompt.md: added one line saying that rewriting the same content is not an edit, with no instance-specific example -> inv1 repeated the no-op write. The library says "make a real edit" text did not help, so this is low-confidence support for the hook check.

dropped -> dom1's "load the skill first" line in systemprompt.md and its "never end on intent" sentence -> inv1's prompt already covers both. Loading the skill first would put it ahead of the list_files "." call.

dropped -> guardrails.md edits -> no candidate changed it and no trajectory moment points to it.