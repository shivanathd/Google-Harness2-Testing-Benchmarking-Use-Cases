---
name: procedural-order-review
description: Procedure for responding to a draft procedural order or other tribunal/counterparty draft by redline plus cover letter, checked against earlier orders and the client's internal strategy materials. Use when the assignment asks for a markup of a draft order together with a letter or memo.
---

# Responding to a draft procedural order: redline + cover letter

Operation: COMPARE the draft (text under review) with the earlier orders (baseline the draft claims to supplement),
TEST the client's strategy material against both, then MARK UP and WRITE. Keep the layers separate in every note:
what the draft says, what the earlier order/rule says (pinpoint), why it matters, what we ask for.

## 1. Before drafting (record in a scratch file `plan.md`, not in output/)
- File map: every document, role (draft under review, earlier orders, client strategy memo, expert/consultant
  email, third-party letter), author, date, and whether read in full. Extracted text longer than ~30KB may be
  truncated in the tool result: write each extraction to a scratch file and read the file in full.
- Paragraph table: for each draft paragraph, the earlier-order paragraph it touches (same topic, same number
  or different) and the verdict: consistent / departs from earlier order / new / silent. A draft that says it
  "supplements" earlier orders may contradict them; a departure with no express statement of modification is itself
  an objection. Also list the draft's own internal conflicts (numbering, cross-references, arithmetic such as
  total hearing hours versus time allocated, dates versus weekdays).
- Strategy-memo audit: tick each memo statement (paragraph references, dates, hours, counts, who is where) against
  the record. Where the memo is wrong, follow the record in both deliverables and list each memo error once in the
  final reply and in a note to the supervising lawyer; do not copy the error and do not silently correct it.
- Source hierarchy: the assignment instruction, then the client's specific instruction, then the strategy memo,
  then the earlier orders for what was ordered, then the draft/counterparty papers. Record each conflict and the
  version chosen.
- Anomalies to scan for every time: sender domain or firm name differing from the signature, addresses that differ
  between documents, dates that differ between orders (e.g. a conference date), deadlines already passed relative
  to the record's own timeline (use dates from the record, not the system clock), steps the draft treats as done
  that the earlier order schedules later.

## 2. Audience and privilege
- Decide who reads each deliverable. A redline and cover letter addressed to the Tribunal (copied to the other
  side) are external: they must argue only from the record and the rules, and must not carry the strategy memo's
  privileged content (fallback positions, internal assessments, expert-consultant advice, the client's tactics).
  Put any fallback the supervising lawyer may want to hold back in the final reply as an option, not in the filing.
- Address the letter as the record directs (Tribunal via the case manager, copy to opposing counsel). Do not invent
  signatures, dates, enclosures or authorities. If a date or enclosure is unknown, use one clearly bracketed
  placeholder and list it in the final reply.
- Cite only instruments in the record. Any rule or statute article cited from memory goes in a short "verify before
  filing" list in the final reply.

## 3. Build, in this order (write each file before polishing the other)
1. The requested redline .docx (exact filename from the task): load the `redline-docx` skill. Every objection is a tracked edit
   with an adjacent inline note; accept-with-comment points get a note only. Proposed replacement language must be
   complete and usable (numbers, days, dates), and consistent with the cover letter.
2. Cover letter: summarise the principal objections in priority order, each with the draft paragraph, the earlier
   order/rule it conflicts with, and the exact relief requested; reservation of rights; list of enclosures. The same
   figures, paragraph numbers and requests must appear in the redline and the letter (diff them at the end).
3. Reopen both files with `read_doc.py`; run `check_redline.py`; scan both for leftover placeholders, internal-only
   terms (external audience) and mismatched numbers.

## 4. Final reply
Short: what was delivered, choices needing the supervising lawyer's decision (disclosed fallbacks, deviations from
the memo), memo errors found, record anomalies, items to verify, and that no visual render was possible.
