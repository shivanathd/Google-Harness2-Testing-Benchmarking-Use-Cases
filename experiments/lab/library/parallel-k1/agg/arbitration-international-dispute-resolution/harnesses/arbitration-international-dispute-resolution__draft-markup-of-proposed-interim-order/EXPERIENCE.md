# arbitration-international-dispute-resolution/draft-markup-of-proposed-interim-order

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/draft-markup-of-proposed-interim-order/agg1`)
- components: always-on edits only; 1,588 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: guardrails.md
candidates: agg1 (adopted)
change: The base guardrails.md is empty. agg1 adds one bullet: a file filed with or sent to a tribunal or counterparty carries no internal, privileged or strategy-memo content and no comment that must be deleted before it goes out; such points go in the final message.
observed: base1 (no such line) moved memo references into filing-facing comments, then tagged 16 comments "INTERNAL – delete before filing" (build at rollout L1618; decision at L1818; audit at L1912 reports 16 internal). Its final message asks the lawyer to delete them (L1965). agg1 ran a self-scan of its comments for memo-derived or internal content (L1756–1767), recorded only legitimate uses of "privileged" and "internal instructions", used no INTERNAL tags, and moved the memo's figures and its §14.4 reading into the final message (L1800–1819). inv1 (base) wrote no INTERNAL tags, and its final message states the comments contain no privileged memo content (L1544). The agg1 accepted text has no memo references. Comment bodies are only partly visible because action inputs are truncated at roughly 1,200–1,500 characters, so the clean comment set is not fully verified.
verdict: confounded

component: guardrails.md
candidates: dom1
change: A different form of the same file. dom1 adds one bullet: do not state what a rule, statute or case says, or omits, unless its text is in the file; mark it for verification and list it in the final message. Relative to base, dom1 adds this and no privilege line.
observed: There is no dom1 trajectory (rollouts/dom1.md: "AttributeError: 'str' object has no attribute 'get'"), so there is no execution trace. A deliverable does exist (deliverables/dom1, 21,050 chars). That contradicts decisions/agg1.md, which records dom1 as non-delivering. The accepted text has no memo or INTERNAL text. It brackets disputed recital facts ([21 April 2025], [14 March 2025], [1 January 2022], the Respondent's address) and has no "[rule text to be verified]" marks. Comments are not in the text conversion, so internal tags cannot be checked. This line cannot be separated from the skill and the trigger line.
verdict: confounded

component: skills/interim-order-redline/SKILL.md (new file)
candidates: dom1
change: A new 78-line skill covering controlling sources, the measure-by-measure test, findings-to-orders consistency, concessions in replacement wording, forum limits, cross-references, rule-text discipline, privilege in the filed file, and the final-message order. Its content is instance-free.
observed: No run in the record calls the Skill tool, so whether dom1 loaded it is unobserved. Artifact differences are not attributable. dom1 ¶4.1 reads "makes no finding at this stage as to breach", with no "provisionally satisfied" or "failed to deliver" wording. base1 has "failed to deliver" in ¶4.1; agg1 and inv1 have "provisionally satisfied… prima facie case". The base draws already differ on this (base1 vs inv1), so the difference may be draw variance rather than the skill. dom1 keeps the USD 47.5m freeze (¶5) under a conditional ¶4.4 with no finding that a dissipation risk is established, so the §3 measure-versus-finding check is not visibly met.
verdict: confounded

component: systemprompt.md
candidates: dom1
change: One bullet added: when the assignment is to review, redline or comment on a proposed interim order, load the interim-order-redline skill.
observed: No trajectory. No run in the record invokes the Skill tool, so the trigger's effect is unobserved.
verdict: confounded

component: plugin/README.md, scripts/README.md, skills/README.md (new in the harness tree; absent from base_harness)
candidates: agg1, dom1, inv1
change: Three HTML-comment README files. plugin/README.md describes a Stop-event hooks.json pointing at a check script. The scripts and skills READMEs describe how to add a helper or a skill. There is no executable content.
observed: No rollout created a hooks.json, a skill, a plugin or a helper beyond the task's read_doc.py. The agg1 workspace listing (rollouts/agg1.md L1–38) shows only CLAUDE.md, documents, output and scripts/read_doc.py. No Stop-hook block occurs in any trajectory, and no run calls the Skill tool.
verdict: no observed effect

## Transferable lesson
- **cue**: An agent drafts a file that will go outside the firm, to a tribunal or counterparty, from a source set that includes privileged or internal material. Partway through the build it finds content that must stay out of that file. The harness rule on what the outward file may contain either says nothing or states only the content prohibition.
- **lesson**: In guardrails.md, state the outward-file rule as a prohibition on comments that would have to be removed before sending, and name the final message as the only destination for internal points. The rule must close the "tag it for later deletion" route, not only prohibit privileged content.
- **evidence**: guardrails.md (agg1 form), a confounded row. The execution contrast: base1, with no rule, found memo references in filing-facing comments and tagged 16 comments "INTERNAL – delete before filing", so the file needed repair (rollout L1818, L1912, L1965). agg1, with the bullet, used no tags and moved those points into the final message (L1756–1819). inv1, on the same base, wrote no tags, so the defect appears in 1 of 2 base draws.
- **confidence**: low. The record has one run with the line, one base run with the defect and one clean base run. The line is the only guardrail change in agg1, but agg1 also differs from base1 in judgment calls the line does not reach, so the attribution is not isolated. The escape route itself is observed directly in base1, and the entry is limited to that.
