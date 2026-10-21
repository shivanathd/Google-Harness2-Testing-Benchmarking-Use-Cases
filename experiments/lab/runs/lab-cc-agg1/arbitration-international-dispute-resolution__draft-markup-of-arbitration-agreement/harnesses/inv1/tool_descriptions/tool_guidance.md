Shell tool notes (macOS, zsh):

- A bare run of `=` characters (`echo =====`) fails with "not found" and stops the `&&` chain, so the later steps silently do not run. Use `echo ---`, or put the separator in its own call.
- BSD `sed -i` needs an argument (`sed -i ''`). For several replacements in one file, use `python3 -I -c` or the Edit tool.
- Write each deliverable to its path under the workspace `output/`. Do not `cd` into a scratch folder and write with a relative path.
- In `read_doc.py` output for a .docx with tracked changes, deletions and insertions appear as `[text]{.deletion ...}` and `{.insertion ...}` spans. Pandoc's plain view (`-t plain`) drops those markers and runs the deleted and inserted text together, so do not read revisions from it.
