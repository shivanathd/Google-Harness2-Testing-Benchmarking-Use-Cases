# arbitration-international-dispute-resolution/draft-markup-of-procedural-order

- adopted: `agg1`  (run `lab-cc-agg1/arbitration-international-dispute-resolution/draft-markup-of-procedural-order/agg1`)
- components: 1 skills; 2,205 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (Doing the work, build bullet)
candidates: agg1, inv1 (dom1 kept the base wording)
change: Replaced the base "verify each produced file is non-empty and re-opens cleanly" with a requirement to read each produced file back through read_doc.py and check the extracted text against the assignment, stating that a file that opens, or a word or paragraph count, is not a read-back.
observed: The moment the bullet targets is the cover-letter check. BASE1 checked the letter by word count and paragraph count, and its final message says it "could only check the files structurally" (base1.md, letter build near the end). AGG1 ran read_doc.py on the letter but printed only `head -c 3000` after a word count (agg1.md ~l.1321–1335), so the read covered about the first two sections. The letter edit it made was in the build script before that read, so the read did not drive any change. INV1 built the letter and checked only its word count (inv1.md ~l.1263–1268) and never read the letter text back, although it did read the redline accept and reject views. DOM1, which lacks the bullet, ran a keyword-presence check on the letter via python-docx (dom1.md ~l.1254). No run found or corrected a defect through a read-back. Record note: pool/inv1 and pool/dom1 harness.diff files are computed against an intermediate "current" harness (the adopted merge), not base; these rows compare directory contents against base_harness.
verdict: no observed effect

component: systemprompt.md (Ground the work bullet, traceability)
candidates: agg1, inv1 (dom1 kept the base wording; dom1 reached a similar bracket through the skill's §3 rule instead)
change: Added that before a sentence added to a deliverable goes final, the agent checks that a document it read supports it; if none does, it rewords or removes the sentence; where the lawyer must confirm a fact it uses a short bracketed placeholder and names the gap in the final message.
observed: The shared moment is the agreement recital in draft ¶5 and the letter. BASE1 kept "Respondent has not agreed to paragraphs 10, 12, 14.3, 17, 18.1, 22.3, 22.4, 25.2 and 26.3" in redline ¶5 and "Respondent has not agreed to the provisions identified in the redline" in letter §G. Its final message says "I had no March–June 2024 correspondence to check this against" and that the files are "written to be filed as they stand." INV1 removed the sentence from ¶5 with no placeholder, has no agreement claim in its letter, and named the gap in its final message ("Client to confirm the March–June 2024 correspondence (not in the file) did not record agreement…"). AGG1 bracketed ¶5 and has no "has not agreed" claim, but letter §11.2 still states, unbracketed, "Respondent does not agree that the hearing schedule, the time allocation, the expert format, the document provisions or the costs provisions were agreed." The record contains no such correspondence (the memo never mentions it), so the adopted letter keeps an unverified statement of the kind the bullet and the adopted skill §3 both forbid. DOM1 bracketed both the ¶5 sentence and its "does not accept that it agreed" line.
verdict: confounded. The difference from base rests on one rollout per harness; in AGG1 the same point is also covered by the skill; INV1 is the only run that isolates this bullet, and it is one run. The direction is the same in all three candidates.

component: systemprompt.md (skill trigger line)
candidates: agg1, dom1 (identical wording)
change: Added "When the assignment is to review a draft procedural order or to prepare a redline, comments or objections on one, load the `procedural-order-redline` skill."
observed: Both runs called Skill("procedural-order-redline") as their first action (agg1.md line 1; dom1.md line 2). BASE1 and INV1 had no such skill and made no skill call. No run had the skill without the trigger line, so the trigger's effect cannot be separated from the presence of the skill file.
verdict: confounded

component: guardrails.md (citation line)
candidates: agg1, dom1
change: Added "Cite statutes and rules only from the matter record or a source you can check. If you rely on rule text that is not in the file, say so in your final message to the supervising lawyer, not in the filed document."
observed: BASE1's letter cites ICC Art 25(4) unbracketed (§E) and PILA Art 192 unbracketed (§G); only Art 192 is flagged, and only in chat. AGG1's letter brackets Art 25(4) ("[ICC Rules Article 25(4) text to be verified before filing]", §10) and brackets the PILA point for Swiss counsel (§7.1). DOM1's letter does not cite Art 25(4) at all; its final message lists ICC Arts 22, 25(2), 25(4), 38 and others as rule text relied on but not verified. INV1 has neither the guardrail line nor the skill, yet its letter also brackets Art 25(4) ("[counsel to verify text]"), its final message says the Art 25(4) text is not in the file, and its letter does not cite the PILA point. So the marking the line targets appears in a run without it.
verdict: confounded. The effect the line was written for also appears in INV1 without it, so its marginal contribution is not shown.

component: skills/procedural-order-redline/SKILL.md (new workflow skill)
candidates: agg1 (adopted, merged form), dom1 (its own form; §3 and §5 differ on where bracketed notes may go)
change: New skill covering the source hierarchy, issue checks (arithmetic, dates, cross-references, repeated dates, names and caption, unilateral change), rule-text discipline, third-party and client-decision material, deliverable anatomy, and the final-message order.
observed: Compared with the two runs without it, the skill runs differ on three moments. (i) Alpstein letter: BASE1 put its content into the Tribunal letter (retention in September 2022, the findings), unbracketed; INV1 also put the content in, bracketed only as an enclosure note. AGG1 kept the content out and bracketed the decision (letter §4.5); DOM1 bracketed it as "[Subject to client decision on disclosure: …]". (ii) PILA Art 192: BASE1 asserts it unbracketed; AGG1 and DOM1 bracket it for Swiss counsel. (iii) Caption: the draft caption reads "THERMOVANTURE AG". DOM1 corrected it as a tracked change with a comment. AGG1 did not change it, although its skill lists caption under issue checks, so its redline still reads THERMOVANTURE while its own letter reads "ThermoVenture AG". INV1 also left the caption. Counter-evidence against a skill-only attribution: INV1, without the skill, caught the Redfern 15 vs 19 April mismatch and the draft's numbering gaps, which BASE1 did not raise in its letter. The ¶14.5 treatment varied across all four (BASE1 unchanged; INV1 neutral rule; DOM1 limited to rejected privilege claims; AGG1 deleted), and the skill does not settle that choice. Both skill runs' final messages follow only part of §6's required order (AGG1 stops after item (c); DOM1 is cut off inside item (d)).
verdict: confounded. The skill is co-changed with the trigger line and the guardrail, and each harness has one rollout. The disclosure and rule-text patterns point in the skill's direction, but nothing isolates the skill.

component: skills/README.md, scripts/README.md, plugin/README.md (new)
candidates: agg1, dom1, inv1 (all three carry them; base has none)
change: One-line HTML-comment READMEs describing where skills, scripts and plugins live. plugin/README.md describes a Stop-hook format for hooks.json, but no candidate ships a hooks.json (the Stop hook was dropped), so that instruction points at nothing.
observed: No run opened any README in any of the four trajectories. The skill was loaded through the Skill tool, not via skills/README.md.
verdict: no observed effect

## Transferable lesson
- **cue**: A drafting or review assignment whose deliverable will be filed or sent, where the run must state facts about what a party said, agreed or did, and the record it was given lacks the correspondence that would show those facts.
- **lesson**: In the grounding bullet of systemprompt.md, make the check an edit to the artifact: before finishing, find each sentence that asserts a party's agreement, position or prior correspondence; if no source file supports it, delete it or replace it in the deliverable with a bracketed placeholder naming the fact to confirm, and list the gap in the final message. A gap named only in the final message, with the sentence left in the deliverable, does not meet the check.
- **evidence**: The systemprompt.md traceability row (confounded). Contrast at one moment: BASE1 left "Respondent has not agreed to…" in redline ¶5 and letter §G, and its final message says it had no correspondence to check that against; INV1, with this bullet and no skill, removed the sentence from ¶5 and the letter and named the gap in its final message. AGG1 shows the operation is only partly applied in the adopted candidate: it bracketed ¶5 but left an unbracketed denial of agreement in letter §11.2.
- **confidence**: low. The base-versus-candidate contrast is one run each, and the adopted run also carries a skill rule covering the same point, so the attribution to the bullet is not isolated. The lesson is narrowed to the artifact-level operation that BASE1 skipped, which is the part the record shows directly.
