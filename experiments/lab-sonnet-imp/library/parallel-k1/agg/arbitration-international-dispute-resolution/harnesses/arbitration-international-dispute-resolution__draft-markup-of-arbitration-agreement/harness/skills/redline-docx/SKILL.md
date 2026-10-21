---
name: redline-docx
description: Build a tracked-changes (w:ins/w:del) redline of a counterparty .docx from a JSON edit spec, then machine-check it (reject-all equals original, well-formed, no leftovers). Use for any "redline / markup / mark up the draft" deliverable.
---

# Redline a .docx with real tracked changes

Why this exists: python-docx is NOT installed in this environment, and a hand-rolled XML builder in an earlier
run first emitted ~14,700 per-character revisions (a list-vs-tuple comparison bug) and cost several turns.
These helpers are tested; do not rewrite them.

## Steps
1. Read the original and the controlling baseline (`python3 scripts/read_doc.py`). Then list paragraph indexes:
   `python3 -I <skill>/scripts/tracked_redline.py --list documents/<original>.docx`
2. Decide every change first (one row per clause: baseline rule, tier/classification, fallback, replacement text).
   Write the spec JSON in a scratch dir outside `documents/` and `output/`. Format is in the script docstring:
   `edits` (word-level diff of a paragraph), `inserts` (new paragraph after an anchor), `deletes` (strike a paragraph),
   `notes`/`note` (bracketed comment paragraph, inserted as italic tracked text -- this is the "bracketed comment"
   convention; use it when the instructions ask for bracketed comments), optional `banner`.
   Keep unchanged wording byte-identical to the original so the diff shows only real changes.
3. Build: `python3 -I <skill>/scripts/tracked_redline.py documents/<original>.docx spec.json output/<name>.docx`
   (exit non-zero + candidate list on a missing/ambiguous `match`; nothing is written then).
4. Check: `python3 -I <skill>/scripts/check_redline.py documents/<original>.docx output/<name>.docx --grep <old term> ... --accepted /tmp/accepted.txt`
   - FAIL on reject-all != original, bad `mc:Ignorable`, duplicate ids, implausible revision count.
   - `--grep` the superseded terms (old institution, seat, governing law, "Arbitrator", defined terms you renamed)
     and judge each hit: fix it, or record why it stays (e.g. a party's street address).
   - Read the accepted-view file end to end once: defined terms, cross-references to renumbered sections, and
     internal consistency of every inserted clause (deadlines that cannot all be met, a carve-out that
     contradicts another clause).
5. Re-read the delivered file through `python3 scripts/read_doc.py output/<name>.docx` (the same reader the work
   is read through) and confirm the tracked changes and notes appear. LibreOffice rendering crashes in the
   observed environment and `timeout` does not exist on macOS -- do not spend turns on visual rendering; say in
   the final reply that it was not rendered.

## Memo / second .docx
Write markdown, then `pandoc memo.md -o output/<name>.docx` (pandoc 3.x is present). Tables in pipe syntax convert
cleanly. Re-open with `read_doc.py` and confirm the tables survived.

## Internal notes vs. external draft
If the notes disclose the client's playbook, fallbacks or classifications, say so in the final reply and in the
memo (internal-only until notes are stripped). Produce an extra clean external file only if the task asks for one;
never add files beyond the named deliverables into `output/` without being asked.
