---
name: arbitration-playbook-redline
description: Checklist for redlining a counterparty arbitration agreement against a client playbook and internal instructions, and writing the tiered cover memo. Use for any arbitration clause or agreement markup review.
---

# Arbitration agreement redline against a client playbook

Operation: COMPARE the counterparty form (baseline) to the playbook (client position), RECONCILE the playbook with the partner/client instruction emails, then DRAFT replacement text, in-document comments and a priority memo. Keep these layers distinct in every comment: what the form says (source text), what the playbook requires (client rule, with section number and Required/Preferred/Fallback), why it matters (legal/commercial inference), and what you recommend.

## 1. Before drafting: build three tables from the record
- **Clause map**: every article/section of the form, the playbook section it meets, and "no playbook position" for the rest (notices, entire agreement, amendment, severability, counterparts, survival, signature blocks). Silence is a finding to state, not a reason to skip the clause.
- **Gap list**: playbook topics with NO counterpart in the form (these are insertions, not edits). Check every playbook section, including those the instruction emails do not mention.
- **Tier reconciliation**: playbook section-level labels (Required/Preferred/Fallback) and the playbook's own priority list (Critical/Important/Recommended) can disagree with each other and with client emails. The memo tier follows the instruction email's tier names; where a client email elevates an item, use the client's tier and say so. State each mismatch once in the memo and use the same tier for the same item in the redline notes and the memo. Check both files at the end.
  - Typical mismatches: an item the playbook lists as Recommended that the client email calls critical; an item Required in its own section but Important or Recommended in the priority list; a section with both a Preferred position and a Required floor.

## 2. Test the form against the instruments, not just the playbook
- Domestic vs international: identify each party's and the target's place of organisation/HQ from the recitals before applying any institution rule (this decides whether ICC is ever allowed).
- Counterparty home test: compare seat and governing law with the counterparty's principal office in the recitals.
- Do not mix the layers: arbitration agreement law, seat, rules/institution, tribunal powers, timetable, enforcement. Where the form has the FAA clause, a seat change and a governing-law change are separate edits.
- Cross-references: the form references the main agreement (e.g. notices to a CIA section, conflict clause giving the exhibit priority). The main agreement is not in the record unless supplied. Say it was not reviewed, and flag cross-references and the playbook's Delaware-consistency requirement as unverified.
- Never state the current title, version or content of an institutional rule set (AAA/JAMS/ICC rules, emergency or appellate rules) or a statute beyond what the playbook supplies. Use the playbook's wording and flag "verify before sending".

## 3. Conforming changes (where redlines usually break)
After each substantive edit, trace what else in the form depends on it, and edit it in the same pass:
- Defined terms and every use of them: ICC, ICC Rules, Arbitrator (sole) vs Tribunal, Seat, definitions section.
- Carve-outs into the exclusivity clause (court relief), the finality/appeal-waiver clause (appellate arbitration), the remedies clause (damages waiver), the award clause and discovery clause (expedited track overrides), the cost clause (fee shifting vs administrative fee sharing).
- New provisions must not collide with each other. Test: expedited track timing arithmetic (10 business days is about 14 calendar days; hearing within 30 days after appointment; award 45 days after filing leaves little or no margin) and whether appellate review applies to expedited awards; class-waiver wording that bars "consolidated" proceedings vs consent-based consolidation; confidentiality exceptions vs the retention clause and any investor-reporting need; hearing location vs seat. Resolve with drafted language or raise as an open decision for the client. Do not leave a collision silent.
- Insertions with no approved-form text available: draft from the playbook wording and flag that the client's approved forms (if the playbook refers to them) should be compared.

## 4. Redline file conventions
- Use real tracked changes on the original file (load the `redline-docx` skill for the builder). Put every explanatory comment INLINE in the document as a bracketed tracked paragraph, not only as a Word comment balloon: the review reader extracts body text and drops comment balloons, so balloon-only comments are invisible. Each comment cites the playbook section, the Required/Preferred/Fallback class (and tier), and the fallback so the client sees negotiating room.
- The same artifact may be read in an accept-all view, where deleted text is invisible. So each comment states what the form said and what it became, in words. Check that reject-all reproduces the original.
- Comments reveal fallbacks and privileged playbook content. Mark the file as an internal draft and say in the memo that an external version needs the notes stripped.
- Do not alter signature blocks, dates or party details. Where a record figure is reused (equity amounts, percentages), reconcile it (e.g. contributions sum to total equity; equity plus debt equals enterprise value; stakes sum to the controlling interest) and say it reconciles.

## 5. Cover memo
- Audience: the supervising partner first (draft for their review), then the client GC. Address it as the assignment email directs (a memo the associate returns to the partner for review is addressed to the partner, with the client named as the onward recipient), and state who reviews before it goes out.
- Structure: summary and the client's stated top priorities first (confirm each is delivered, by clause number); then every change by tier, each row giving form text, markup, playbook section and class, fallback and escalation requirement (no Required position may be conceded without GC approval); then open decisions; then assumptions; then record anomalies.
- Open decisions and anomalies to check in the record every time: conflicting deadlines across emails (compute weekdays for the stated dates), sender/domain/firm-name mismatches on the counterparty transmittal, items the playbook leaves silent, escalation triggers, documents referred to but not supplied.
- Keep fact, inference and recommendation separate. Do not invent authorities; cite only the statutes and rules the playbook gives, and mark anything else unverified.
- Final check before stopping: every playbook section is either marked up or noted as compliant; every tier label and number in the memo matches the redline; every named deliverable exists and re-opens.
