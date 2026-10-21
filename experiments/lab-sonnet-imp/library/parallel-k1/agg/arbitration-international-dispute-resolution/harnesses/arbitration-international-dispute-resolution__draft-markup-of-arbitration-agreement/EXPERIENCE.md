# arbitration-international-dispute-resolution/draft-markup-of-arbitration-agreement

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/draft-markup-of-arbitration-agreement/agg1`)
- components: 2 skills; 4,618 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/redline-docx/ (SKILL.md plus tracked_redline.py and check_redline.py)
candidates: inv1, agg1
change: Added a tested JSON-spec builder for tracked changes. It also adds a checker (reject-all equals original, no leftover terms, accepted-view dump). The skill says python-docx is missing and bracketed notes should be inserted as tracked paragraphs.
observed: base1 found python-docx missing and hand-wrote WordprocessingML (base1 around line 1026–1039). dom1 had no skill, hit missing lxml and python-docx, built a venv, and delivered Word comment balloons (comments.xml, 31 comments). The reviewer reader showed no comment text for dom1's redline. inv1 and agg1 used the builder and delivered inline bracketed notes visible in the reader (31 in inv1, 28 in agg1) with a passing reject-all check. inv1's first build crashed on malformed spec JSON and was then fixed. This is a plausible reliability and visibility gain. Each side has only one rollout, and the memo-audience difference also separates the runs, so the effect is not isolated.
verdict: confounded

component: skills/arbitration-playbook-redline/SKILL.md
candidates: dom1, agg1
change: Added a checklist: clause map, gap list and tier reconciliation up front. It also calls for conforming-change and collision tests, no invented rule titles, and anomaly checks (deadlines, sender domain, missing main agreement). The memo is to be addressed to the person the assignment email names. dom1's version had Whitmore/Cascadian section numbers hard-coded and vaguer comment-format wording. agg1's version is generic and requires inline bracketed tracked paragraphs.
observed: base1 and inv1 (no skill) addressed the memo to Stadler with a "draft for Ostrander review" stamp. dom1 and agg1 addressed it to Ostrander first, with Stadler as onward recipient. dom1 and agg1 also raised the appellate-timing issue for expedited awards. agg1 additionally raised the 48%/24% anomaly, the Jan 11 vs Jan 12 deadline conflict, and the domain mismatch. dom1 caught the expedited sole arbitrator vs "non-starter" conflict. base1 and inv1 each raised only some of these. dom1's looser comment-format wording ("format the email asked for") did not prevent balloon comments. agg1's explicit inline-paragraph wording plus the builder gave visible notes. Single rollouts, and the skill is bundled with the other edits, so the attribution is not isolated.
verdict: confounded

component: systemprompt.md (rewrite: inventory first, source hierarchy, plan outputs, verify artifact; trigger lines for both skills)
candidates: inv1 (rewrite with redline-docx trigger), dom1 (base prompt plus playbook trigger only), agg1 (rewrite with both triggers)
change: inv1 and agg1 replaced the base prompt's generic steps with a numbered procedure. It covers an inventory of all files including emails, a source hierarchy applied in both deliverables, early output planning, and read-back verification. It also adds notes that python-docx is absent and that .eml bodies need decoding. dom1 only appended one trigger line for the playbook skill.
observed: inv1 and agg1 surfaced a "source hierarchy and conflicts" table or section, with tier conflicts and the Jan 11/12 deadline conflict. dom1 reached the Ostrander routing through the skill, not the prompt. agg1 loaded the playbook skill on its first action (Skill call at line 2). inv1 had no trigger line for the playbook skill, so the prompt rewrite alone did not give the Ostrander routing. The hierarchy's effect cannot be separated from the skills.
verdict: confounded

component: LongTermMEMORY.md (method-only notes)
candidates: inv1, agg1
change: Added seven generic method bullets. They cover baseline and instructions first, mark unverifiable agreements, reconcile tiers, report conflicts without silently correcting them, test the playbook's positions against each other, and check the tooling.
observed: No distinct behavior can be traced to this file. It largely duplicates the systemprompt and skill content. Neither inv1 nor agg1 cites it, and dom1 and base1 behaved comparably on the points it covers where those were already in the prompt or skill.
verdict: no observed effect

## Transferable lesson
- **cue**: A document-review or redline task whose assignment email names a specific recipient or comment convention, the review tool cannot read some constructs, and the environment lacks an expected library.
- **lesson**: In the review-skill component (here skills/arbitration-playbook-redline/SKILL.md), state the output-format conventions as explicit operations and do not rely on "use the format the email asked for". Require the memo to be addressed to the recipient the assignment email names, with the client as onward recipient. Require explanatory comments as inline bracketed tracked paragraphs, not Word comment balloons. Pair this with a working builder in a separate skill (skills/redline-docx), so the agent does not hand-roll XML or install packages. Keep the playbook skill generic, without matter-specific section numbers.
- **evidence**: The memo-audience row: base1 and inv1 (no playbook skill) addressed the memo to the client GC, while dom1 and agg1 (skill with audience instruction) addressed it to the partner. The tooling row: dom1 had only the loose "format the email asked for" wording and no builder, and delivered balloon comments the reader could not see. agg1 had the explicit inline instruction and the builder, and delivered visible bracketed notes. Both contrasts are single rollouts with bundled edits.
- **confidence**: low. Both contrasts rest on one rollout per arm, and the agg1 harness changed several components at once. The memo-audience pattern is the stronger of the two, since it holds across two skill-bearing runs against two without.
