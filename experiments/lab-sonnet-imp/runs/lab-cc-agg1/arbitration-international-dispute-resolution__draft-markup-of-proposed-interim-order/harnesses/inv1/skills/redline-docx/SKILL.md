---
name: redline-docx
description: Build a tracked-changes (w:ins/w:del) redline of a .docx from a JSON edit spec, with visible inline bracketed annotation paragraphs, then machine-check it (reject-all equals original, well-formed, no leftovers). Use for any "redline / markup / mark up the draft" .docx deliverable.
---

# Redline a .docx with real tracked changes

Why this exists: python-docx and LibreOffice are typically absent, and a pandoc-built redline that puts grounds in
Word comment balloons loses them (the review reader extracts body text only) and flattens lists and the TOC. This
builder edits the original document.xml in place (formatting, numbering, signature block preserved) and is tested;
do not rewrite it or hand-write WordprocessingML.

## Steps
1. Read the original and the controlling baseline (`python3 scripts/read_doc.py`). List paragraph indexes:
   `python3 -I <skill>/scripts/tracked_redline.py --list documents/<original>.docx`
   (`<skill>` = `skills/redline-docx` in the harness; if it is not on disk beside `scripts/`, search for
   `tracked_redline.py` once with `find / -name tracked_redline.py 2>/dev/null` and use that path.)
2. Decide every change first, one row per paragraph: baseline rule (pinpoint), the change, the reason, the fallback.
   Write the spec JSON in a scratch dir outside `documents/` and `output/`. Format is in the script docstring:
   `edits` (word-level diff of one paragraph: give the full new paragraph text; unchanged wording must be
   byte-identical, including the "**14.3**" bold number markers), `inserts` (new paragraph after an anchor),
   `deletes` (strike a whole paragraph), `notes`/`note` (an italic coloured tracked paragraph after the anchor),
   optional `banner`. Anchors are the unique start of the paragraph text, or `#N` from `--list` when the start is
   not unique (e.g. repeated bullet lines). Set `author` and a `date` that sits inside the matter timeline.
3. Annotations are INLINE bracketed note paragraphs (`note` / `notes`), never Word comment balloons. The reader
   shows the accepted view, where deleted text is invisible, so each note names the paragraph, says in words what
   the draft said and what the markup makes it, gives the ground with a pinpoint to the record, and states any
   fallback only if the audience may see it (see the audience section of the arbitration-order-markup skill).
4. Build: `python3 -I <skill>/scripts/tracked_redline.py documents/<original>.docx spec.json output/<name>.docx`
   (non-zero exit with a candidate list on a missing/ambiguous anchor; nothing is written then. Fix the spec and
   rerun once; do not loop. A paragraph containing a line break cannot be `edits`-ed: use `deletes` + `inserts`.)
5. Check: `python3 -I <skill>/scripts/check_redline.py documents/<original>.docx output/<name>.docx --grep <old term> ... --accepted /tmp/accepted.txt`
   - FAIL on reject-all != original, undeclared `mc:Ignorable` prefix, duplicate ids, implausible revision count.
   - `--grep` superseded terms (old numbers, durations, venue, defined terms you renamed) and, for an external
     audience, internal-only terms (privileged, memo, fallback, strategy); judge each hit and fix it or record why
     it stays.
   - Read the accepted-view file once end to end: cross-references to renumbered paragraphs, and that inserted
     clauses do not contradict each other or the untouched clauses (arithmetic, dates, paragraph numbers).
6. Re-read the delivered file through `python3 scripts/read_doc.py output/<name>.docx` and confirm the changes and
   notes appear. Say in the final reply that it was not rendered visually (no LibreOffice).

## Second .docx (letter / memo), only if the assignment names one
Write markdown, then `pandoc x.md -o output/<name>.docx` (pandoc 3.x is present). Pipe tables convert cleanly.
Re-open with `read_doc.py`.
