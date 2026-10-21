---
name: redline-docx
description: Build a tracked-changes Word redline (.docx) of a baseline or counterparty document, with bracketed playbook comments, then check it in both revision views. Use when the deliverable is a .docx markup, redline or comparison of a contract or instrument.
---

# Redline a .docx with tracked changes

## 1. Baseline and changes first
Extract the baseline and the competing text with `python3 scripts/read_doc.py <path>`, writing the output to a scratch file outside `output/` and `documents/`. Read it in ranges if the tool output is truncated. Before writing, list every consequential change with its source: the playbook or instruction section, or the competing document. Mark a source that is silent as silent; do not fill the gap.

## 2. Write the redline as Markdown in scratch
Pandoc turns spans into Word revisions. The span forms are:

- deletion: `[old text]{.deletion author="Firm name" date="2025-01-11T00:00:00Z"}`
- insertion: `[new text]{.insertion author="Firm name" date="2025-01-11T00:00:00Z"}`
- a replacement is a deletion span directly followed by an insertion span; nested spans work.

If the installed pandoc is unfamiliar, test these forms on a two-word file in scratch and read the `w:del`/`w:ins` XML before building the real redline.

Put `author=` on every span when you write it. A bare `{.insertion}` produces a revision with no author, and adding the attribute afterwards means a second pass over every span.

- Keep unchanged paragraphs and headings word-for-word from the baseline extraction.
- After each changed provision, add a bracketed comment paragraph, e.g. `> **[Comment — <source section>, <classification if the source gives one>: <reason>. Fallback: <if any>.]**`. A reader of the accepted view cannot see deleted text, so the comment must name what was removed or the original position.
- Do not leave a bracketed placeholder in operative text unless the choice is genuinely open; if it is, say so in the comment.

## 3. Build into the workspace output directory
Use the absolute path of the workspace `output/` directory:

    pandoc <scratch>/redline.md -f markdown+smart -o <workspace>/output/<exact-name>.docx

Do not `cd` into scratch and write with a relative `./output` path: a relative path resolves against the current directory, so the file lands in scratch rather than the workspace `output/`.

## 4. Check it
    python3 -I <this skill's directory>/scripts/check_docx.py <workspace>/output/<exact-name>.docx --terms <defined terms to trace>

The script reopens the file and reads it in the accepted and rejected views:

- **FAIL** (exit 1): unreadable file, or leftover span markup (`{.insertion`, `{.deletion`, `author=`) in either view. Fix the source and rebuild.
- **WARN**: no revisions; revisions without an author; a `Section X.Y` reference with no matching heading in the accepted text (references to another agreement are skipped); bracketed text outside a comment; a term used in the accepted view but not defined there. Each WARN needs a decision: fix it, or state it in the final message or cover memo. Do not drop it silently.
- **INFO**: revision counts, word counts, and per-term counts in each view with line numbers. The `--terms` list is a checklist; the script does not judge meaning.

## 5. Read the accepted view yourself
The check cannot see grammar or meaning. Read each changed section in the accepted view and check: a deletion with no replacement leaves a broken sentence (for example "The shall issue"); a defined term that is still used after its definition was changed or removed; a cross-reference that resolves but points to the wrong section.

## 6. Finish
Run `ls <workspace>/output/` and confirm every named deliverable is present. In the final message, say which views you checked and list any WARN you left open.
