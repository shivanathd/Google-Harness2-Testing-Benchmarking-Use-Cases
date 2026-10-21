# arbitration-international-dispute-resolution/draft-markup-of-proposed-interim-order

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/draft-markup-of-proposed-interim-order/agg1`)
- components: 2 skills; 2,436 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/redline-docx/ (SKILL.md, tracked_redline.py, check_redline.py) plus the "For any redline or markup… load the `redline-docx` skill… no comment balloons" line in systemprompt.md
candidates: dom1, agg1, inv1
change: The base harness had no redline tooling. The edit added a tested builder that edits the original document.xml in place. It writes real tracked insertions and deletions, and puts each ground in an inline bracketed note paragraph. The checker confirms reject-all equals the original and prints the accepted view. The systemprompt line says the reader shows body text only and forbids hand-built pandoc/XML and comment balloons "even if a memo asks for margin comments". inv1 carried a lightly reworded copy of the skill with the same builder.
observed: base1 had no skills. It hand-built a pandoc/XML redline with 52 tracked edits and 50 comment balloons. Its extracted deliverable shows 0 "NOTE" grounds, and deleted paragraphs appear only as "[Deleted.]". All three skill-carrying rollouts loaded the skill ("Launching skill: redline-docx" in agg1) and delivered with inline notes: 42 in dom1, 45 in agg1 and 48 in inv1. agg1 and inv1 ran the checker ("OK: reject-all text == original"). The two skill-carrying rollouts I read through to the end re-read the file with read_doc.py. The three candidates share this edit and differ in other components, so one component is not isolated. But the contrast between base1 and all three is the same, and the mechanism is visible in the trajectories.
verdict: helped

component: skills/interim-measures-order-review/SKILL.md (defect checklist, audience rules, memo-audit points) plus its trigger line in systemprompt.md
candidates: dom1, agg1
change: The edit added an on-demand skill with practitioner knowledge for this work type. It covers a source hierarchy; the external audience for the filed markup; a paragraph-by-paragraph defect checklist with pinpoints; a list of memo-versus-record errors; the Bogotá-forum risk under SOA 14.4; and the final-reply contents.
observed: The dom1 and agg1 deliverables and final replies bracket the record conflicts (exhibit dates, PetroChem article date, counsel addresses). Both also flag the memo's signature-block address, the PO1 "Section 9" slip and the memo's "mandatory" cross-undertaking error. Both state the Bogotá-forum risk. base1, with no skill, also found the uplift error, the "may" cross-undertaking, Section 9 vs 8 and the Bogotá risk in its final reply. The visible gains were smaller: base1 overwrote the order's PetroChem date with the Application's, and it did not flag the memo's signature-block address. The skill was loaded together with the redline skill in every run, so the analysis gain cannot be separated from the format gain. I did not compare the analytical text paragraph by paragraph.
verdict: confounded

component: systemprompt.md "Review and redline work" block (reader limitation, load-skill triggers, use record dates, final-reply contents)
candidates: dom1, agg1
change: Added four lines of always-on text to the base prompt.
observed: Both rollouts that carried it loaded both skills and used inline notes. Both final replies list memo errors and record anomalies. agg1's reply adds that it used record dates and flags the clock conflict. base1 did none of this, but the skills themselves were also absent from base1, so the prompt block is not isolated from the skills.
verdict: confounded

component: systemprompt.md "Reading documents" hint (output over ~30KB is truncated: write extractions to a scratch file and read in full; decode .eml quoted-printable)
candidates: agg1 (short form), inv1 (longer form, with a decode one-liner and a pandoc/python-docx availability note); dom1 lacked it
change: agg1 added one sentence to the prompt. inv1 rewrote the whole "Doing the work" section into a five-step numbered procedure and added the same hint.
observed: agg1's first action wrote every document to a scratch file, and no truncation appears in its trajectory. inv1 also extracted to scratch first. dom1, without the hint, printed PO1 straight into the tool result, which truncated it ("[20002 characters truncated]", rollouts/dom1.md around line 292). dom1 still cited later PO1 paragraphs correctly, so I did not trace any lasting loss. The trajectories show that the hint changes behaviour. They do not show a quality effect, and each form was tried in one rollout. inv1's wholesale rewrite of the base bullets has no isolated effect.
verdict: confounded

component: skills/arbitration-order-markup/SKILL.md (inv1's generic matter-type skill; mandates an internal banner)
candidates: inv1
change: Added a generic method skill that overlaps the interim-measures skill. It requires a tracked top-of-file "INTERNAL DRAFT NOTE - delete before filing" banner listing client decisions, memo errors and conflicts.
observed: The inv1 deliverable opens with that banner, inside a file meant to be filed and served. The banner discusses the Bogotá filing risk and the memo's alternatives. inv1's own final reply tells the user to delete the banner and every note citing the memo's internal assessments before filing. agg1 and dom1 kept that material in the chat reply and the notes did not cite the memo. inv1 also had a background extraction task stopped at its time limit, but it still delivered. The note count was comparable (48 against 42 and 45). Only the banner was clearly worse, from one rollout.
verdict: hurt

component: guardrails.md, LongTermMEMORY.md, tool_descriptions/tool_guidance.md, plugin and scripts
candidates: none (unchanged in all candidates)
change: None.
observed: Nothing to compare.
verdict: no observed effect

## Transferable lesson
- **cue**: A review or redline task whose deliverable is read through a text extractor that drops comment balloons and deleted text, with a memo that asks for margin comments. A prior run lost its reasons in extraction, or the harness has no redline tooling.
- **lesson**: In the harness, add a tested tracked-changes builder with a reject-all checker as a skill (skills/redline-docx). It should write real tracked edits plus an inline bracketed note after each change. Add a systemprompt.md line that names the reader limitation, points to that skill, and forbids hand-built pandoc/XML and comment balloons even when the instructions ask for margin comments. Keep privileged memo content and internal "delete before filing" banners out of the skill's required output when the markup is to be filed or served. Put internal flags in the final reply instead.
- **evidence**: Edit row "skills/redline-docx". base1 had no skill and produced 52 edits plus 50 comment balloons, and its extracted file showed 0 grounds. dom1, agg1 and inv1 all loaded the skill and delivered 42, 45 and 48 visible inline notes. agg1 and inv1 ran the checker's reject-all check. The banner caution comes from the inv1 skill row (hurt): its mandated internal banner put memo-derived content into the file to be served, and inv1's own final reply told the user to delete it. The other skill and prompt rows are confounded and do not support further claims.
- **confidence**: medium. The format contrast is stark and consistent across three candidates, and the mechanism is visible in the trajectories. But it is one task with one rollout each, I did not read the checker output in the rollouts, and the legal-analysis gain from the matter skill is not isolated.
