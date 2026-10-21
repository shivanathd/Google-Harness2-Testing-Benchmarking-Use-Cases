# arbitration-international-dispute-resolution/identify-arbitration-agreement-issues

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/identify-arbitration-agreement-issues/agg1`)
- components: 1 skills; 2,306 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/arbitration-clause-review/SKILL.md (new on-demand method skill) plus the one-line trigger at the end of systemprompt.md
candidates: dom1, agg1 (adopted; its harness has this skill, and the harness.diff files show dom1 and inv1 against it). inv1 removed it.
change: Adds a method-only skill with six parts:
- Build a snapshot table of every instrument.
- Trace the precedence clauses of all instruments together.
- Test each statement in the counterparty memo against the operative clause.
- Map each client priority to an issue.
- Draft replacement language, a fallback and negotiating realism.
- Run end checks, including draft-versus-executed framing and a list of unverified authorities.
The system prompt carries a trigger line that tells the agent to load it.
observed: Both rollouts with the skill (dom1, agg1) called `Skill arbitration-clause-review` as their first action (line 1 of each trajectory). Neither of the two rollouts without it did.
- agg1: about 60KB memo with prefixed issue IDs. Critical issues include precedence, forums, joinder and the damages bar.
- dom1: about 60KB memo with DR-01 to DR-18, six Critical issues, a statement-by-statement test of the Harmon & Grey (H&G) memo (H&G-n and CL-n tables), a client-priority map that flags Heller's walk-away position as not to be disclosed, and a list of unverified authorities.
- base1: about 40KB, with four Critical issues and no skill.
- inv1: about 31KB, with 17 issues and two Critical.
Both skill runs state that the documents may be drafts or may be signed. Both give pre-signing and amendment framing and add a "do not quote to counterparty" handling note. The base and inv1 memos do not give both framings. They either assume drafts (inv1) or treat them as pre-signing.
verdict: helped. Two independent rollouts with the skill produced the same richer structure and the two without it did not. It is still one rollout per arm, and I judged memo structure, not legal accuracy, so this is tentative.

component: systemprompt.md "Review reading discipline" block (four bullets)
candidates: agg1 (adopted harness). dom1 deleted the block. inv1 replaced it with a longer "Review procedure" block.
change: Short always-on rules:
- Inventory every file and open the `.eml` directly.
- Make byte-chunk reads abut or overlap.
- The operative clause controls over a summary, with pinpoint cites for each mismatch.
- Take the date basis from the record's own timeline and say how it relates to the memo date.
observed: Comparing agg1 (block present) with dom1 (block deleted), both runs took the same route. They extracted whole documents to /tmp and read them, and parsed the `.eml` with Python. Both produced a dual-framing date section and a divergence test of the H&G memo. No behavioural difference traces to the block. The gap in chunked reads that motivated it appeared only in base1, which used `head -c 30000` and then `tail -c` from Article 13. The skill runs did not do that, so the bullet was never exercised. Base also handled the summary-versus-clause mismatch unprompted.
verdict: no observed effect

component: skill section 6 date-check wording ("compare the record's dates with the memo date" in agg1, "check dates against today's date" in dom1)
candidates: agg1 vs dom1
change: Two forms of the same instruction. agg1 compares the record's signing and effective dates with the memo date. dom1 checks them against today's date.
observed: Both memos give the memo date as 19 Oct 2026 and state that all record dates have passed. Both leave signed or unsigned open and give both framings. Wording made no visible difference.
verdict: no observed effect

component: systemprompt.md "Review procedure (matter documents)" block, replacing the reading-discipline block and the skill trigger
candidates: inv1
change: The skill was removed. A longer always-on procedure took its place:
- Extract once to a scratch directory.
- Classify sources as summary or operative text.
- Fix the date basis from the record.
- List planned issues before building, then reopen the file and verify.
observed: inv1 produced the shortest memo (about 31KB), with 17 issues and only two Critical. It has a "Date basis" paragraph saying the documents are drafts and the dates may have run, but no separate pre-signing and amendment framing section. The issue list is flat, and Medium items such as notice addresses and definitions sit alongside the main ones. Without the skill there is no snapshot table, no per-priority client map and no target-architecture check. I cannot isolate whether the shorter memo came from the missing skill or from the longer always-on procedure.
verdict: confounded

## Transferable lesson
- **cue**: A review or issue-spotting task over a multi-instrument document suite, including a counterparty summary and client emails, where the record's dates and signing status are unclear. The harness can hold a reusable review method either inline in the system prompt or as an on-demand skill.
- **lesson**: Put the review method in a separate on-demand skill file, for example skills/<topic>-review/SKILL.md. It should hold only matter-independent steps: a per-instrument snapshot table, a joint trace of precedence clauses, a clause-by-clause test of every counterparty-summary statement, a client-priority-to-issue map, replacement language with a fallback, and a "draft versus executed" check that gives both pre-signing and amendment framing. Add one trigger line to systemprompt.md telling the agent when to load it. Do not copy the method into always-on system prompt text. Keep any always-on reading rules to short bullets. Those rules showed no effect when they were removed.
- **evidence**: Skill rows. Both skill runs (dom1 and agg1) loaded the skill as their first action. Both produced about 60KB memos with a snapshot table, a summary-versus-clause test, a client-priority map and dual signed/unsigned framing. The runs without the skill were base1 (about 40KB, no dual framing) and inv1, which put a longer procedure inline (about 31KB, 17 issues, two Critical, no dual framing). The reading-discipline row shows no difference between agg1 and dom1 once the skill was present.
- **confidence**: low-medium. It rests on one rollout per arm and on memo structure and length, not on checked legal quality. The inv1 contrast is confounded, because inv1 differs by both removing the skill and adding the inline procedure. The skill-versus-no-skill pattern is consistent across the two skill runs and the two non-skill runs.
