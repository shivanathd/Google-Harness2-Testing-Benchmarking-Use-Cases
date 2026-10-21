# arbitration-international-dispute-resolution/identify-arbitration-agreement-issues

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/identify-arbitration-agreement-issues/agg1`)
- components: 2 skills; 1,524 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md, "Doing the work" deliverable bullet (base: "verify each produced file is non-empty and re-opens cleanly"; candidates: trigger for deliverable-check)
candidates: agg1, inv1
change: Replaced the base sentence that asks the agent to verify each binary deliverable is non-empty and re-opens cleanly with: build with Python or pandoc, then load `deliverable-check` and run it on each produced file before finishing. The two candidates carry identical wording.
observed: inv1 built the memo (l.1668), loaded deliverable-check (l.1676), and ran a full readback with an ID tally from the saved file (l.1679). Its source cross-check (l.1863) corrected three defects in its own draft: a renewal sentence cited to H&G §II.A (it sits under §I, which I confirmed), a Heller quotation missing "initial" (the email reads "well north of the initial $178M"), and an unsourced distance figure. Its final count, 3 Critical / 6 High / 7 Medium / 4 Low = 20, matches its table. A naive grep over all ID occurrences had given 8 M / 5 L, so the count has to be taken from table rows. agg1 loaded the skill after its build (l.1674→1681). Its readback found the memo body had no title (l.1691), and it fixed that plus two pointers (l.2087–2096). Final 2/8/4/2 = 16 matches its headings. Base1 had no trigger and read back with head/tail only (l.1667, l.1735). It stated "22 issues … 4 Critical, 5 High, 7 Medium, and 3 Low" (l.1755) against a 19-row table. Dom1 reconciled its count (20) without this trigger, by recounting the saved file with python-docx (l.1723).
verdict: confounded

component: systemprompt.md, arbitration trigger bullet (new line: when the assignment is to review arbitration or dispute-resolution provisions across instruments, load `arbitration-clause-issues-review`)
candidates: agg1, dom1
change: Added one bullet that loads the arbitration skill for this task type. Base and inv1 have no such line.
observed: Both runs loaded the skill at their first action (dom1 l.1; agg1 l.1). Both memos contain what base1 and inv1 lack. They give an FAA Chapter 2 / New York Convention route (dom1 deliverable l.287; agg1 l.290). They answer the client's seat and U.S.-enforcement questions explicitly (dom1 l.295; agg1 l.297). They use [Verify] tags 24 and 28 times, against 6 in base1 and 0 in inv1. Base1 does not give the FAA route, and inv1 gives only a conditional seat recommendation (l.246). The trigger's only mechanical effect is loading the skill, so its output effect cannot be separated from the skill's content.
verdict: confounded

component: skills/deliverable-check/SKILL.md
candidates: agg1 (five steps, plus a sentence that a range row such as "M-1 to M-7" counts each ID, and a sentence to re-check the memo's own pointers and quotations), inv1 (five steps without those two sentences)
change: New on-demand checklist: exact filenames; full readback; totals counted from the readback; cross-references checked against the source; final-message figures taken from the saved file.
observed: Same skill, different execution. inv1 ran the step-4 source check and found and fixed the three defects listed under the trigger row (l.1863–1864). agg1 ran the pointer part (two fixes, l.2087–2096). Its final message says it did not re-check clause numbers against the source (l.2148). Step 4 with its source check is present in both forms, so the gap is not explained by the two sentences that differ. Neither run shows the count step failing once it was run.
verdict: confounded

component: skills/arbitration-clause-issues-review/SKILL.md (§1 layers, §2 per-instrument anatomy incl. exhibits, §3 cross-instrument table and accuracy check, §4 enforcement posture, §5 quote-before-change, §6 before-finishing checks)
candidates: dom1 (§6 counts: "re-count from the file"; full-text: exhibits must have been read before claiming coverage), agg1 (§6 counts points to the deliverable-check counts step; full-text adds: a read that stops before the document ends is not coverage, so re-read by offset first)
change: New six-section skill for arbitration-clause review. Keeps layers separate, requires each instrument's exhibits to be recorded, asks for a cross-instrument comparison and an accuracy check of third-party statements, requires the FAA route to be marked for statute confirmation, requires quoting before any change, and lists before-finishing checks.
observed: Consistent contrast with base1 and inv1, which lack the skill. Both skill runs produce the FAA route, explicit answers to client questions, a cross-instrument comparison, an accuracy table, and [Verify] tags. Neither base1 nor inv1 has a comparison table in the §3 form; I found none by row label. Coverage: both skill memos state that the SA exhibits were read (dom1 deliverable l.23, "Read in full: … Exhibits A to D, Schedule 1"; agg1 l.19–21). The logged SA observation ends at source line 503 (the Exhibit A table header) in base1, inv1 and agg1, and base1 and agg1 are both exactly 50,021 bytes, which points to an output cap. No run logs a re-read. But agg1 quotes SA Exhibit B word for word, and base1, inv1 and agg1 all call Exhibit B "to be attached", none of which appears in any logged observation. So the logs probably understate what the model saw, and the record cannot show whether the agg1 stop-before-end rule changed anything. The §5 quote-before-change rule: base1's L-2 ("remove §15.9's exception"; the SA §15.9 has no exception) does not recur. Neither candidate proposes changing §15.9, so the record does not show the rule producing that.
verdict: confounded

component: plugin/README.md, scripts/README.md, skills/README.md
candidates: agg1, dom1, inv1 (identical in all three; absent from base_harness)
change: Added rig documentation. The plugin README says Stop hooks in hooks.json enforce in-loop behaviour. The scripts README describes helpers under scripts/. The skills README describes on-demand loading.
observed: No candidate ships a hooks.json, no run fires a Stop hook, and no run reads any of the three READMEs (zero mentions in all four rollouts). dom1 wrote scripts/build_memo.py as an ad hoc build script (l.1713). That was a run-time choice, not an effect of the README.
verdict: no observed effect

## Transferable lesson
- **cue**: A review deliverable whose final message restates totals (issues by severity, instruments, placeholders) that the deliverable's own summary table also tallies, with the verification step expected to check those totals before finishing.
- **lesson**: In the verification component (deliverable-check step 3, and the systemprompt line that sends the agent to it), require each total in the final message to be recomputed by a command over the saved file, counting only the summary-table rows (a range row such as "M-1 to M-7" counts each ID it covers), and to be quoted from that output rather than from working memory.
- **evidence**: Edit rows "systemprompt.md, deliverable bullet" and "skills/deliverable-check/SKILL.md" (both confounded). Contrast: base1 stated "22 issues" (l.1755) against a 19-row table, reading back with head/tail only. Inv1, agg1 and dom1 each recounted from the saved file, and their final totals match their tables (20, 16, 20). Inv1's first unrestricted grep over-counted (8 M / 5 L), so the restriction to table rows is part of the operation.
- **confidence**: low. Every row here rests on one rollout per candidate, and base1's miss could be a one-off. Dom1 reconciled without deliverable-check, so the count contrast is not isolated to one edit. The lesson is narrowed to totals only; the record does not show the readback or source-check steps helping the counts, and the source-check contrast is weaker than it looks because agg1's quotations were accurate without it.
