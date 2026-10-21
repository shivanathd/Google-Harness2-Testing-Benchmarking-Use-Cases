---
name: arbitration-order-markup
description: Procedure for marking up a counterparty's or tribunal's proposed order (interim measures, procedural order, similar) for one side, tested against the controlling orders, the contract and the client's internal strategy memo. Use when the assignment is a redline of a draft order with commentary.
---

# Marking up a proposed order for one side

Operation: COMPARE the draft (text under review) with the controlling instruments, TEST the strategy memo against
them, then MARK UP. Every note keeps four layers apart: what the draft says; what the controlling instrument says
(pinpoint); why it matters; what the markup now says. Keep contract law, seat/lex arbitri, rules, and tribunal
power separate -- tie each change to the instrument that controls it.

## 1. Plan first (scratch `plan.md`, not in output/)
- File map: each document, role, author, date, read in full or not. The memo's issue list is a checklist, not the
  baseline: read the draft paragraph by paragraph yourself and also list defects the memo does not mention.
- Table, one row per draft paragraph: controlling-instrument pinpoint (procedural orders, contract clause, application, rules) | consistent /
  departs / new / silent | accept, reject or revise | replacement wording. Include draft-internal conflicts
  (cross-references, numbering, figures that differ between recital and operative text).
- Memo audit: tick every memo statement (paragraph numbers, figures, section numbers, quotations, what the
  Application says) against the record. Follow the record where the memo is wrong; log each error once.
- Do-not-object list in the memo: honour it; show accepted provisions with a short "no change" note only where useful.

## 2. Audience
Decide who reads the file. If the markup is to be filed with the tribunal and served (as the memo or tribunal
email says), the notes must argue only from the record and rules: no privileged memo content, no internal
assessments, no instructions-to-associate tone. Fallbacks appear in the file only if the memo directs
it be presented there. Client facts that appear only in the memo (not in any exhibit) are stated as the
client's position with a bracket "[to be evidenced]", never as established fact.
Put a single tracked `banner` at the top, headed as an internal draft note to be removed before filing, listing:
open client decisions, memo errors found, record conflicts and bracketed items, and cites to verify. The final
reply repeats it briefly; the file must stand alone.

## 3. Build
Load `redline-docx`. Each objection = tracked edit + adjacent inline note (pinpoint to source). Replacement language
must be complete and usable (numbers, days, defined terms, cross-references to renumbered or inserted paragraphs).
New paragraphs use a numbering that does not disturb existing cross-references (e.g. 7A). Read the accepted view
once end to end for contradictions among inserted and untouched clauses.

## 4. Reconcile and check
- Dates: when the system clock is later than the record's dates, use the record's dates and say so.
- Record a source hierarchy for conflicts (tribunal order > contract > party filing > internal memo) and log each
  conflict in the banner rather than silently choosing a version.
- Where the memo and record differ on a legal characterisation (mandatory vs discretionary power, whether a body is
  a "court or regulatory authority"), flag it as an open point; do not assume.
- Reopen the saved .docx, list tracked changes and comments, confirm it parses and the banner is present.
