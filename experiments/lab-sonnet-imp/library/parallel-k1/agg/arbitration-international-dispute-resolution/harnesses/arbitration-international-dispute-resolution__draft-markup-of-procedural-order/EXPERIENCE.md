# arbitration-international-dispute-resolution/draft-markup-of-procedural-order

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/draft-markup-of-procedural-order/agg1`)
- components: 2 skills; 2,569 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/redline-docx (SKILL.md, scripts/tracked_redline.py, scripts/check_redline.py)
candidates: inv1, agg1 (agg1 kept it; its decision note says it softened the header wording)
change: Added a tested builder that edits the original document.xml in place to produce real tracked insertions and deletions. Added a checker that confirms rejecting all changes reproduces the original and greps the accepted text. Added a skill rule that each tracked edit carries an adjacent inline bracketed note stating the ground. The base harness had no redline tooling.
observed: base1 built the redline with pandoc and put its 25 grounds in Word comment balloons. The extracted redline text (deliverables/base1) showed 1 bracket and no grounds, and the §17.3 list and TOC were flattened. inv1 and agg1 both loaded the skill at the start of the run and read the builder docstring before using it. In inv1 the first build crashed (tracked_redline.py line 224) and the second run worked after a spec fix. Reject-all matched the original. The extracted redline shows 38 bracketed notes (inv1) and 35 (agg1), each with a pinpoint. dom1 had no builder and used a visible strikethrough and bold-underline convention, with no native tracked changes. That form is readable but is not a real redline. This is the clearest execution contrast in the record. It is still one rollout per arm, and it is entangled with the systemprompt change that told the solver not to use comment balloons.
verdict: helped

## Transferable lesson
- **cue**: A review task that asks for a redline of an existing .docx, where the evaluating reader shows only extracted body text. Tracked deletions and Word comment balloons may not survive that extraction, and a hand-built or pandoc-built file can flatten the formatting.
- **lesson**: Put a tested in-place tracked-changes builder and checker in the harness skills directory. The builder should write real tracked edits into the original document.xml. The checker should confirm that reject-all reproduces the original and that the accepted text contains the key phrases. Add a skill rule that each tracked edit has an adjacent inline note stating what the draft said and what it is changed to. Add a systemprompt trigger line telling the solver to load the skill and not to build the redline with pandoc or put grounds in comment balloons. Also state the reader limitation in the systemprompt.
- **evidence**: Edit row "skills/redline-docx". base1 (pandoc, 25 grounds in comment balloons) extracted with 1 bracket and no visible grounds. inv1 and agg1 (builder plus inline notes) extracted with 38 and 35 bracketed notes and passed reject-all. dom1 had only visible-markup text conventions, which were readable but not a true redline. The skill and the systemprompt instruction ship together in both successful arms, so the row cannot say which one did the work.
- **confidence**: medium. The base-versus-builder contrast is concrete and consistent across two builder rollouts. Each arm is a single rollout. The reader limitation is inferred from the base extraction, not from a test of the reader. The skill and the systemprompt rule cannot be separated.
